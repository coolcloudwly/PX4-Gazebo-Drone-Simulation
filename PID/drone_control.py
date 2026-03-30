import asyncio
import sys
from mavsdk import System
from mavsdk.offboard import OffboardError, VelocityNedYaw
from PID import PIDController

# 全局停止标志
run_flag = True

# --------------------------
# 错误屏蔽（封装成函数）
# --------------------------
def suppress_all_errors():
    sys.tracebacklimit = 0
    import warnings
    warnings.filterwarnings("ignore")
    import logging
    logging.basicConfig(level=logging.CRITICAL)
    logger = logging.getLogger()
    logger.disabled = True
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"
    os.environ["GRPC_VERBOSITY"] = "NONE"

# --------------------------
# 停止监听任务
# --------------------------
async def check_stop():
    global run_flag
    await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
    run_flag = False
    print("\n🛬 正在停止控制...")

# --------------------------
# 无人机连接
# --------------------------
async def connect_drone():
    drone = System()
    await drone.connect(system_address="udp://:14540")
    print("等待无人机连接...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(" 无人机已连接！")
            break
        await asyncio.sleep(0.1)
    return drone

# --------------------------
# 等待飞控就绪
# --------------------------
async def wait_drone_ready(drone):
    print("等待无人机就绪...")
    async for health in drone.telemetry.health():
        if health.is_armable:
            print(" 飞控就绪！")
            break
        await asyncio.sleep(0.2)

# --------------------------
# 解锁 + 启动OFFBOARD
# --------------------------
async def arm_and_start_offboard(drone):
    print(" 解锁电机")
    await drone.action.arm()
    await asyncio.sleep(0.5)
    await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
    try:
        await drone.offboard.start()
        print(" OFFBOARD 启动成功！")
        print(" 按 回车 停止控制")
        return True
    except:
        await drone.action.disarm()
        return False

# --------------------------
# PID位置控制主循环
# --------------------------
async def pid_position_control(drone):
    global run_flag
    pid_x = PIDController(kp=1.0, ki=0.01, kd=0.6)
    pid_y = PIDController(kp=1.0, ki=0.03, kd=0.6)
    pid_z = PIDController(kp=1.2, ki=0.0, kd=0.8)

    target_x, target_y, target_z = 3.0, 0.0, -2.0
    asyncio.create_task(check_stop())

    while run_flag:
        try:
            pos_ned = await drone.telemetry.position_velocity_ned().__anext__()
            cx = pos_ned.position.north_m
            cy = pos_ned.position.east_m
            cz = pos_ned.position.down_m

            vx = pid_x.compute(target_x, cx)
            vy = pid_y.compute(target_y, cy)
            vz = pid_z.compute(target_z, cz)

            await drone.offboard.set_velocity_ned(VelocityNedYaw(vx, vy, vz, 0.0))
            print(f"目标X={target_x:.1f},{target_y:.1f},{target_z:.1f} 当前X={cx:.1f},{cy:.1f},{cz:.1f}", end="\r")
        except:
            pass
        await asyncio.sleep(0.05)

# --------------------------
# 安全停止
# --------------------------
async def stop_offboard_safe(drone):
    try:
        await drone.offboard.stop()
        print("\n 已停止控制，无人机会自动悬停")

    except:
        pass

