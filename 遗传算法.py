import numpy as np
from deap import base, creator, tools, algorithms
import pandas as pd
import matplotlib.pyplot as plt
import statistics

# Excel文件路径
excel_file = 'total_energy_demand3.xlsx'
# 读取Excel文件
df = pd.read_excel(excel_file, header=None)
# 假设你想要读取的列名为'Demand'
demand_column = df.iloc[:, 0]
# 能源系统参数
wind_supply = np.full(24, 140)
solar_supply = np.array([0, 0, 0, 0, 0, 0, 5, 15, 50, 80, 120, 130, 140, 140, 100, 80, 60, 30, 5, 0, 0, 0, 0, 0])
# 风光
demand = demand_column.to_numpy()
# 需求
hydrogen_storage_capacity = 600  # 氢储能池最大容量
initial_hydrogen_storage = 400  # 初始氢储能池能量
conversion_efficiency = 0.7
electricity_price = np.array(
    [0.64, 0.64, 0.64, 0.64, 0.64, 0.64, 0.64, 0.64, 0.64, 0.29, 0.29, 0.19, 0.19, 0.19, 0.19, 1.14, 1.14, 1.14, 1.14,
     0.99, 0.99, 0.64, 0.64, 0.64])
hydrogen_price = np.full(24, 0.226)
h = np.array([-3.3918248,  198.5208272,   56.93988211, 531.15876985,  78.07488241,
  91.39348033, 153.26591099, 162.47856358, 241.59454622, 319.56567916,
  -9.99418765,  80.80330167,  87.47086093, 218.27273041,  27.33503202,
  65.26816399,  28.02191477, 248.2398289,  76.51066675,  86.71151276,
 330.63613073,  88.65534611, 252.79812193 -33.59626228])
g = np.array([1085.19650211,  894.39143994, 1028.57134155,  520.38338598,  963.15974301,
  940.80762792, 842.29202465,  813.5876013,   736.80199978,  682.35441566,
 1024.96336257,  957.22420435,  400.1571963,   859.75426959, 1060.69196798,
 1022.75883601, 1060.00508523,  839.7871711,  1011.51633325, 1001.31548724,
  757.39086927,  999.37165389,  835.22887807, -106.40373772])
# 惩罚因子，用于惩罚供需不匹配的情况
penalty_factor = 1e6  # 大约束惩罚
waste_penalty = 3  # 浪费惩罚
grid_penalty = 1000  # 小约束惩罚

# co2处理成本

# 遗传算法参数
population_size = 1500
num_generations = 200
mutation_rate = 0.01
crossover_rate = 0.01
DNA_SIZE = 48  # 24 for grid_power_use and 24 for hydrogen_to_use

# 设置适应度最小化和个体类
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
# 初始化种群和算法参数
toolbox = base.Toolbox()
toolbox.register("attr_float", np.random.uniform, 0.45, 0.95)  # 电的占比权重，比如0.6代表电氢比为6:4
# toolbox.register("Binary", bernoulli.rvs, 0.5)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=DNA_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=population_size)


# 解码函数 - 将二进制编码转换为实际能源使用量
def decode_individual(individual):
    x = demand - (solar_supply + wind_supply)
    grid_power_use = np.zeros(24)
    hydrogen_to_use = np.zeros(24)
    # 解码电网电能使用量和氢能使用量
    for i in range(24):
        grid_power_use[i] = (demand[i] - solar_supply[i] - wind_supply[i]) * individual[i]
        # grid_power_use[i] = g[i] * individual[i]
        # 映射到 [0, demand[i]-风，光]
        hydrogen_to_use[i] = x[i] - grid_power_use[i]
        if hydrogen_to_use[i] > hydrogen_storage_capacity:
            hydrogen_to_use[i] = hydrogen_storage_capacity
            grid_power_use[i] = x[i] - hydrogen_to_use[i]
        # hydrogen_to_use[i]小于hydrogen_storage_capacity的约束
        # hydrogen_to_use[i] = hydrogen_storage_capacity * individual[i]
        # hydrogen_to_use[i] = h[i] * individual[i]
        # 映射到 [0, hydrogen_storage_capacity]
        grid_power_use[23] = 0
        hydrogen_to_use[23] = x[i]
    return grid_power_use, hydrogen_to_use


# 能源分配函数 - 按照优先级分配能源
def allocate_energy(solar_wind_supply, demand, hydrogen_to_use, current_hydrogen_storage):
    energy_deficit = demand - solar_wind_supply  # 计算使用风、光后的能源需求
    hydrogen_produced = max(0, conversion_efficiency * (solar_wind_supply - demand))  # 多余的太阳能和风能用于产生氢能或充电
    # 如果hydrogen_to_use小于0，则表示充电
    if hydrogen_to_use < 0:
        # 计算可充电量，不能超过当前存储容量与最大存储容量之差，也不能超过-hydrogen_to_use（即充电请求量）
        hydrogen_to_charge = min(hydrogen_produced, hydrogen_storage_capacity - current_hydrogen_storage)
        # 更新氢能存储量
        current_hydrogen_storage += hydrogen_to_charge
        # 实际上没有使用氢能，所以hydrogen_used为0
        hydrogen_used = 0
    else:
        # 使用氢能填补剩余需求，但不能超过当前存储量和需求量
        hydrogen_used = min(hydrogen_to_use, current_hydrogen_storage, energy_deficit)
        # 更新氢能存储量
        current_hydrogen_storage -= hydrogen_used
    wasted_energy = max(0, solar_wind_supply - demand - hydrogen_produced - hydrogen_used)
    wasted_hydrogen = max(0, hydrogen_to_use - hydrogen_used)

    # 使用电网电能填补剩余能源需求
    grid_power_needed = max(0, energy_deficit - hydrogen_used)
    grid_power_used = grid_power_needed  # 电网电能量不能为负，且此时已经确保非负
    return grid_power_used, hydrogen_used, current_hydrogen_storage, wasted_energy, wasted_hydrogen


