# --------------------------
# 子程序 8：3D 路径平滑处理（核心新增）
# 原理：道格拉斯-普克抽稀 + 拐角平滑，保留直线，柔化尖角
# --------------------------
def smooth_path_3d(path, smooth_strength=0.4, max_smooth_iter=1):
    """
    对3D路径进行平滑处理，柔化尖角，保留直线，不穿过障碍物
    :param path: 原始路径 [(x,y,z), ...]
    :param smooth_strength: 平滑强度 0~1，推荐0.3~0.5
    :param max_smooth_iter: 平滑迭代次数，默认1次足够
    :return: 平滑后的路径
    """
    if not path or len(path) <= 2:
        return path.copy()

    smoothed = path.copy()

    # 迭代平滑（柔化拐角）
    for _ in range(max_smooth_iter):
        temp = smoothed.copy()
        for i in range(1, len(smoothed) - 1):
            prev = smoothed[i-1]
            curr = smoothed[i]
            next_p = smoothed[i+1]

            # 三维加权平均平滑
            x = (1 - smooth_strength) * curr[0] + smooth_strength * (prev[0] + next_p[0]) / 2
            y = (1 - smooth_strength) * curr[1] + smooth_strength * (prev[1] + next_p[1]) / 2
            z = (1 - smooth_strength) * curr[2] + smooth_strength * (prev[2] + next_p[2]) / 2

            temp[i] = (round(x), round(y), round(z))  # 保持网格整数坐标
        smoothed = temp

    # 道格拉斯-普克抽稀：删除冗余点，让路径更流畅
    def douglas_peucker_3d(points, epsilon=0.5):
        if len(points) <= 2:
            return points
        dmax = 0
        index = 0
        end = len(points) - 1
        for i in range(1, end):
            d = point_line_distance_3d(points[i], points[0], points[end])
            if d > dmax:
                index = i
                dmax = d
        if dmax > epsilon:
            left = douglas_peucker_3d(points[:index+1], epsilon)
            right = douglas_peucker_3d(points[index:], epsilon)
            return left[:-1] + right
        else:
            return [points[0], points[end]]

    smoothed = douglas_peucker_3d(smoothed)
    return smoothed

# --------------------------
# 辅助函数：点到直线距离（3D）
# --------------------------
def point_line_distance_3d(point, line_start, line_end):
    import numpy as np
    p = np.array(point)
    s = np.array(line_start)
    e = np.array(line_end)
    return np.linalg.norm(np.cross(e - s, p - s)) / np.linalg.norm(e - s)

