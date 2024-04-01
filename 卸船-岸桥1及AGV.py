import math
import itertools
import time
import random
import pandas as pd
import csv
from itertools import zip_longest

# 假设岸桥上小车初始位置是轨道的最右端，并具有一定的z坐标
x_right = 200  # 岸桥上轨道最右端的x坐标
z_initial = 55  # 小车初始z坐标

# 小车移动速度（假设为恒定速度）
v_x_loaded = 5  # 满载时小车在x轴上的移动速度，单位：米/秒
v_x_unloaded = 5  # 空载时小车在x轴上的移动速度，单位：米/秒
v_z_load_down = 1.25  # 小车满载下行的速度，单位：米/秒
v_z_unload_down = 3  # 小车空载下行的速度，单位：米/秒
v_z_load_up = 1.25  # 小车满载上行的速度，单位：米/秒
v_z_unload_up = 3  # 小车满载上行的速度，单位：米/秒
v_qc_move = 0.75  # 岸桥做贝位移动，单位：米/秒

# 功率值
P_x_loaded_kW = 244.8  # 满载时岸桥小车功率，单位：千瓦（移动箱子）
P_x_unloaded_kW = 228  # 空载时岸桥小车功率，单位：千瓦（移动箱子）
P_down_load_kW = 244.8  # 小车下行满载功率，单位：千瓦
P_down_unloaded_kW = 228  # 小车下行空载功率，单位：千瓦
P_up_load_kW = 244.8  # 小车上行满载功率，单位：千瓦
P_up_unload_kW = 228  # 小车上行空载功率，单位：千瓦
P_qc_move = 228  # 岸桥空载做贝位移动，单位：千瓦
agvWait = (0, 0, 0)
# 功率值
P_AGV_UNLOAD = 3.1  # AGV空载功率
P_AGV_LOAD = 3.3  # AGV满载功率
P_AGV_RELAX = 1
# 由集装箱随机生成.py生成，包含多个集装箱的空间坐标
unload_positions = [
    (258.6, 0.5, 25.0),
    (261.9, 0.5, 25.0),
    (266.7, 0.5, 25.0),
    (268.6, 0.5, 25.0),
    (271.4, 0.5, 25.0),
    (275.4, 0.5, 25.0),
    (277.2, 0.5, 25.0),
    (281.3, 0.5, 25.0),
    (283.3, 0.5, 25.0),
    (286.1, 0.5, 25.0),
    (289.7, 0.5, 25.0),
    (294.0, 0.5, 25.0),
    (295.1, 0.5, 25.0),
    (297.5, 0.5, 25.0),
    (302.7, 0.5, 25.0),
    (305.2, 0.5, 25.0),
    (308.4, 0.5, 25.0),
    (311.4, 0.5, 25.0),
    (313.1, 0.5, 25.0),
    (316.6, 0.5, 25.0),
    (319.5, 0.5, 25.0),
    (322.7, 0.5, 25.0),
    (325.0, 0.5, 25.0),
    (329.9, 0.5, 25.0),
    (332.0, 0.5, 25.0),
    (335.2, 0.5, 25.0),
    (336.7, 0.5, 25.0),
    (339.7, 0.5, 25.0),
    (344.6, 0.5, 25.0),
    (347.7, 0.5, 25.0),
    (349.1, 0.5, 25.0),
    (353.8, 0.5, 25.0),
    (355.9, 0.5, 25.0),
    (358.9, 0.5, 25.0),
    (361.7, 0.5, 25.0),
    (364.0, 0.5, 25.0),
    (369.0, 0.5, 25.0),
    (370.0, 0.5, 25.0),
    (373.5, 0.5, 25.0),
    (377.4, 0.5, 25.0),
    (380.9, 0.5, 25.0),
    (382.6, 0.5, 25.0),
    (385.8, 0.5, 25.0),
    (388.6, 0.5, 25.0),
    (392.5, 0.5, 25.0),
    (394.2, 0.5, 25.0),
    (396.9, 0.5, 25.0),
    (400.8, 0.5, 25.0),
    (402.8, 0.5, 25.0),
    (406.2, 0.5, 25.0),
    (410.2, 0.5, 25.0),
    (413.1, 0.5, 25.0),
    (417.0, 0.5, 25.0),
    (419.7, 0.5, 25.0),
    (421.5, 0.5, 25.0),
    (424.4, 0.5, 25.0),
    (427.1, 0.5, 25.0),
    (431.9, 0.5, 25.0),
    (433.7, 0.5, 25.0),
    (436.0, 0.5, 25.0),
    (440.4, 0.5, 25.0),
    (442.9, 0.5, 25.0),
    (445.6, 0.5, 25.0),
    (448.4, 0.5, 25.0),
    (450.8, 0.5, 25.0),
    (453.6, 0.5, 25.0),
    (259.9, 13.5, 27.6),
    (262.8, 13.5, 27.6),
    (264.6, 13.5, 27.6),
    (269.4, 13.5, 27.6),
    (272.6, 13.5, 27.6),
    (275.4, 13.5, 27.6),
    (278.6, 13.5, 27.6),
    (280.5, 13.5, 27.6),
    (282.5, 13.5, 27.6),
    (286.5, 13.5, 27.6),
    (289.3, 13.5, 27.6),
    (293.4, 13.5, 27.6),
    (294.9, 13.5, 27.6),
    (298.4, 13.5, 27.6),
    (302.3, 13.5, 27.6),
    (303.6, 13.5, 27.6),
    (308.6, 13.5, 27.6),
    (312.0, 13.5, 27.6),
    (312.8, 13.5, 27.6),
    (315.7, 13.5, 27.6),
    (319.7, 13.5, 27.6),
    (322.1, 13.5, 27.6),
    (325.5, 13.5, 27.6),
    (329.9, 13.5, 27.6),
    (331.9, 13.5, 27.6),
    (334.8, 13.5, 27.6),
    (337.9, 13.5, 27.6),
    (341.4, 13.5, 27.6),
    (343.0, 13.5, 27.6),
    (347.6, 13.5, 27.6),
    (350.6, 13.5, 27.6),
    (353.5, 13.5, 27.6),
    (355.3, 13.5, 27.6),
    (357.9, 13.5, 27.6),
    (361.6, 13.5, 27.6),
    (365.8, 13.5, 27.6),
    (366.9, 13.5, 27.6),
    (371.7, 13.5, 27.6),
    (373.6, 13.5, 27.6),
    (375.9, 13.5, 27.6),
    (380.5, 13.5, 27.6),
    (383.1, 13.5, 27.6),
    (385.8, 13.5, 27.6),
    (387.7, 13.5, 27.6),
    (391.8, 13.5, 27.6),
    (393.8, 13.5, 27.6),
    (397.0, 13.5, 27.6),
    (400.2, 13.5, 27.6),
    (403.5, 13.5, 27.6),
    (406.6, 13.5, 27.6),
    (410.0, 13.5, 27.6),
    (412.6, 13.5, 27.6),
    (416.4, 13.5, 27.6),
    (419.7, 13.5, 27.6),
    (422.6, 13.5, 27.6),
    (423.6, 13.5, 27.6),
    (427.2, 13.5, 27.6),
    (429.7, 13.5, 27.6),
    (433.7, 13.5, 27.6),
    (436.4, 13.5, 27.6),
    (440.7, 13.5, 27.6),
    (443.7, 13.5, 27.6),
    (445.4, 13.5, 27.6),
    (449.6, 13.5, 27.6),
    (452.5, 13.5, 27.6),
    (453.9, 13.5, 27.6),
    (260.7, 26.5, 30.2),
    (263.4, 26.5, 30.2),
    (266.8, 26.5, 30.2),
    (268.9, 26.5, 30.2),
    (270.6, 26.5, 30.2),
    (274.4, 26.5, 30.2),
    (276.7, 26.5, 30.2),
    (280.9, 26.5, 30.2),
    (284.9, 26.5, 30.2),
    (286.8, 26.5, 30.2),
    (289.3, 26.5, 30.2),
    (293.5, 26.5, 30.2),
    (294.7, 26.5, 30.2),
    (299.3, 26.5, 30.2),
    (301.6, 26.5, 30.2),
    (305.6, 26.5, 30.2),
    (307.6, 26.5, 30.2),
    (309.9, 26.5, 30.2),
    (313.2, 26.5, 30.2),
    (316.1, 26.5, 30.2),
    (319.5, 26.5, 30.2),
    (322.6, 26.5, 30.2),
    (324.7, 26.5, 30.2),
    (327.5, 26.5, 30.2),
    (331.1, 26.5, 30.2),
    (334.3, 26.5, 30.2),
    (337.0, 26.5, 30.2),
    (341.8, 26.5, 30.2),
    (343.4, 26.5, 30.2),
    (346.9, 26.5, 30.2),
    (349.7, 26.5, 30.2),
    (353.9, 26.5, 30.2),
    (356.8, 26.5, 30.2),
    (357.5, 26.5, 30.2),
    (361.7, 26.5, 30.2),
    (364.2, 26.5, 30.2),
    (367.7, 26.5, 30.2),
    (370.6, 26.5, 30.2),
    (374.7, 26.5, 30.2),
    (376.4, 26.5, 30.2),
    (379.9, 26.5, 30.2),
    (382.9, 26.5, 30.2),
    (386.1, 26.5, 30.2),
    (389.0, 26.5, 30.2),
    (391.0, 26.5, 30.2),
    (394.7, 26.5, 30.2),
    (397.2, 26.5, 30.2),
    (399.9, 26.5, 30.2),
    (404.9, 26.5, 30.2),
    (407.3, 26.5, 30.2),
    (409.9, 26.5, 30.2),
    (411.5, 26.5, 30.2),
    (415.0, 26.5, 30.2),
    (420.0, 26.5, 30.2),
    (422.8, 26.5, 30.2),
    (424.9, 26.5, 30.2),
    (427.4, 26.5, 30.2),
    (430.2, 26.5, 30.2),
    (432.8, 26.5, 30.2),
    (436.3, 26.5, 30.2),
    (438.7, 26.5, 30.2),
    (443.6, 26.5, 30.2),
    (447.0, 26.5, 30.2),
    (447.9, 26.5, 30.2),
    (452.4, 26.5, 30.2),
    (454.2, 26.5, 30.2),
    (260.9, 39.5, 32.8),
    (262.3, 39.5, 32.8),
    (266.9, 39.5, 32.8),
    (269.5, 39.5, 32.8),
    (270.6, 39.5, 32.8),
    (275.4, 39.5, 32.8),
    (277.6, 39.5, 32.8),
    (281.7, 39.5, 32.8),
    (284.0, 39.5, 32.8),
    (287.4, 39.5, 32.8),
    (288.7, 39.5, 32.8),
    (293.0, 39.5, 32.8),
    (296.5, 39.5, 32.8),
    (299.3, 39.5, 32.8),
    (301.3, 39.5, 32.8),
    (305.5, 39.5, 32.8),
    (308.2, 39.5, 32.8),
    (310.2, 39.5, 32.8),
    (313.3, 39.5, 32.8),
    (316.3, 39.5, 32.8),
    (320.8, 39.5, 32.8),
    (323.8, 39.5, 32.8),
    (324.6, 39.5, 32.8),
    (330.0, 39.5, 32.8),
    (330.6, 39.5, 32.8),
    (334.6, 39.5, 32.8),
    (337.7, 39.5, 32.8),
    (340.9, 39.5, 32.8),
    (344.3, 39.5, 32.8),
    (346.8, 39.5, 32.8),
    (348.9, 39.5, 32.8),
    (352.7, 39.5, 32.8),
    (355.2, 39.5, 32.8),
    (359.3, 39.5, 32.8),
    (362.1, 39.5, 32.8),
    (364.4, 39.5, 32.8),
    (368.9, 39.5, 32.8),
    (370.8, 39.5, 32.8),
    (372.7, 39.5, 32.8),
    (377.3, 39.5, 32.8),
    (379.0, 39.5, 32.8),
    (383.6, 39.5, 32.8),
    (386.5, 39.5, 32.8),
    (389.8, 39.5, 32.8),
    (392.0, 39.5, 32.8),
    (396.0, 39.5, 32.8),
    (397.8, 39.5, 32.8),
    (400.0, 39.5, 32.8),
    (402.8, 39.5, 32.8),
    (407.3, 39.5, 32.8),
    (409.5, 39.5, 32.8),
    (413.4, 39.5, 32.8),
    (416.3, 39.5, 32.8),
    (417.8, 39.5, 32.8),
    (421.5, 39.5, 32.8),
    (424.6, 39.5, 32.8),
    (428.5, 39.5, 32.8),
    (431.7, 39.5, 32.8),
    (434.2, 39.5, 32.8),
    (437.4, 39.5, 32.8),
    (440.3, 39.5, 32.8),
    (441.6, 39.5, 32.8),
    (447.0, 39.5, 32.8),
    (448.0, 39.5, 32.8),
    (452.0, 39.5, 32.8),
    (260.4, 52.5, 35.4),
    (263.3, 52.5, 35.4),
    (265.8, 52.5, 35.4),
    (269.4, 52.5, 35.4),
    (272.1, 52.5, 35.4),
    (274.6, 52.5, 35.4),
    (278.6, 52.5, 35.4),
    (281.9, 52.5, 35.4),
    (283.5, 52.5, 35.4),
    (286.4, 52.5, 35.4),
    (289.7, 52.5, 35.4),
    (293.2, 52.5, 35.4),
    (296.4, 52.5, 35.4),
    (298.7, 52.5, 35.4),
    (302.3, 52.5, 35.4),
    (305.2, 52.5, 35.4),
    (307.7, 52.5, 35.4),
    (310.2, 52.5, 35.4),
    (314.0, 52.5, 35.4),
    (316.5, 52.5, 35.4),
    (320.5, 52.5, 35.4),
    (323.8, 52.5, 35.4),
    (326.3, 52.5, 35.4),
    (329.5, 52.5, 35.4),
    (331.5, 52.5, 35.4),
    (334.0, 52.5, 35.4),
    (338.3, 52.5, 35.4),
    (339.7, 52.5, 35.4),
    (342.7, 52.5, 35.4),
    (346.7, 52.5, 35.4),
    (348.7, 52.5, 35.4),
    (352.1, 52.5, 35.4),
    (354.7, 52.5, 35.4),
    (357.6, 52.5, 35.4),
    (360.5, 52.5, 35.4),
    (364.5, 52.5, 35.4),
    (366.9, 52.5, 35.4),
    (371.2, 52.5, 35.4),
    (374.2, 52.5, 35.4),
    (377.6, 52.5, 35.4),
    (380.6, 52.5, 35.4),
    (383.9, 52.5, 35.4),
    (386.2, 52.5, 35.4),
    (388.1, 52.5, 35.4),
    (391.3, 52.5, 35.4),
    (393.8, 52.5, 35.4),
    (396.8, 52.5, 35.4),
    (401.0, 52.5, 35.4),
    (404.5, 52.5, 35.4),
    (406.5, 52.5, 35.4),
    (408.7, 52.5, 35.4),
    (413.5, 52.5, 35.4),
    (415.3, 52.5, 35.4),
    (417.9, 52.5, 35.4),
    (422.9, 52.5, 35.4),
    (425.7, 52.5, 35.4),
    (428.3, 52.5, 35.4),
    (431.7, 52.5, 35.4),
    (434.2, 52.5, 35.4),
    (437.1, 52.5, 35.4),
]

