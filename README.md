# PX4-Gazebo-Drone-Simulation
# 基于PX4的多旋翼无人机自主飞行控制系统
基于PX4与Gazebo的无人机仿真、PID/MPC控制、航点飞行与算法验证

## 实现功能
- PX4 + Gazebo 环境搭建与软件在环仿真（SITL）
- 姿态 / 速度 / 位置三环 PID 控制与参数整定
- MPC 模型预测控制与轨迹跟踪
- Offboard 模式自主起飞、降落、航点飞行
- 正方形轨迹、路径规划与避障仿真
- MAVLink 数据监控与飞行日志分析

## 技术栈
- 系统：Ubuntu 20.04
- 飞控：PX4 1.14
- 仿真：Gazebo 11
- 开发语言：Python
- 通信：MAVLink、MAVSDK
- 算法：PID、MPC、路径规划

## 项目亮点
- 完整无人机仿真开发流程
- 控制算法验证与参数调优实践
- 可直接复现的仿真与控制脚本

## 运行环境
Ubuntu 20.04
PX4-Autopilot 1.14
Gazebo 11
Python 3.8+

## 成果展示
1.square.py
<img width="1106" height="590" alt="图片" src="https://github.com/user-attachments/assets/e0d02542-ae75-4bcf-8c6e-96b53d8402f9" />
2.规划与飞行

<img width="1106" height="1149" alt="图片" src="https://github.com/user-attachments/assets/b728df0e-5bb6-40ee-bd23-4fd2f54e7bfc" />

3.PID+A*静态避障飞行
<img width="1107" height="708" alt="图片" src="https://github.com/user-attachments/assets/4977840a-7a8c-4675-bdc1-8a5e0cb46a1d" />
3.MPC循迹飞行

<img width="1960" height="1130" alt="2026-03-30 13-14-27 的屏幕截图" src="https://github.com/user-attachments/assets/93aba499-fe3f-46ae-be95-3f28564e5d03" />

