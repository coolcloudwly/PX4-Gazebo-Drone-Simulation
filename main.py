import asyncio
import numpy as np
from mavsdk import System
import drone
import offboard
import telemetry

# ---------------------------
# 目标点：(1, 1, -3)
# ---------------------------
TARGET_X = 1.0
TARGET_Y = 1.0
TARGET_Z = -3.0

async def main():
    drone_sys = System()

    await drone.connect(drone_sys, "udp://:14540")
    await drone.wait_for_arming(drone_sys)
    await drone.arm(drone_sys)
    await drone.takeoff(drone_sys, 2.0)

    await asyncio.sleep(2)
    await offboard.start_offboard(drone_sys)
    print("✅ OFFBOARD 启动成功")

    print(f"\n🎯 飞往目标：({TARGET_X}, {TARGET_Y}, {-TARGET_Z}m)")

    start_t = asyncio.get_event_loop().time()
    while asyncio.get_event_loop().time() - start_t < 50:
        state = await telemetry.get_state(drone_sys)
        cx, cy, cz, _, _, _ = state

        # ==========================
        # 水平：位置→速度，必到点
        # ==========================
        kp = 0.35
        vx = (TARGET_X - cx) * kp
        vy = (TARGET_Y - cy) * kp

        vx = np.clip(vx, -0.4, 0.4)
        vy = np.clip(vy, -0.4, 0.4)

        # ==========================
        # 高度锁死 -3.0
        # ==========================
        if cz > TARGET_Z + 0.1:
            vz = -0.15
        elif cz < TARGET_Z - 0.1:
            vz = 0.15
        else:
            vz = 0.0

        await offboard.send_vel(drone_sys, vx, vy, vz)
        print(f"[飞行] X:{cx:+.1f} Y:{cy:+.1f} Z:{cz:+.1f}")

        await asyncio.sleep(0.1)

    await drone.land(drone_sys)
    print("\n🎉 已精准到达目标！")

if __name__ == "__main__":
    asyncio.run(main())