data_list = []  # excel输出


# 生成器函数，用于产生指定数量的随机排列，每个排列内部按 z 值降序排列
def generate_random_permutations(positions, num_permutations):
    for _ in range(num_permutations):
        # 创建当前 positions 列表的一个副本，并随机打乱它的顺序
        shuffled_positions = positions.copy()
        random.shuffle(shuffled_positions)

        # 对打乱后的列表进行排序，按 z 值的降序排列
        shuffled_positions.sort(key=lambda pos: pos[2], reverse=True)

        # 产出排列
        yield shuffled_positions

    # 设置你想要生成的排列数量


num_permutations_to_generate = 100

total_time_agvstart = 0
# 记录岸桥贝位移动时间和能源
t_qc_move = 0
energy_qc_move = 0

# 初始化上一个y坐标的变量，用于操作两个箱子之间计算岸桥贝位移动
previous_y = None

# 记录循环开始的时间
start_time = time.time()

# 设置循环运行的时间限制（秒）
time_limit = 30000

#  初始化运行时间
elapsed_time = 0
total_energies_kWhs = []
total_times_ss = []
total_time_agvstarts = []
# 初始化计数器和循环条件
count = 0

# AGV 参数（这些参数应根据您的实际情况进行调整）
v_agv_unload = 5.55  # AGV空载移动速度 (m/s)
v_agv_load = 5.2  # AGV满载移动速度 (m/s)


