from mavsdk.offboard import VelocityNedYaw
import asyncio

async def start_offboard(drone_sys):  # 改名：drone → drone_sys
    for _ in range(50):
        await drone_sys.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(0.02)
    await drone_sys.offboard.start()

async def send_vel(drone_sys, vx, vy, vz):  # 改名：drone → drone_sys
    await drone_sys.offboard.set_velocity_ned(VelocityNedYaw(vx, vy, vz, 0.0))

