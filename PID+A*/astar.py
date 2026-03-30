# astar3d_lib.py
# 3D A* 子程序库（恢复26方向斜向移动）
import heapq
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# --------------------------
# 子程序 1：3D节点类
# --------------------------
class Node3D:
    def __init__(self, x, y, z, parent=None):
        self.x = x
        self.y = y
        self.z = z
        self.parent = parent
        self.g = 0.0
        self.h = 0.0
        self.f = 0.0

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z)

# --------------------------
# 子程序 2：生成26个全方向（恢复斜向移动）
# --------------------------
def get_26_directions():
    dirs = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                dirs.append((dx, dy, dz))
    return dirs

# --------------------------
# 子程序 3：3D距离计算
# --------------------------
def distance_3d(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)

# --------------------------
# 子程序 4：获取合法邻居（使用26方向）
# --------------------------
def get_valid_neighbors(current_node, grid):
    max_z = len(grid)
    max_y = len(grid[0]) if max_z else 0
    max_x = len(grid[0][0]) if max_y else 0
    dirs = get_26_directions()  # 恢复26方向
    neighbors = []

    for dx, dy, dz in dirs:
        x = current_node.x + dx
        y = current_node.y + dy
        z = current_node.z + dz

        if 0 <= x < max_x and 0 <= y < max_y and 0 <= z < max_z:
            if grid[z][y][x] == 0:
                neighbor = Node3D(x, y, z, current_node)
                neighbors.append(neighbor)
    return neighbors

# --------------------------
# 子程序 5：A* 3D寻路算法
# --------------------------
def search_path_3d(grid, start, end):
    start_node = Node3D(*start)
    end_node = Node3D(*end)
    open_list = []
    closed_list = []

    heapq.heappush(open_list, start_node)

    while open_list:
        current = heapq.heappop(open_list)
        closed_list.append(current)

        if current == end_node:
            path = []
            while current:
                path.append((current.x, current.y, current.z))
                current = current.parent
            return path[::-1]

        neighbors = get_valid_neighbors(current, grid)

        for neighbor in neighbors:
            if neighbor in closed_list:
                continue

            neighbor.g = current.g + distance_3d(
                (current.x, current.y, current.z),
                (neighbor.x, neighbor.y, neighbor.z)
            )
            neighbor.h = distance_3d(
                (neighbor.x, neighbor.y, neighbor.z),
                (end_node.x, end_node.y, end_node.z)
            )
            neighbor.f = neighbor.g + neighbor.h

            skip = False
            for node in open_list:
                if neighbor == node and neighbor.g >= node.g:
                    skip = True
                    break
            if skip:
                continue

            heapq.heappush(open_list, neighbor)
    return []
