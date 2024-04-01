import math
import itertools
import time
import random
import pandas as pd

# 假设初始位置是轨道的最右端，并具有一定的z坐标
z_initial = 18  # 小车初始z坐标

# 小车移动速度（假设为恒定速度）
v_y_loaded = 1.166  # 满载时小车在y轴上的移动速度，单位：米/秒
v_y_unloaded = 1.166  # 空载时小车在y轴上的移动速度，单位：米/秒
v_z_load_down = 0.3666  # 小车满载下行的速度，单位：米/秒
v_z_unload_down = 0.4583  # 小车空载下行的速度，单位：米/秒
v_z_load_up = 0.3666  # 小车满载上行的速度，单位：米/秒
v_z_unload_up = 0.4583  # 小车满载上行的速度，单位：米/秒
v_yc_move = 0.5  # 场桥满载桥做贝位移动
v_yc_move2 = 2.25  # 场桥空载做贝位移动
# 功率值
P_y_loaded_kW = 56.1  # 满载时场桥小车功率，单位：千瓦（移动箱子）
P_y_unloaded_kW = 54.3  # 空载时场桥小车功率，单位：千瓦（移动箱子）
P_down_load_kW = 56.1  # 小车下行满载功率，单位：千瓦
P_down_unloaded_kW = 54.3  # 小车下行空载功率，单位：千瓦
P_up_load_kW = 56.1  # 小车上行满载功率，单位：千瓦
P_up_unload_kW = 54.3  # 小车上行空载功率，单位：千瓦
P_x_load_kW = 56.1  # 场桥满载做贝位移动
P_x_unload_kW = 54.3  # 场桥空载做贝位移动
#  需要卸载箱子的目标坐标列表
unload_positions = [
    (-112.0, 400.5, 0.0),
    (-109.0, 400.5, 0.0),
    (-106.0, 400.5, 0.0),
    (-103.0, 400.5, 0.0),
    (-100.0, 400.5, 0.0),
    (-97.0, 400.5, 0.0),
    (-94.0, 400.5, 0.0),
    (-91.0, 400.5, 0.0),
    (-88.0, 400.5, 0.0),
    (-85.0, 400.5, 0.0),
    (-82.0, 400.5, 0.0),
    (-79.0, 400.5, 0.0),
    (-76.0, 400.5, 0.0),
    (-73.0, 400.5, 0.0),
    (-70.0, 400.5, 0.0),
    (-67.0, 400.5, 0.0),
    (-64.0, 400.5, 0.0),
    (-61.0, 400.5, 0.0),
    (-58.0, 400.5, 0.0),
    (-112.0, 413.5, 2.6),
    (-109.0, 413.5, 2.6),
    (-106.0, 413.5, 2.6),
    (-103.0, 413.5, 2.6),
    (-100.0, 413.5, 2.6),
    (-97.0, 413.5, 2.6),
    (-94.0, 413.5, 2.6),
    (-91.0, 413.5, 2.6),
    (-88.0, 413.5, 2.6),
    (-85.0, 413.5, 2.6),
    (-82.0, 413.5, 2.6),
    (-79.0, 413.5, 2.6),
    (-76.0, 413.5, 2.6),
    (-73.0, 413.5, 2.6),
    (-70.0, 413.5, 2.6),
    (-67.0, 413.5, 2.6),
    (-64.0, 413.5, 2.6),
    (-112.0, 426.5, 5.2),
    (-109.0, 426.5, 5.2),
    (-106.0, 426.5, 5.2),
    (-103.0, 426.5, 5.2),
    (-100.0, 426.5, 5.2),
    (-97.0, 426.5, 5.2),
    (-94.0, 426.5, 5.2),
    (-91.0, 426.5, 5.2),
    (-88.0, 426.5, 5.2),
    (-85.0, 426.5, 5.2),
    (-82.0, 426.5, 5.2),
    (-79.0, 426.5, 5.2),
    (-76.0, 426.5, 5.2),
    (-73.0, 426.5, 5.2),
    (-70.0, 426.5, 5.2),
    (-67.0, 426.5, 5.2),
    (-64.0, 426.5, 5.2),
    (-112.0, 439.5, 7.8),
    (-109.0, 439.5, 7.8),
    (-106.0, 439.5, 7.8),
    (-103.0, 439.5, 7.8),
    (-100.0, 439.5, 7.8),
    (-97.0, 439.5, 7.8),
    (-94.0, 439.5, 7.8),
    (-91.0, 439.5, 7.8),
    (-88.0, 439.5, 7.8),
    (-85.0, 439.5, 7.8),
    (-82.0, 439.5, 7.8),
    (-79.0, 439.5, 7.8),
    (-76.0, 439.5, 7.8),
    (-73.0, 439.5, 7.8),
    (-112.0, 452.5, 10.4),
    (-109.0, 452.5, 10.4),
    (-106.0, 452.5, 10.4),
    (-103.0, 452.5, 10.4),
    (-100.0, 452.5, 10.4),
    (-97.0, 452.5, 10.4),
    (-94.0, 452.5, 10.4),
    (-91.0, 452.5, 10.4),
    (-88.0, 452.5, 10.4),
    (-85.0, 452.5, 10.4),
    (-82.0, 452.5, 10.4),
    (-79.0, 452.5, 10.4),
]
# 箱子起始点
springboard = (0, 425, 0)
x, y, z = springboard

