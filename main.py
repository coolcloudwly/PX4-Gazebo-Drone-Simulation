# main.py
import asyncio
from waypoint_processor import smooth_path_to_waypoints
from drone_mission import run_mission

def main():
    """主程序入口：协调航点生成与无人机任务执行"""
    print("========== 第19天：规划与飞控联调 ==========")
    
    # 1. 生成航点
    waypoints = smooth_path_to_waypoints()
    
    # 2. 执行无人机任务
    asyncio.run(run_mission(waypoints))

if __name__ == "__main__":
    main()

