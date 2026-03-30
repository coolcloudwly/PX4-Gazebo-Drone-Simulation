import asyncio
from drone_control import (
    suppress_all_errors,
    connect_drone,
    wait_drone_ready,
    arm_and_start_offboard,
    pid_position_control,
    stop_offboard_safe
)

async def main():
    # 屏蔽错误
    suppress_all_errors()
    
    # 1. 连接无人机
    drone = await connect_drone()
    
    # 2. 等待就绪
    await wait_drone_ready(drone)
    
    # 3. 解锁并启动OFFBOARD
    success = await arm_and_start_offboard(drone)
    if not success:
        return
    
    # 4. PID定点控制
    await pid_position_control(drone)
    
    # 5. 安全停止
    await stop_offboard_safe(drone)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        pass