data_list = []  # excel输出


# 生成器函数，用于产生指定数量的随机排列，每个排列内部按 z 值降序排列
def generate_random_permutations(positions, num_permutations):
    for _ in range(num_permutations):
        # 创建当前 positions 列表的一个副本，并随机打乱它的顺序
        shuffled_positions = positions.copy()
        random.shuffle(shuffled_positions)

        # 对打乱后的列表进行排序，按 z 值的降序排列
        shuffled_positions.sort(key=lambda pos: pos[2], reverse=False)

        # 产出排列
        yield shuffled_positions

    # 设置你想要生成的排列数量


num_permutations_to_generate = 100
# 初始化总能耗和总时间
total_energy_kWh = 0
total_time_s = 0
t_yc_move = 0
energy_yc_move = 0
t_yc_move2 = 0
energy_yc_move2 = 0

# 初始化总能耗和总时间的列表，用于存储每种顺序的结果
total_energies_kWh = []
total_times_s = []
# 初始化上一个y坐标的变量
previous_y = None
# 记录循环开始的时间
start_time = time.time()
# 设置循环运行的时间限制（秒）
time_limit = 0.05
#  初始化运行时间
elapsed_time = 0
# 初始化计数器和循环条件
count = 0

for permutation in generate_random_permutations(unload_positions, num_permutations_to_generate):
    order = list(permutation)  # 将元组转换为列表（这一步其实是不必要的，因为permutation已经是一个元组列表）
    # 打印当前顺序
    print("----start------")
    print(f"第一个场桥工作顺序：{order}")
    # 在循环体内增加计数器的值
    count += 1
    # 遍历每个需要卸载的箱子坐标
    for position in unload_positions:
        x_unload, y_unload, z_unload = position
        # 计算小车从初始位置到箱子位置的y轴上距离（假设只在x轴上移动）
        L_m = abs(y - y_unload)  # 单位：米

        # 第一步：计算场桥移动的时间和能耗
        x_distance = abs(x - x_unload)
        t_x_load = x_distance / v_yc_move
        energy_x_kWh = P_x_load_kW * (t_x_load / 3600)
        total_energies_kWh.append(energy_x_kWh)
        total_times_s.append(t_x_load)

        # 第二步：计算无货y轴移动时间和能耗
        t_s_move3 = L_m / v_y_unloaded  # 单位：秒
        energy_move3_kWh = P_y_unloaded_kW * (t_s_move3 / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_move3_kWh)
        total_times_s.append(t_s_move3)

        # 第三步：计算小车向下抓取移动时间和能耗
        z_distance = z_initial - z  # 下行距离
        t_s_down = z_distance / v_z_unload_down  # 单位：秒
        energy_move1_kWh = P_down_unloaded_kW * (t_s_down / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_move1_kWh)
        total_times_s.append(t_s_down)

        # 第四步：计算小车抓箱子向上的时间和能耗
        t_s_up = z_distance / v_z_load_up  # 单位：秒
        energy_up_kWh = P_up_load_kW * (t_s_up / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_up_kWh)
        total_times_s.append(t_s_up)

        # 第五步：计算载货y轴移动时间和能耗
        t_s_move2 = L_m / v_y_loaded  # 单位：秒
        energy_move2_kWh = P_y_loaded_kW * (t_s_move2 / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_move2_kWh)
        total_times_s.append(t_s_move2)

        # 第六步：计算小车载箱子后下行的时间和能耗
        t_s_down2 = z_initial / v_z_load_down  # 单位：秒
        energy_down2_kWh = P_down_load_kW * (t_s_down2 / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_down2_kWh)
        total_times_s.append(t_s_down2)

        # 第七步：计算空载小车上行时间和能耗
        t_s_up2 = z_initial / v_z_unload_up  # 单位：秒
        energy_up2_kWh = P_up_unload_kW * (t_s_up2 / 3600)  # 单位：千瓦时
        total_energies_kWh.append(energy_up2_kWh)
        total_times_s.append(t_s_up2)

        # 第八步：计算场桥移动的时间和能耗
        x_distance = abs(x - x_unload)
        t_x_unload = x_distance / v_yc_move2
        energy_x_kWh2 = P_x_unload_kW * (t_x_unload / 3600)
        total_energies_kWh.append(energy_x_kWh2)
        total_times_s.append(t_x_unload)

        total_energy_kWh += (energy_move1_kWh + energy_up_kWh + energy_x_kWh + energy_move2_kWh + energy_down2_kWh +
                             energy_up2_kWh + energy_move3_kWh + energy_x_kWh2)
        total_time_s += t_s_down + t_s_up + t_x_load + t_s_move2 + t_s_down2 + t_s_up2 + t_s_move3 + t_x_unload
        # 输出每一步的能耗和时间
        print(f"箱子起点坐标：（{x}, {y}, {z}）箱子目标坐标：({x_unload}, {y_unload}, {z_unload})")
        print(f"第一步（场桥小车向下移动）时间：{t_s_down:.2f} 秒，能耗：{energy_move1_kWh:.2f} 千瓦时")
        print(f"第二步（场桥小车向上移动）时间：{t_s_up:.2f} 秒，能耗：{energy_up_kWh:.2f} 千瓦时")
        print(f"第三步（场桥整体移动）时间：{t_x_load:.2f} 秒，能耗：{energy_x_kWh:.2f} 千瓦时")
        print(f"第四步（场桥小车y轴上移动）时间：{t_s_move2:.2f} 秒，能耗：{energy_move2_kWh:.2f} 千瓦时")
        print(f"第五步（场桥小车向下移动）时间：{t_s_down2:.2f} 秒，能耗：{energy_down2_kWh:.2f} 千瓦时")
        print(f"第六步（小场桥小车向上移动）时间：{t_s_up2:.2f} 秒，能耗：{energy_up2_kWh:.2f} 千瓦时")
        print(f"第七步（场桥小车y轴上移动）：{t_s_move3:.2f} 秒，能耗：{energy_move3_kWh:.2f} 千瓦时")
        print(f"第八步（场桥整体移动）：{t_x_unload:.2f} 秒，能耗：{energy_x_kWh2:.2f} 千瓦时")

    # 初始化变量每60min
    total_time = 0.0  # 累计时间
    total_energy = 0.0  # 当前小时的能源总和
    print(f"----0-23个时间段，每个时间段的能耗----")
    # 遍历时间和能源列表
    for times, energy in zip(total_times_s, total_energies_kWh):
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
            total_energy = 0.0 if remaining_time == 0.0 else total_energies_kWh[
                total_energies_kWh.index(energy) + 1]  # 假设下一个能源值是当前小时剩余时间的能源

    # 如果在循环结束时还有剩余时间（即不是整小时结束），则输出最后的能源和
    if total_time > 0:
        print(f"未满1h部分: {total_energy}")
        data_list.append(total_energy)
    total_times_s.clear()
    total_energies_kWh.clear()
    # 检查是否已经超过了时间限制
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time >= time_limit:
        break  # 如果已经超过了时间限制，跳出循环
# 输出最终结果包含方案个数.运行时间.总能耗和总时间
print("循环已停止，代码总共运行了 {} 秒".format(elapsed_time))
print(f"-------------共有方案个数: {count} ---------------------------")
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
df.to_excel('场桥16.xlsx', index=False, engine='openpyxl')