# 计算两点之间的距离
def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


s = 0
yard_crane_positions = [
    (0, -75),
    (0, -125),
    (0, -175),
]  # 场桥位置列表

# 按生成的箱子顺序迭代器做方案循环
for permutation in generate_random_permutations(unload_positions, num_permutations_to_generate):
    order = list(permutation)  # 将元组转换为列表（这一步其实是不必要的，因为permutation已经是一个元组列表）
    # 打印当前岸桥工作方案
    print("----start------")
    print(f"第一个岸桥工作顺序：{order}")
    # 在循环体内增加计数器的值
    count += 1
    # 在每次外层循环开始时，初始化两个临时列表来存储本次循环的数据
    total_energies_kWh = []
    total_times_s = []
    energy_move1_kWh = 0
    energy_down_kWh = 0
    energy_up_kWh = 0
    energy_move2_kWh = 0
    energy_down2_kWh = 0
    energy_up2_kWh = 0
    t_s_down2 = 0
    t_s_move = 0
    t_s_up2 = 0
    t_s_down = 0
    t_qc_move = 0
    t_s_up = 0
    t_s_move2 = 0
    energy_qc_move = 0
    # 初始化总能耗和总时间
    total_energy_kWh = 0
    total_time_s = 0
    # 遍历每个需要卸载的箱子坐标
    for position in permutation:
        s += 1
        x_unload, y_unload, z_unload = position
        # 计算小车从初始位置到箱子位置的水平距离（假设只在x轴上移动）
        L_m = abs(x_right - x_unload)  # 单位：米

        # 第一步：计算水平移动时间和能耗
        t_s_move = L_m / v_x_unloaded  # 单位：秒
        energy_move1_kWh = P_x_unloaded_kW * (t_s_move / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_move1_kWh)
        total_times_s.append(t_s_move)

        # 第二步：计算小车下行抓箱子的时间和能耗
        z_distance = z_initial - z_unload  # 计算下行距离
        t_s_down = z_distance / v_z_unload_down  # 单位：秒
        energy_down_kWh = P_down_unloaded_kW * (t_s_down / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_down_kWh)
        total_times_s.append(t_s_down)

        # 第三步：计算小车抓箱子后上行的时间和能耗
        t_s_up = z_distance / v_z_unload_up  # 单位：秒
        energy_up_kWh = P_up_load_kW * (t_s_up / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_up_kWh)
        total_times_s.append(t_s_up)

        # 第四步：计算载货水平移动时间和能耗
        t_s_move2 = L_m / v_x_loaded  # 单位：秒
        energy_move2_kWh = P_x_loaded_kW * (t_s_move2 / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_move2_kWh)
        total_times_s.append(t_s_move2)

        # 第五步：计算小车抓箱子后下行的时间和能耗
        t_s_down2 = z_initial / v_z_load_down  # 单位：秒
        energy_down2_kWh = P_down_load_kW * (t_s_down2 / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_down2_kWh)
        total_times_s.append(t_s_down2)

        # 第六步：计算回归原位时间和能耗
        t_s_up2 = z_initial / v_z_unload_up  # 单位：秒
        energy_up2_kWh = P_up_unload_kW * (t_s_up2 / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_up2_kWh)
        total_times_s.append(t_s_up2)

        # agv送集装箱场桥
        quay_crane_index = s % 3  # 使用取模来选择岸桥
        yard_crane_index = s % len(yard_crane_positions)  # 使用取模来选择场桥

        quay_crane_pos = unload_positions[quay_crane_index]
        yard_crane_pos = yard_crane_positions[yard_crane_index]

        # agv从等待区到岸桥的距离和时间
        distance_to_yc = calculate_distance(quay_crane_pos, agvWait)
        time_to_yc2 = distance_to_yc / v_agv_unload
        e_to_yc2 = P_AGV_UNLOAD * (time_to_yc2 / 3600)  # 单位：千瓦时

        # 从岸桥到场桥的距离和时间
        distance_to_yc = calculate_distance(quay_crane_pos, yard_crane_pos)
        time_to_yc = distance_to_yc / v_agv_load
        e_to_yc = P_AGV_LOAD * (time_to_yc / 3600)  # 单位：千瓦时

        # 第九步：AGV等待场桥时间
        z_distance = 18
        t_s_down = z_distance / v_z_unload_down  # 单位：秒
        t_s_up = z_distance / v_z_load_up
        t4 = t_s_down + t_s_up
        energy_agv4 = P_AGV_RELAX * (t4 / 3600)

        # 第十步：AGV返回等待区时间
        L_v = calculate_distance(yard_crane_pos, agvWait)
        t5 = L_v / v_agv_unload
        energy_agv5 = P_AGV_UNLOAD * (t5 / 3600)  # 单位：千瓦时

        # 第七步：计算贝位移动时间和能耗
        if previous_y is not None:
            # 计算当前y坐标与上一个y坐标的差值
            difference = abs(y_unload - previous_y)
            if difference != 0:
                t_qc_move = abs(difference) / v_qc_move  # 单位：秒
                energy_qc_move = P_qc_move * (t_qc_move / 3600)  # 单位：千瓦时
                total_energy_kWh += energy_qc_move
                total_time_s += t_qc_move
                total_energies_kWh.append(energy_qc_move + e_to_yc + energy_agv4 + energy_agv5 + e_to_yc2)
                total_times_s.append(t_qc_move)
        # 更新上一个y坐标的值
        previous_y = y_unload
        total_energy_kWh += (energy_move1_kWh + energy_down_kWh + energy_up_kWh + energy_move2_kWh + energy_down2_kWh +
                             energy_up2_kWh + energy_qc_move)
        total_time_s += t_s_move + t_s_down + t_s_up + t_s_move2 + t_s_down2 + t_s_up2 + t_qc_move
        # 打印调试信息（可选）
        # print(f"当工作下个箱子需要调整岸桥y轴上的距离：{difference}m")
        # print(f"计算岸桥贝位移动时间：{t_qc_move:.2f} 秒，能耗：{energy_qc_move:.2f} 千瓦时")
        # 输出每一步的能耗和时间
        print(f"---当前工作箱子坐标：({x_unload}, {y_unload}, {z_unload})")
        print(f"第一步（岸桥小车向左水平移动）时间：{t_s_move:.2f} 秒，能耗：{energy_move1_kWh:.2f} 千瓦时")
        print(f"第二步（小车下行抓箱子）时间：{t_s_down:.2f} 秒，能耗：{energy_down_kWh:.2f} 千瓦时")
        print(f"第三步（小车载箱子上行）时间：{t_s_up:.2f} 秒，能耗：{energy_up_kWh:.2f} 千瓦时")
        print(f"第四步（岸桥小车向右水平移动）时间：{t_s_move:.2f} 秒，能耗：{energy_move2_kWh:.2f} 千瓦时")
        print(f"第五步（小车载箱子下行）时间：{t_s_down2:.2f} 秒，能耗：{energy_down2_kWh:.2f} 千瓦时")
        print(f"第六步（小车空载上行回归原位）时间：{t_s_up2:.2f} 秒，能耗：{energy_up2_kWh:.2f} 千瓦时")
        print(f"第七步（岸桥做贝位移动时间）：{t_qc_move:.2f} 秒，能耗：{energy_qc_move:.2f} 千瓦时")
    total_energies_kWhs.extend(total_energies_kWh)
    total_times_ss.extend(total_times_s)
    total_energies_kWh.clear()
    total_times_s.clear()
    # 初始化变量每60min
    total_time = 0.0  # 累计时间
    total_energy = 0.0  # 当前小时的能源总和
    print(f"----0-23个时间段，每个时间段的能耗----")
    # 遍历时间和能源列表
    for times, energy in zip(total_times_ss, total_energies_kWhs):
        # 累加时间
        total_time += times
        # 累加能源
        total_energy += energy
        # 检查是否达到或超过1小时（3600秒）
        if total_time >= 3600:
            # 输出当前小时的能源和
            print(f"------{total_energy:.2f}------")
            data_list.append(total_energy)
            # 重置时间和能源总和为剩余部分（如果有的话）
            remaining_time = total_time - math.floor(total_time / 3600) * 3600
            total_time = remaining_time
            total_energy = 0.0 if remaining_time == 0.0 else total_energies_kWhs[
                total_energies_kWhs.index(energy) + 1]  # 假设下一个能源值是当前小时剩余时间的能源

    if total_time > 0:
        print(f"未满1h部分: {total_energy}")
        data_list.append(total_energy)
    print(f"----岸桥小车卸载所有箱子所需的总能耗是：{total_energy_kWh:.2f} 千瓦时-----")
    print(f"----岸桥小车卸载所有箱子所需的总运输时间是：{total_time_s:.2f} 秒-----")
    print(f"----岸桥工作开始时间：{0}   岸桥工作结束时间：{total_time_s:.2f} 秒----")
    total_energies_kWhs.clear()
    total_times_ss.clear()
    # 检查是否已经超过了时间限制
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time >= time_limit:
        break  # 如果已经超过了时间限制，跳出循环
# 输出最终结果包含方案个数.运行时间.总能耗和总时间
print("循环已停止，代码总共运行了 {} 秒".format(elapsed_time))
print(f"-------------共有方案个数: {count} ---------------------------")
# -----------------打印---------------------------------
# 确定每列包含的元素数量
elements_per_column = 13
# 准备一个空的DataFrame
df = pd.DataFrame()
# 计算需要的列数
num_columns = len(data_list) // elements_per_column
# 遍历列表，将数据添加到DataFrame中
for i in range(num_columns):
    # 计算当前列在列表中的起始和结束索引
    start_index = i * elements_per_column
    end_index = start_index + elements_per_column

    # 提取当前列的数据
    column_data = data_list[start_index:end_index]

    # 如果当前列的数据长度不足12个，用None填充到12个
    if len(column_data) < elements_per_column:
        column_data.extend([None] * (elements_per_column - len(column_data)))

        # 将当前列的数据添加到DataFrame中
    df[f'方案{i + 1}'] = column_data

# 将DataFrame写入Excel文件
df.to_excel('岸桥1及AGV能耗.xlsx', index=False, engine='openpyxl')
