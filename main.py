import asyncio
from drone_control import (

    connect_drone,
    suppress_all_errors,
    wait_drone_ready,
    arm_and_start_offboard,
    pid_position_control,
    stop_offboard_safe
)

from astar import search_path_3d
from map import grid_3d,start_point,end_point
from get_pos import get_pos,gazebo_enu_to_pixhawk_ned
from smoothway import smooth_path_3d

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
    
    path= search_path_3d(grid_3d,start_point,end_point)
    
    # 2. ✅ 平滑处理（关键）
    path_smoothed = smooth_path_3d(path)
    
    h_x,h_y,h_z= get_pos()
    print(f"获取起点 {h_x:.1f},{h_y:.1f},{h_z:.1f}")
    
    for idx, pos in enumerate(path_smoothed):
    
    	x,y,z=pos
    	print(f"前往目标绝对点 第{idx+1}点{x:.1f},{y:.1f},{z:.1f}")
    	
    	
    	target_x,target_y,target_z=gazebo_enu_to_pixhawk_ned(x,y,z,(h_x,h_y,h_z))
    	print(f"获取目标相对点 第{idx+1}点{target_x:.1f},{target_y:.1f},{target_z:.1f}")
    	
    	# 4. PID定点控制
    	
    	await pid_position_control(drone,target_x,target_y,target_z)
    	
    # 5. 安全停
    await stop_offboard_safe(drone) 
    
    print(path)
    print(path_smoothed)
	    
	    
	   

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        pass

