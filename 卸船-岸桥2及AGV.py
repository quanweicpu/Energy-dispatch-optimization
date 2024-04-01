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
    (258.9, 70.5, 25.0),
    (263.7, 70.5, 25.0),
    (266.8, 70.5, 25.0),
    (267.8, 70.5, 25.0),
    (272.4, 70.5, 25.0),
    (275.7, 70.5, 25.0),
    (276.5, 70.5, 25.0),
    (279.5, 70.5, 25.0),
    (284.7, 70.5, 25.0),
    (285.6, 70.5, 25.0),
    (290.4, 70.5, 25.0),
    (291.7, 70.5, 25.0),
    (295.1, 70.5, 25.0),
    (297.8, 70.5, 25.0),
    (302.0, 70.5, 25.0),
    (305.9, 70.5, 25.0),
    (307.2, 70.5, 25.0),
    (309.8, 70.5, 25.0),
    (313.6, 70.5, 25.0),
    (316.4, 70.5, 25.0),
    (318.8, 70.5, 25.0),
    (323.8, 70.5, 25.0),
    (325.8, 70.5, 25.0),
    (327.7, 70.5, 25.0),
    (332.4, 70.5, 25.0),
    (334.1, 70.5, 25.0),
    (337.3, 70.5, 25.0),
    (339.6, 70.5, 25.0),
    (344.2, 70.5, 25.0),
    (345.7, 70.5, 25.0),
    (348.6, 70.5, 25.0),
    (352.8, 70.5, 25.0),
    (355.5, 70.5, 25.0),
    (358.8, 70.5, 25.0),
    (361.6, 70.5, 25.0),
    (365.5, 70.5, 25.0),
    (367.0, 70.5, 25.0),
    (371.0, 70.5, 25.0),
    (374.8, 70.5, 25.0),
    (376.8, 70.5, 25.0),
    (379.6, 70.5, 25.0),
    (381.9, 70.5, 25.0),
    (386.1, 70.5, 25.0),
    (389.0, 70.5, 25.0),
    (391.5, 70.5, 25.0),
    (394.5, 70.5, 25.0),
    (397.0, 70.5, 25.0),
    (400.2, 70.5, 25.0),
    (404.0, 70.5, 25.0),
    (405.6, 70.5, 25.0),
    (410.7, 70.5, 25.0),
    (411.7, 70.5, 25.0),
    (416.1, 70.5, 25.0),
    (419.8, 70.5, 25.0),
    (422.4, 70.5, 25.0),
    (424.1, 70.5, 25.0),
    (428.5, 70.5, 25.0),
    (430.7, 70.5, 25.0),
    (434.6, 70.5, 25.0),
    (436.1, 70.5, 25.0),
    (439.6, 70.5, 25.0),
    (442.8, 70.5, 25.0),
    (446.9, 70.5, 25.0),
    (448.1, 70.5, 25.0),
    (451.6, 70.5, 25.0),
    (454.3, 70.5, 25.0),
    (258.6, 83.5, 27.6),
    (261.9, 83.5, 27.6),
    (265.7, 83.5, 27.6),
    (269.0, 83.5, 27.6),
    (271.2, 83.5, 27.6),
    (275.1, 83.5, 27.6),
    (278.4, 83.5, 27.6),
    (281.1, 83.5, 27.6),
    (283.0, 83.5, 27.6),
    (286.1, 83.5, 27.6),
    (288.8, 83.5, 27.6),
    (293.0, 83.5, 27.6),
    (295.9, 83.5, 27.6),
    (299.5, 83.5, 27.6),
    (300.8, 83.5, 27.6),
    (304.5, 83.5, 27.6),
    (307.7, 83.5, 27.6),
    (311.6, 83.5, 27.6),
    (313.2, 83.5, 27.6),
    (317.1, 83.5, 27.6),
    (320.7, 83.5, 27.6),
    (322.0, 83.5, 27.6),
    (325.2, 83.5, 27.6),
    (328.2, 83.5, 27.6),
    (330.8, 83.5, 27.6),
    (334.8, 83.5, 27.6),
    (338.4, 83.5, 27.6),
    (339.6, 83.5, 27.6),
    (343.1, 83.5, 27.6),
    (346.4, 83.5, 27.6),
    (350.9, 83.5, 27.6),
    (353.8, 83.5, 27.6),
    (356.9, 83.5, 27.6),
    (359.0, 83.5, 27.6),
    (360.9, 83.5, 27.6),
    (365.8, 83.5, 27.6),
    (368.0, 83.5, 27.6),
    (370.2, 83.5, 27.6),
    (373.7, 83.5, 27.6),
    (375.7, 83.5, 27.6),
    (379.5, 83.5, 27.6),
    (382.9, 83.5, 27.6),
    (385.5, 83.5, 27.6),
    (388.0, 83.5, 27.6),
    (391.1, 83.5, 27.6),
    (394.9, 83.5, 27.6),
    (396.8, 83.5, 27.6),
    (401.4, 83.5, 27.6),
    (404.8, 83.5, 27.6),
    (407.5, 83.5, 27.6),
    (410.9, 83.5, 27.6),
    (411.7, 83.5, 27.6),
    (416.7, 83.5, 27.6),
    (418.8, 83.5, 27.6),
    (422.3, 83.5, 27.6),
    (424.9, 83.5, 27.6),
    (427.2, 83.5, 27.6),
    (429.9, 83.5, 27.6),
    (432.9, 83.5, 27.6),
    (437.3, 83.5, 27.6),
    (440.8, 83.5, 27.6),
    (443.7, 83.5, 27.6),
    (445.9, 83.5, 27.6),
    (448.3, 83.5, 27.6),
    (451.0, 83.5, 27.6),
    (454.4, 83.5, 27.6),
    (259.4, 96.5, 30.2),
    (262.2, 96.5, 30.2),
    (266.4, 96.5, 30.2),
    (269.2, 96.5, 30.2),
    (272.6, 96.5, 30.2),
    (275.4, 96.5, 30.2),
    (277.6, 96.5, 30.2),
    (279.6, 96.5, 30.2),
    (284.7, 96.5, 30.2),
    (286.7, 96.5, 30.2),
    (289.3, 96.5, 30.2),
    (293.1, 96.5, 30.2),
    (296.6, 96.5, 30.2),
    (299.1, 96.5, 30.2),
    (302.4, 96.5, 30.2),
    (305.8, 96.5, 30.2),
    (308.6, 96.5, 30.2),
    (310.5, 96.5, 30.2),
    (314.2, 96.5, 30.2),
    (317.5, 96.5, 30.2),
    (320.6, 96.5, 30.2),
    (323.6, 96.5, 30.2),
    (325.3, 96.5, 30.2),
    (328.5, 96.5, 30.2),
    (331.9, 96.5, 30.2),
    (335.9, 96.5, 30.2),
    (337.4, 96.5, 30.2),
    (340.4, 96.5, 30.2),
    (344.1, 96.5, 30.2),
    (346.4, 96.5, 30.2),
    (350.3, 96.5, 30.2),
    (352.5, 96.5, 30.2),
    (356.4, 96.5, 30.2),
    (358.0, 96.5, 30.2),
    (361.8, 96.5, 30.2),
    (365.5, 96.5, 30.2),
    (367.6, 96.5, 30.2),
    (371.6, 96.5, 30.2),
    (375.0, 96.5, 30.2),
    (377.2, 96.5, 30.2),
    (379.8, 96.5, 30.2),
    (383.5, 96.5, 30.2),
    (386.1, 96.5, 30.2),
    (389.9, 96.5, 30.2),
    (390.9, 96.5, 30.2),
    (393.7, 96.5, 30.2),
    (398.0, 96.5, 30.2),
    (401.5, 96.5, 30.2),
    (404.1, 96.5, 30.2),
    (407.0, 96.5, 30.2),
    (408.6, 96.5, 30.2),
    (413.1, 96.5, 30.2),
    (416.0, 96.5, 30.2),
    (419.6, 96.5, 30.2),
    (422.3, 96.5, 30.2),
    (424.7, 96.5, 30.2),
    (427.2, 96.5, 30.2),
    (430.0, 96.5, 30.2),
    (434.1, 96.5, 30.2),
    (437.4, 96.5, 30.2),
    (439.6, 96.5, 30.2),
    (443.4, 96.5, 30.2),
    (446.8, 96.5, 30.2),
    (447.9, 96.5, 30.2),
    (451.0, 96.5, 30.2),
    (454.3, 96.5, 30.2),
    (259.8, 109.5, 32.8),
    (261.8, 109.5, 32.8),
    (266.8, 109.5, 32.8),
    (268.2, 109.5, 32.8),
    (271.3, 109.5, 32.8),
    (275.5, 109.5, 32.8),
    (278.6, 109.5, 32.8),
    (280.1, 109.5, 32.8),
    (284.0, 109.5, 32.8),
    (286.5, 109.5, 32.8),
    (289.1, 109.5, 32.8),
    (293.9, 109.5, 32.8),
    (296.9, 109.5, 32.8),
    (298.1, 109.5, 32.8),
    (301.0, 109.5, 32.8),
    (304.4, 109.5, 32.8),
    (307.0, 109.5, 32.8),
    (311.1, 109.5, 32.8),
    (314.3, 109.5, 32.8),
    (315.7, 109.5, 32.8),
    (318.7, 109.5, 32.8),
    (323.5, 109.5, 32.8),
    (324.9, 109.5, 32.8),
    (328.1, 109.5, 32.8),
    (332.3, 109.5, 32.8),
    (333.9, 109.5, 32.8),
    (338.5, 109.5, 32.8),
    (339.8, 109.5, 32.8),
    (344.4, 109.5, 32.8),
    (345.7, 109.5, 32.8),
    (349.3, 109.5, 32.8),
    (352.3, 109.5, 32.8),
    (355.3, 109.5, 32.8),
    (358.9, 109.5, 32.8),
    (360.9, 109.5, 32.8),
    (363.7, 109.5, 32.8),
    (366.9, 109.5, 32.8),
    (371.2, 109.5, 32.8),
    (374.5, 109.5, 32.8),
    (376.5, 109.5, 32.8),
    (379.8, 109.5, 32.8),
    (382.7, 109.5, 32.8),
    (386.5, 109.5, 32.8),
    (387.9, 109.5, 32.8),
    (390.8, 109.5, 32.8),
    (393.9, 109.5, 32.8),
    (398.3, 109.5, 32.8),
    (401.9, 109.5, 32.8),
    (402.9, 109.5, 32.8),
    (406.4, 109.5, 32.8),
    (408.5, 109.5, 32.8),
    (413.1, 109.5, 32.8),
    (416.5, 109.5, 32.8),
    (417.8, 109.5, 32.8),
    (422.5, 109.5, 32.8),
    (425.5, 109.5, 32.8),
    (426.5, 109.5, 32.8),
    (431.9, 109.5, 32.8),
    (434.2, 109.5, 32.8),
    (435.9, 109.5, 32.8),
    (440.3, 109.5, 32.8),
    (443.8, 109.5, 32.8),
    (445.4, 109.5, 32.8),
    (449.6, 109.5, 32.8),
    (451.4, 109.5, 32.8),
    (259.1, 122.5, 35.4),
    (262.2, 122.5, 35.4),
    (265.2, 122.5, 35.4),
    (267.9, 122.5, 35.4),
    (272.4, 122.5, 35.4),
    (275.3, 122.5, 35.4),
    (276.6, 122.5, 35.4),
    (280.7, 122.5, 35.4),
    (282.8, 122.5, 35.4),
    (285.8, 122.5, 35.4),
    (290.5, 122.5, 35.4),
    (293.8, 122.5, 35.4),
    (296.2, 122.5, 35.4),
    (298.7, 122.5, 35.4),
    (302.0, 122.5, 35.4),
    (303.9, 122.5, 35.4),
    (306.7, 122.5, 35.4),
    (310.9, 122.5, 35.4),
    (312.6, 122.5, 35.4),
    (316.5, 122.5, 35.4),
    (320.9, 122.5, 35.4),
    (323.3, 122.5, 35.4),
    (327.0, 122.5, 35.4),
    (327.9, 122.5, 35.4),
    (331.1, 122.5, 35.4),
    (335.2, 122.5, 35.4),
    (337.8, 122.5, 35.4),
    (339.9, 122.5, 35.4),
    (343.2, 122.5, 35.4),
    (347.2, 122.5, 35.4),
    (349.7, 122.5, 35.4),
    (353.9, 122.5, 35.4),
    (354.8, 122.5, 35.4),
    (358.2, 122.5, 35.4),
    (363.0, 122.5, 35.4),
    (364.2, 122.5, 35.4),
    (367.6, 122.5, 35.4),
    (370.5, 122.5, 35.4),
    (374.3, 122.5, 35.4),
    (375.5, 122.5, 35.4),
    (380.2, 122.5, 35.4),
    (381.5, 122.5, 35.4),
    (386.9, 122.5, 35.4),
    (389.1, 122.5, 35.4),
    (392.0, 122.5, 35.4),
    (394.6, 122.5, 35.4),
    (397.8, 122.5, 35.4),
    (401.1, 122.5, 35.4),
    (403.9, 122.5, 35.4),
    (406.9, 122.5, 35.4),
    (409.8, 122.5, 35.4),
    (411.6, 122.5, 35.4),
    (414.6, 122.5, 35.4),
    (417.9, 122.5, 35.4),
    (422.6, 122.5, 35.4),
    (423.9, 122.5, 35.4),
    (426.6, 122.5, 35.4),
    (431.0, 122.5, 35.4),
    (434.4, 122.5, 35.4),
    (435.6, 122.5, 35.4),
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
    (0, -25),
    (0, -25),
    (0, 75),
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
df.to_excel('岸桥2及AGV能耗.xlsx', index=False, engine='openpyxl')