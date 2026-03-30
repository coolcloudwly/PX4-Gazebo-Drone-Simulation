import asyncio

async def connect(drone, uri):
    await drone.connect(system_address=uri)
    print("等待无人机连接...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ 无人机已连接")
            break
        await asyncio.sleep(0.2)

async def wait_for_arming(drone):
    print("⏳ 等待无人机可解锁...")
    async for health in drone.telemetry.health():
        if health.is_armable:
            print("✅ 无人机已准备好，可以解锁")
            break
        await asyncio.sleep(0.3)

async def arm(drone):
    print("🔓 正在解锁电机...")
    await drone.action.arm()
    await asyncio.sleep(1.0)

async def takeoff(drone, alt):
    print(f"✈️ 起飞至 {alt}m")
    await drone.action.set_takeoff_altitude(alt)
    await drone.action.takeoff()
    await asyncio.sleep(5)

async def land(drone):
    print("🛬 正在降落")
    await drone.action.land()
    await asyncio.sleep(5)

