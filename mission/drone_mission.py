# drone_mission.py
import asyncio
from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)

async def run_mission(waypoints, system_address="udp://:14540"):
    """
    执行无人机航点任务
    参数：
        waypoints: 航点列表 [[纬度, 经度, 高度], ...]
        system_address: 无人机连接地址（默认udp://:14540）
    """
    # 初始化无人机对象并连接
    drone = System()
    await drone.connect(system_address=system_address)
    print(" 等待无人机连接...")
    
    # 等待无人机连接成功
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(" 已连接无人机！")
            break

    # 等待飞控初始化完成
    print(" 等待飞控初始化...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print(" 飞控初始化完成")
            break

    # 构建航点任务项（兼容新版MAVSDK）
    mission_items = []
    for lat, lon, alt in waypoints:
        mission_item = MissionItem(
            latitude_deg=lat,
            longitude_deg=lon,
            relative_altitude_m=alt,
            speed_m_s=5,
            is_fly_through=True,
            gimbal_pitch_deg=0.0,
            gimbal_yaw_deg=0.0,
            camera_action=MissionItem.CameraAction.NONE,
            # 新版MAVSDK必填参数
            loiter_time_s=0.0,                # 悬停时间
            camera_photo_interval_s=0.0,      # 拍照间隔
            acceptance_radius_m=1.0,          # 到达判定半径
            yaw_deg=float('nan'),             # 机头自动指向飞行方向
            camera_photo_distance_m=0.0       # 拍照距离间隔
        )
        mission_items.append(mission_item)

    # 上传航点任务
    mission_plan = MissionPlan(mission_items)
    await drone.mission.set_return_to_launch_after_mission(True)
    print(" 正在上传航点任务...")
    await drone.mission.upload_mission(mission_plan)
    print(" 航点上传成功！")

    # 解锁电机并启动任务
    print(" 解锁电机...")
    await drone.action.arm()
    print(" 开始执行任务！")
    await drone.mission.start_mission()

    # 监控任务进度
    async for mission_progress in drone.mission.mission_progress():
        current = mission_progress.current
        total = mission_progress.total
        print(f"飞行进度：{current}/{total}")
        
        if current == total:
            print(" 所有航点飞行完成，自动返航中...")
            break

    await asyncio.sleep(2)
    print(" 任务全部完成！")

