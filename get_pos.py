import subprocess
import re

def get_pos(model_name="iris"):
    """
    读取 Gazebo 世界绝对坐标 x, y, z（ENU）
    无ROS、无依赖、实时真值
    """
    try:
        res = subprocess.check_output(
            ["gz", "model", "-m", model_name, "-p"],
            stderr=subprocess.DEVNULL
        ).decode()
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", res)
        x = float(nums[0])
        y = float(nums[1])
        z = float(nums[2])
        return x, y, z
    except:
        return 0.0, 0.0, 0.0

def gazebo_enu_to_pixhawk_ned(gaz_x, gaz_y, gaz_z, home_enu):
    """
    Gazebo世界ENU → PX4 NED 坐标转换
    """
    hx, hy, hz = home_enu
    dx = gaz_x - hx
    dy = gaz_y - hy
    dz = gaz_z - hz

    north = dy
    east = dx
    down = -dz
    return north, east, down

