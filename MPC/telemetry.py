async def get_state(drone):

    data = await drone.telemetry.position_velocity_ned().__anext__()
    
    pos = data.position
    vel = data.velocity

    return [
        pos.north_m,
        pos.east_m,
        pos.down_m,
        vel.north_m_s,
        vel.east_m_s,
        vel.down_m_s
    ]