# 适应度函数
def evaluate(individual):
    grid_power_use, hydrogen_to_use = decode_individual(individual)
    total_cost = 0
    cost = 0
    current_hydrogen_storage = initial_hydrogen_storage
    grid_used_per_hour = [0] * 24
    hydrogen_used_per_hour = [0] * 24
    hydrogen_to_uses = 0
    for i in range(24):
        solar_wind_supply = solar_supply[i] + wind_supply[i]  # 当前时刻太阳能和风能的总供应量
        hydrogen_produced = max(0, conversion_efficiency * (solar_wind_supply - demand[i]))
        # 分配能源并计算成本
        grid_power_used, hydrogen_used, current_hydrogen_storage, wasted_energy, wasted_hydrogen = allocate_energy(
            solar_wind_supply, demand[i], hydrogen_to_use[i], current_hydrogen_storage)
        total_cost += electricity_price[i] * grid_power_used + hydrogen_price[i] * max(0,
                                                                                       hydrogen_used)  # 氢能使用量为负时不计入成本
        # 各种约束惩罚
        total_cost += waste_penalty * wasted_energy  # 风光多生产未使用惩罚
        total_cost += penalty_factor * wasted_hydrogen  # 氢的实际使用量接近于种群生成值
        total_cost += penalty_factor * abs(grid_power_used - grid_power_use[i])  # 电的实际使用量接近于种群生成值
        if current_hydrogen_storage - hydrogen_used < 0:
            total_cost += penalty_factor * abs(current_hydrogen_storage - hydrogen_used)
        if hydrogen_to_use[i] < 0:
            total_cost += penalty_factor * abs(-hydrogen_to_use[i] - hydrogen_produced)
        hydrogen_to_uses += hydrogen_to_use[i]
    # for i in range(24):
    #     solar_wind_supply = solar_supply[i] + wind_supply[i]  # 当前时刻太阳能和风能的总供应量
    #     # 分配能源并计算成本
    #     grid_power_used, hydrogen_used, _, _, _ = allocate_energy(
    #         solar_wind_supply, demand[i], hydrogen_to_use[i], current_hydrogen_storage)
    #     cost += electricity_price[i] * grid_power_used + hydrogen_price[i] * max(0, hydrogen_used)  # 氢能使用量为负时不计入成本
    # # 返回总成本作为适应度值（注意：在某些遗传算法实现中，可能需要将其转换为元组形式）
    # total_cost += abs(hydrogen_to_uses - initial_hydrogen_storage) * penalty_factor
    best_fitness_values.append(total_cost)
    return total_cost,  # 或者返回 (total_cost,) 如果需要单元素元组形式


best_fitness_values = []


def calculate_cost(individual):
    grid_power_use, hydrogen_to_use = decode_individual(individual)
    cost = 0
    current_hydrogen_storage = initial_hydrogen_storage
    for i in range(24):
        solar_wind_supply = solar_supply[i] + wind_supply[i]  # 当前时刻太阳能和风能的总供应量
        # 分配能源并计算成本
        grid_power_used, hydrogen_used, _, _, _ = allocate_energy(
            solar_wind_supply, demand[i], hydrogen_to_use[i], current_hydrogen_storage)
        cost += electricity_price[i] * grid_power_used + hydrogen_price[i] * max(0, hydrogen_used)  # 氢能使用量为负时不计入成本
    # best_fitness_values.append(cost)
    return cost


# 注册评估、交叉、变异和选择操作
toolbox.register("evaluate", evaluate)
toolbox.register("calculate_cost", calculate_cost)
toolbox.register("mate", tools.cxTwoPoint)  # 使用两点交叉
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.1)  # 使用高斯变异，这里可能需要调整sigma和indpb的值以适应问题规模
toolbox.register("select", tools.selTournament, tournsize=3)  # 使用锦标赛选择

# 创建初始种群并运行遗传算法
pop = toolbox.population(n=population_size)
result = algorithms.eaSimple(pop, toolbox, cxpb=crossover_rate, mutpb=mutation_rate, ngen=num_generations,
                             verbose=False)

# 输出最佳解和对应的成本
best_individual = tools.selBest(result[0], 1)[0]
best_grid_power_use, best_hydrogen_to_use = decode_individual(best_individual)
best_constraint_reference_value = evaluate(best_individual)[0]
best_cost = calculate_cost(best_individual)

# 绘制优化图像
plt.plot(best_fitness_values)
plt.xlabel('Generation')  # X轴标签为“代数”
plt.ylabel('fitness')  # Y轴标签为“适应度值”
plt.title('Genetic algorithm total cost optimization')  # 图表标题为“遗传算法中的适应度进展”
plt.grid(False)  # 显示网格线
plt.show()  # 显示图表
print(best_individual)
print("Best grid power use:", best_grid_power_use)
print("Best hydrogen to use:", best_hydrogen_to_use)
print("Satisfy constraint reference value:", best_constraint_reference_value)
print("best cost:", best_cost)
