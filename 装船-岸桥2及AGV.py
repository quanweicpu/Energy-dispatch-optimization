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
    (261.4, 1.5, 25.0),
    (266.0, 1.5, 25.0),
    (269.9, 1.5, 25.0),
    (275.0, 1.5, 25.0),
    (278.1, 1.5, 25.0),
    (282.5, 1.5, 25.0),
    (284.8, 1.5, 25.0),
    (290.6, 1.5, 25.0),
    (293.0, 1.5, 25.0),
    (297.8, 1.5, 25.0),
    (302.1, 1.5, 25.0),
    (306.5, 1.5, 25.0),
    (309.5, 1.5, 25.0),
    (314.0, 1.5, 25.0),
    (318.5, 1.5, 25.0),
    (321.3, 1.5, 25.0),
    (325.1, 1.5, 25.0),
    (328.9, 1.5, 25.0),
    (333.6, 1.5, 25.0),
    (337.2, 1.5, 25.0),
    (342.8, 1.5, 25.0),
    (346.6, 1.5, 25.0),
    (350.5, 1.5, 25.0),
    (354.5, 1.5, 25.0),
    (357.2, 1.5, 25.0),
    (362.8, 1.5, 25.0),
    (366.9, 1.5, 25.0),
    (371.0, 1.5, 25.0),
    (374.9, 1.5, 25.0),
    (377.2, 1.5, 25.0),
    (382.0, 1.5, 25.0),
    (386.1, 1.5, 25.0),
    (390.6, 1.5, 25.0),
    (392.6, 1.5, 25.0),
    (398.2, 1.5, 25.0),
    (402.9, 1.5, 25.0),
    (405.9, 1.5, 25.0),
    (409.8, 1.5, 25.0),
    (412.5, 1.5, 25.0),
    (418.8, 1.5, 25.0),
    (422.6, 1.5, 25.0),
    (426.7, 1.5, 25.0),
    (429.0, 1.5, 25.0),
    (433.6, 1.5, 25.0),
    (437.8, 1.5, 25.0),
    (442.6, 1.5, 25.0),
    (444.7, 1.5, 25.0),
    (450.5, 1.5, 25.0),
    (260.6, 15.5, 27.6),
    (266.2, 15.5, 27.6),
    (269.0, 15.5, 27.6),
    (273.3, 15.5, 27.6),
    (278.5, 15.5, 27.6),
    (282.5, 15.5, 27.6),
    (285.3, 15.5, 27.6),
    (289.7, 15.5, 27.6),
    (294.0, 15.5, 27.6),
    (297.1, 15.5, 27.6),
    (300.6, 15.5, 27.6),
    (304.6, 15.5, 27.6),
    (310.2, 15.5, 27.6),
    (313.1, 15.5, 27.6),
    (316.5, 15.5, 27.6),
    (322.6, 15.5, 27.6),
    (326.5, 15.5, 27.6),
    (330.2, 15.5, 27.6),
    (334.5, 15.5, 27.6),
    (338.8, 15.5, 27.6),
    (342.7, 15.5, 27.6),
    (345.4, 15.5, 27.6),
    (350.8, 15.5, 27.6),
    (353.1, 15.5, 27.6),
    (358.2, 15.5, 27.6),
    (361.5, 15.5, 27.6),
    (365.8, 15.5, 27.6),
    (370.0, 15.5, 27.6),
    (374.1, 15.5, 27.6),
    (378.3, 15.5, 27.6),
    (383.0, 15.5, 27.6),
    (385.0, 15.5, 27.6),
    (390.6, 15.5, 27.6),
    (392.6, 15.5, 27.6),
    (397.7, 15.5, 27.6),
    (401.0, 15.5, 27.6),
    (404.6, 15.5, 27.6),
    (408.7, 15.5, 27.6),
    (413.3, 15.5, 27.6),
    (417.6, 15.5, 27.6),
    (421.8, 15.5, 27.6),
    (425.8, 15.5, 27.6),
    (430.5, 15.5, 27.6),
    (433.9, 15.5, 27.6),
    (437.4, 15.5, 27.6),
    (441.1, 15.5, 27.6),
    (446.0, 15.5, 27.6),
    (451.0, 15.5, 27.6),
    (261.4, 29.5, 30.2),
    (265.7, 29.5, 30.2),
    (270.8, 29.5, 30.2),
    (274.1, 29.5, 30.2),
    (277.7, 29.5, 30.2),
    (282.3, 29.5, 30.2),
    (286.3, 29.5, 30.2),
    (289.9, 29.5, 30.2),
    (292.8, 29.5, 30.2),
    (297.6, 29.5, 30.2),
    (302.5, 29.5, 30.2),
    (306.0, 29.5, 30.2),
    (310.8, 29.5, 30.2),
    (314.9, 29.5, 30.2),
    (317.3, 29.5, 30.2),
    (322.7, 29.5, 30.2),
    (325.1, 29.5, 30.2),
    (330.5, 29.5, 30.2),
    (334.9, 29.5, 30.2),
    (337.5, 29.5, 30.2),
    (340.6, 29.5, 30.2),
    (346.3, 29.5, 30.2),
    (350.1, 29.5, 30.2),
    (353.6, 29.5, 30.2),
    (358.9, 29.5, 30.2),
    (360.8, 29.5, 30.2),
    (366.9, 29.5, 30.2),
    (370.1, 29.5, 30.2),
    (373.7, 29.5, 30.2),
    (378.8, 29.5, 30.2),
    (382.6, 29.5, 30.2),
    (386.4, 29.5, 30.2),
    (390.6, 29.5, 30.2),
    (393.2, 29.5, 30.2),
    (398.1, 29.5, 30.2),
    (401.3, 29.5, 30.2),
    (404.6, 29.5, 30.2),
    (410.1, 29.5, 30.2),
    (414.3, 29.5, 30.2),
    (417.8, 29.5, 30.2),
    (421.8, 29.5, 30.2),
    (425.0, 29.5, 30.2),
    (430.8, 29.5, 30.2),
    (433.0, 29.5, 30.2),
    (438.9, 29.5, 30.2),
    (440.8, 29.5, 30.2),
    (446.5, 29.5, 30.2),
    (262.6, 43.5, 32.8),
    (266.2, 43.5, 32.8),
    (269.3, 43.5, 32.8),
    (274.0, 43.5, 32.8),
    (277.4, 43.5, 32.8),
    (282.5, 43.5, 32.8),
    (286.3, 43.5, 32.8),
    (289.3, 43.5, 32.8),
    (292.7, 43.5, 32.8),
    (298.1, 43.5, 32.8),
    (302.6, 43.5, 32.8),
    (306.4, 43.5, 32.8),
    (309.4, 43.5, 32.8),
    (313.8, 43.5, 32.8),
    (316.9, 43.5, 32.8),
    (322.4, 43.5, 32.8),
    (325.0, 43.5, 32.8),
    (329.3, 43.5, 32.8),
    (333.7, 43.5, 32.8),
    (338.3, 43.5, 32.8),
    (341.2, 43.5, 32.8),
    (346.0, 43.5, 32.8),
    (348.5, 43.5, 32.8),
    (353.7, 43.5, 32.8),
    (358.5, 43.5, 32.8),
    (362.3, 43.5, 32.8),
    (366.4, 43.5, 32.8),
    (369.7, 43.5, 32.8),
    (374.5, 43.5, 32.8),
    (377.8, 43.5, 32.8),
    (381.5, 43.5, 32.8),
    (385.8, 43.5, 32.8),
    (390.4, 43.5, 32.8),
    (393.9, 43.5, 32.8),
    (397.9, 43.5, 32.8),
    (400.7, 43.5, 32.8),
    (405.1, 43.5, 32.8),
    (410.5, 43.5, 32.8),
    (414.6, 43.5, 32.8),
    (417.4, 43.5, 32.8),
    (422.3, 43.5, 32.8),
    (424.6, 43.5, 32.8),
    (430.0, 43.5, 32.8),
    (432.9, 43.5, 32.8),
    (437.1, 43.5, 32.8),
    (441.7, 43.5, 32.8),
    (261.6, 57.5, 35.4),
    (265.7, 57.5, 35.4),
    (269.7, 57.5, 35.4),
    (274.5, 57.5, 35.4),
    (278.9, 57.5, 35.4),
    (280.7, 57.5, 35.4),
    (285.1, 57.5, 35.4),
    (289.8, 57.5, 35.4),
    (294.3, 57.5, 35.4),
    (297.5, 57.5, 35.4),
    (302.9, 57.5, 35.4),
    (306.7, 57.5, 35.4),
    (310.3, 57.5, 35.4),
    (314.8, 57.5, 35.4),
    (318.7, 57.5, 35.4),
    (321.9, 57.5, 35.4),
    (325.3, 57.5, 35.4),
    (330.0, 57.5, 35.4),
    (333.1, 57.5, 35.4),
    (337.7, 57.5, 35.4),
    (340.6, 57.5, 35.4),
    (345.0, 57.5, 35.4),
    (350.4, 57.5, 35.4),
    (354.5, 57.5, 35.4),
    (357.8, 57.5, 35.4),
    (362.2, 57.5, 35.4),
    (365.7, 57.5, 35.4),
    (370.6, 57.5, 35.4),
    (374.2, 57.5, 35.4),
    (376.8, 57.5, 35.4),
    (382.6, 57.5, 35.4),
    (385.8, 57.5, 35.4),
    (388.6, 57.5, 35.4),
    (394.4, 57.5, 35.4),
    (398.8, 57.5, 35.4),
    (401.6, 57.5, 35.4),
    (404.8, 57.5, 35.4),
    (408.9, 57.5, 35.4),
    (414.5, 57.5, 35.4),
    (417.3, 57.5, 35.4),
    (421.1, 57.5, 35.4),
    (426.3, 57.5, 35.4),
    (430.8, 57.5, 35.4),
    (433.4, 57.5, 35.4),
    (437.3, 57.5, 35.4),
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
    (0, 275),
    (0, 325),
    (0, 225),
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

        # 第一步：计算岸桥贝位移动时间和能耗
        if previous_y is not None:
            # 计算当前y坐标与上一个y坐标的差值
            difference = abs(y_unload - previous_y)
            if difference != 0:
                t_qc_move = abs(difference) / v_qc_move  # 单位：秒
                energy_qc_move = P_qc_move * (t_qc_move / 3600)  # 单位：千瓦时
                total_energy_kWh += energy_qc_move
                total_time_s += t_qc_move
                total_energies_kWh.append(energy_qc_move)
                total_times_s.append(t_qc_move)
                # 打印调试信息（可选）
            # print(f"当工作下个箱子需要调整岸桥y轴上的距离：{difference}m")
            # print(f"计算岸桥贝位移动时间：{t_qc_move:.2f} 秒，能耗：{energy_qc_move:.2f} 千瓦时")

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

        # 第六步：计算小车空载上行时间和能耗
        t_s_up2 = z_initial / v_z_unload_up  # 单位：秒
        energy_up2_kWh = P_up_unload_kW * (t_s_up2 / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_up2_kWh)
        total_times_s.append(t_s_up2)

        # agv送集装箱场桥
        quay_crane_index = s % 3  # 使用取模来选择岸桥
        yard_crane_index = s % len(yard_crane_positions)  # 使用取模来选择场桥

        quay_crane_pos = unload_positions[quay_crane_index]
        yard_crane_pos = yard_crane_positions[yard_crane_index]

        # agv从等待区到场桥的距离和时间
        distance_to_yc = calculate_distance(yard_crane_pos, agvWait)
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

        # 第七步：计算小车空载水平移动时间和能耗
        t_s_move = L_m / v_x_unloaded  # 单位：秒
        energy_move1_kWh = P_x_unloaded_kW * (t_s_move / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_move1_kWh + energy_agv5 + energy_agv4 + e_to_yc + e_to_yc2)
        total_times_s.append(t_s_move)
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
        print(f"第一步（岸桥贝位移动）时间：{t_qc_move:.2f} 秒，能耗：{energy_qc_move:.2f} 千瓦时")
        print(f"第二步（小车下行抓箱子）时间：{t_s_down:.2f} 秒，能耗：{energy_down_kWh:.2f} 千瓦时")
        print(f"第三步（小车抓箱子后上行）时间：{t_s_up:.2f} 秒，能耗：{energy_up_kWh:.2f} 千瓦时")
        print(f"第四步（小车载货水平移动）时间：{t_s_move2:.2f} 秒，能耗：{energy_move2_kWh:.2f} 千瓦时")
        print(f"第五步（小车抓箱子后下行）时间：{t_s_down2:.2f} 秒，能耗：{energy_down2_kWh:.2f} 千瓦时")
        print(f"第六步（小车空载上行）时间：{t_s_up2:.2f} 秒，能耗：{energy_up2_kWh:.2f} 千瓦时")
        print(f"第七步（小车空载水平移动）：{t_s_move:.2f} 秒，能耗：{energy_move1_kWh:.2f} 千瓦时")
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
elements_per_column = 10
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
df.to_excel('岸桥2及AGV能耗2.xlsx', index=False, engine='openpyxl')