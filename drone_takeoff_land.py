import asyncio
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk.telemetry import LandedState

async def run():
    # 1. 初始化无人机对象
    drone = System()
    print("🔗 正在连接无人机（适配你的14540端口）...")

    # 核心修改：连接PX4显示的remote port 14540
    await drone.connect(system_address="udp://:14540")

    # 2. 等待连接成功（只判断是否连接，适配MAVSDK 1.4.1）
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

    # 3. 等待无人机就绪
    print("⏳ 等待无人机就绪...")
    async for health in drone.telemetry.health():
        if health.is_armable:
            print("✅ 无人机可解锁！")
            break
        await asyncio.sleep(0.5)

    # 4. 解锁→起飞→悬停→降落→锁定
    try:
        print("🔓 解锁电机...")
        await drone.action.arm()
        await asyncio.sleep(1)

        print("✈️  执行起飞...")
        await drone.action.takeoff()
        await asyncio.sleep(20)  # 起飞+悬停20秒

        print("🛬 执行降落...")
        await drone.action.land()

        # 等待降落完成
        async for landed in drone.telemetry.landed_state():
            if landed == LandedState.ON_GROUND:
                print("✅ 无人机已成功降落！")
                break

        await drone.action.disarm()
        print("🔒 电机已锁定")
        print("🎉 任务全部完成！")
    except ActionError as e:
        print(f"❌ 操作失败：{e}")

if __name__ == "__main__":
    asyncio.run(run())

