import asyncio
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk.telemetry import LandedState
from mavsdk.offboard import OffboardError, PositionNedYaw

# 配置参数（按需修改）
SQUARE_SIDE = 8    # 正方形边长（米）
FLIGHT_HEIGHT = 5  # 飞行高度（米）
CONNECT_PORT = "udp://:14540"  # 你的14540端口

async def run():
    # 1. 初始化并连接无人机
    drone = System()
    print("🔗 正在连接无人机（14540端口）...")
    await drone.connect(system_address=CONNECT_PORT)

    # 等待连接成功
    connect_ok = False
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ 连接成功！")
            connect_ok = True
            break
        await asyncio.sleep(0.1)

    if not connect_ok:
        print("❌ 连接失败！")
        return

    # 2. 等待无人机就绪
    print("⏳ 等待无人机就绪...")
    async for health in drone.telemetry.health():
        if health.is_armable:
            print("✅ 无人机可解锁！")
            break
        await asyncio.sleep(0.5)

    # 3. 解锁+起飞
    try:
        print("🔓 解锁电机...")
        await drone.action.arm()
        await asyncio.sleep(1)

        print(f"✈️  起飞到 {FLIGHT_HEIGHT} 米...")
        await drone.action.takeoff()
        await asyncio.sleep(8)  # 等待起飞并悬停稳定

        # 4. 切换到Offboard模式（用于发送航点）
        print("🔄 切换到Offboard模式...")
        # 先发送初始位置（悬停在当前位置）
        await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -FLIGHT_HEIGHT, 0.0))
        # 启动Offboard
        try:
            await drone.offboard.start()
        except OffboardError as e:
            print(f"❌ Offboard启动失败：{e}")
            await drone.action.land()
            return

        # 5. 定义正方形航点（NED坐标系：北/东/下，下为负=高度）
        square_waypoints = [
            PositionNedYaw(0.0, 0.0, -FLIGHT_HEIGHT, 0.0),      # 起点（悬停点）
            PositionNedYaw(SQUARE_SIDE, 0.0, -FLIGHT_HEIGHT, 0.0),    # 北8米
            PositionNedYaw(SQUARE_SIDE, SQUARE_SIDE, -FLIGHT_HEIGHT, 0.0),  # 东8米
            PositionNedYaw(0.0, SQUARE_SIDE, -FLIGHT_HEIGHT, 0.0),    # 南8米
            PositionNedYaw(0.0, 0.0, -FLIGHT_HEIGHT, 0.0)       # 回到起点
        ]

        # 6. 依次飞向每个航点
        print("🟩 开始执行正方形航线...")
        for i, wp in enumerate(square_waypoints):
            print(f"📍 飞往航点 {i+1}: 北={wp.north_m}m, 东={wp.east_m}m")
            await drone.offboard.set_position_ned(wp)
            await asyncio.sleep(7)  # 每个航点停留7秒（足够飞到）

        # 7. 结束Offboard并降落
        print("🛬 结束航线，开始降落...")
        await drone.offboard.stop()
        await drone.action.land()

        # 等待降落完成
        async for landed in drone.telemetry.landed_state():
            if landed == LandedState.ON_GROUND:
                print("✅ 无人机已成功降落！")
                break

        await drone.action.disarm()
        print("🔒 电机已锁定")
        print("🎉 正方形航线任务全部完成！")

    except ActionError as e:
        print(f"❌ 操作失败：{e}")
        # 失败后自动降落
        await drone.action.land()

if __name__ == "__main__":
    # 适配不同Python版本的asyncio运行方式
    try:
        asyncio.run(run())
    except RuntimeError as e:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())

