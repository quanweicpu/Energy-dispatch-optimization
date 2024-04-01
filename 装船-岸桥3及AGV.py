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
    (261.1, 71.5, 25.0),
    (265.7, 71.5, 25.0),
    (269.1, 71.5, 25.0),
    (274.6, 71.5, 25.0),
    (277.1, 71.5, 25.0),
    (282.1, 71.5, 25.0),
    (286.3, 71.5, 25.0),
    (288.9, 71.5, 25.0),
    (293.4, 71.5, 25.0),
    (297.9, 71.5, 25.0),
    (301.0, 71.5, 25.0),
    (305.9, 71.5, 25.0),
    (309.2, 71.5, 25.0),
    (314.0, 71.5, 25.0),
    (318.1, 71.5, 25.0),
    (321.2, 71.5, 25.0),
    (325.7, 71.5, 25.0),
    (330.4, 71.5, 25.0),
    (334.0, 71.5, 25.0),
    (337.7, 71.5, 25.0),
    (340.9, 71.5, 25.0),
    (345.7, 71.5, 25.0),
    (350.2, 71.5, 25.0),
    (354.7, 71.5, 25.0),
    (358.6, 71.5, 25.0),
    (362.6, 71.5, 25.0),
    (365.4, 71.5, 25.0),
    (369.1, 71.5, 25.0),
    (373.5, 71.5, 25.0),
    (376.7, 71.5, 25.0),
    (382.2, 71.5, 25.0),
    (385.8, 71.5, 25.0),
    (390.4, 71.5, 25.0),
    (393.4, 71.5, 25.0),
    (397.2, 71.5, 25.0),
    (400.9, 71.5, 25.0),
    (406.6, 71.5, 25.0),
    (408.6, 71.5, 25.0),
    (414.5, 71.5, 25.0),
    (417.3, 71.5, 25.0),
    (421.2, 71.5, 25.0),
    (425.2, 71.5, 25.0),
    (429.1, 71.5, 25.0),
    (434.8, 71.5, 25.0),
    (436.7, 71.5, 25.0),
    (440.8, 71.5, 25.0),
    (444.8, 71.5, 25.0),
    (449.9, 71.5, 25.0),
    (261.7, 85.5, 27.6),
    (265.4, 85.5, 27.6),
    (269.1, 85.5, 27.6),
    (274.7, 85.5, 27.6),
    (278.2, 85.5, 27.6),
    (282.1, 85.5, 27.6),
    (284.9, 85.5, 27.6),
    (289.1, 85.5, 27.6),
    (293.7, 85.5, 27.6),
    (298.7, 85.5, 27.6),
    (302.0, 85.5, 27.6),
    (306.0, 85.5, 27.6),
    (310.0, 85.5, 27.6),
    (314.0, 85.5, 27.6),
    (316.9, 85.5, 27.6),
    (322.3, 85.5, 27.6),
    (324.9, 85.5, 27.6),
    (329.2, 85.5, 27.6),
    (332.8, 85.5, 27.6),
    (338.5, 85.5, 27.6),
    (340.7, 85.5, 27.6),
    (344.7, 85.5, 27.6),
    (349.8, 85.5, 27.6),
    (354.7, 85.5, 27.6),
    (358.4, 85.5, 27.6),
    (362.9, 85.5, 27.6),
    (366.6, 85.5, 27.6),
    (369.9, 85.5, 27.6),
    (374.8, 85.5, 27.6),
    (377.3, 85.5, 27.6),
    (382.8, 85.5, 27.6),
    (385.0, 85.5, 27.6),
    (388.5, 85.5, 27.6),
    (392.5, 85.5, 27.6),
    (397.6, 85.5, 27.6),
    (401.6, 85.5, 27.6),
    (406.2, 85.5, 27.6),
    (410.9, 85.5, 27.6),
    (414.4, 85.5, 27.6),
    (418.5, 85.5, 27.6),
    (420.9, 85.5, 27.6),
    (426.8, 85.5, 27.6),
    (430.2, 85.5, 27.6),
    (433.9, 85.5, 27.6),
    (436.6, 85.5, 27.6),
    (440.6, 85.5, 27.6),
    (446.8, 85.5, 27.6),
    (449.9, 85.5, 27.6),
    (261.3, 99.5, 30.2),
    (265.0, 99.5, 30.2),
    (270.7, 99.5, 30.2),
    (273.5, 99.5, 30.2),
    (278.9, 99.5, 30.2),
    (281.6, 99.5, 30.2),
    (286.2, 99.5, 30.2),
    (288.9, 99.5, 30.2),
    (293.2, 99.5, 30.2),
    (298.6, 99.5, 30.2),
    (300.5, 99.5, 30.2),
    (306.4, 99.5, 30.2),
    (309.2, 99.5, 30.2),
    (314.4, 99.5, 30.2),
    (317.7, 99.5, 30.2),
    (321.1, 99.5, 30.2),
    (326.2, 99.5, 30.2),
    (328.5, 99.5, 30.2),
    (333.1, 99.5, 30.2),
    (337.0, 99.5, 30.2),
    (341.6, 99.5, 30.2),
    (345.2, 99.5, 30.2),
    (350.0, 99.5, 30.2),
    (353.6, 99.5, 30.2),
    (358.4, 99.5, 30.2),
    (362.6, 99.5, 30.2),
    (365.8, 99.5, 30.2),
    (369.3, 99.5, 30.2),
    (374.5, 99.5, 30.2),
    (378.9, 99.5, 30.2),
    (382.1, 99.5, 30.2),
    (385.1, 99.5, 30.2),
    (390.9, 99.5, 30.2),
    (393.0, 99.5, 30.2),
    (396.9, 99.5, 30.2),
    (401.2, 99.5, 30.2),
    (405.4, 99.5, 30.2),
    (410.5, 99.5, 30.2),
    (413.4, 99.5, 30.2),
    (416.7, 99.5, 30.2),
    (421.3, 99.5, 30.2),
    (424.7, 99.5, 30.2),
    (430.8, 99.5, 30.2),
    (433.8, 99.5, 30.2),
    (437.7, 99.5, 30.2),
    (441.1, 99.5, 30.2),
    (446.3, 99.5, 30.2),
    (260.6, 113.5, 32.8),
    (265.0, 113.5, 32.8),
    (270.3, 113.5, 32.8),
    (273.2, 113.5, 32.8),
    (276.7, 113.5, 32.8),
    (282.5, 113.5, 32.8),
    (284.9, 113.5, 32.8),
    (288.9, 113.5, 32.8),
    (293.7, 113.5, 32.8),
    (296.7, 113.5, 32.8),
    (302.8, 113.5, 32.8),
    (306.4, 113.5, 32.8),
    (309.9, 113.5, 32.8),
    (312.7, 113.5, 32.8),
    (318.2, 113.5, 32.8),
    (322.7, 113.5, 32.8),
    (325.3, 113.5, 32.8),
    (330.7, 113.5, 32.8),
    (334.8, 113.5, 32.8),
    (337.6, 113.5, 32.8),
    (342.6, 113.5, 32.8),
    (345.1, 113.5, 32.8),
    (349.7, 113.5, 32.8),
    (353.7, 113.5, 32.8),
    (358.2, 113.5, 32.8),
    (360.7, 113.5, 32.8),
    (366.3, 113.5, 32.8),
    (369.3, 113.5, 32.8),
    (374.7, 113.5, 32.8),
    (377.2, 113.5, 32.8),
    (380.9, 113.5, 32.8),
    (386.2, 113.5, 32.8),
    (390.3, 113.5, 32.8),
    (394.8, 113.5, 32.8),
    (398.0, 113.5, 32.8),
    (401.5, 113.5, 32.8),
    (405.1, 113.5, 32.8),
    (409.1, 113.5, 32.8),
    (414.2, 113.5, 32.8),
    (417.5, 113.5, 32.8),
    (421.2, 113.5, 32.8),
    (426.2, 113.5, 32.8),
    (428.9, 113.5, 32.8),
    (434.4, 113.5, 32.8),
    (438.7, 113.5, 32.8),
    (441.2, 113.5, 32.8),
    (262.0, 127.5, 35.4),
    (265.5, 127.5, 35.4),
    (270.7, 127.5, 35.4),
    (273.5, 127.5, 35.4),
    (278.4, 127.5, 35.4),
    (280.8, 127.5, 35.4),
    (286.4, 127.5, 35.4),
    (289.9, 127.5, 35.4),
    (292.9, 127.5, 35.4),
    (299.0, 127.5, 35.4),
    (301.5, 127.5, 35.4),
    (305.2, 127.5, 35.4),
    (309.9, 127.5, 35.4),
    (313.6, 127.5, 35.4),
    (316.5, 127.5, 35.4),
    (321.1, 127.5, 35.4),
    (325.3, 127.5, 35.4),
    (329.0, 127.5, 35.4),
    (333.8, 127.5, 35.4),
    (338.7, 127.5, 35.4),
    (342.6, 127.5, 35.4),
    (346.4, 127.5, 35.4),
    (350.9, 127.5, 35.4),
    (354.9, 127.5, 35.4),
    (357.0, 127.5, 35.4),
    (362.3, 127.5, 35.4),
    (364.6, 127.5, 35.4),
    (370.8, 127.5, 35.4),
    (372.9, 127.5, 35.4),
    (377.2, 127.5, 35.4),
    (382.7, 127.5, 35.4),
    (387.0, 127.5, 35.4),
    (390.7, 127.5, 35.4),
    (394.7, 127.5, 35.4),
    (397.2, 127.5, 35.4),
    (402.9, 127.5, 35.4),
    (406.5, 127.5, 35.4),
    (410.3, 127.5, 35.4),
    (413.1, 127.5, 35.4),
    (416.9, 127.5, 35.4),
    (421.8, 127.5, 35.4),
    (424.5, 127.5, 35.4),
    (429.9, 127.5, 35.4),
    (433.4, 127.5, 35.4),
    (438.5, 127.5, 35.4),
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
    (0, 425),
    (0, 475),
    (0, 525)
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
df.to_excel('岸桥3及AGV能耗2.xlsx', index=False, engine='openpyxl')