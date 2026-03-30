# waypoint_processor.py
def smooth_path_to_waypoints():
    """
    将平滑路径转换为去重后的航点列表
    返回：[[纬度, 经度, 高度], ...]
    """
    smooth_path = [
        (47.3977419, 8.5455937, 10),
        (47.3977419, 8.5459937, 10),
        (47.3974419, 8.5459937, 10),
        (47.3974419, 8.5455937, 10),
        (47.3977419, 8.5455937, 10),
    ]
    
    waypoints = []
    last_lat, last_lon = 0, 0
    for lat, lon, alt in smooth_path:
        # 过滤重复航点（经纬度差值小于1e-6视为同一航点）
        if abs(lat - last_lat) < 1e-6 and abs(lon - last_lon) < 1e-6:
            continue
        waypoints.append([lat, lon, alt])
        last_lat, last_lon = lat, lon
    
    print(f" 平滑路径转换完成，共 {len(waypoints)} 个航点")
    return waypoints

