import pandas as pd
import random

# 假设您有一个包含Excel文件路径的列表
excel_files = ['场桥1.xlsx', '场桥2.xlsx', '场桥3.xlsx', '场桥4.xlsx', '场桥5.xlsx', '场桥6.xlsx', '场桥7.xlsx',
               '场桥8.xlsx', '场桥9.xlsx', '岸桥1及AGV能耗.xlsx', '岸桥2及AGV能耗.xlsx', '岸桥3及AGV能耗.xlsx']  # 替换为您的文件名

# 初始化一个空的DataFrame来存储最终结果
final_results = pd.DataFrame()

# 重复操作10次
for i in range(10):
    # 用于存储所有DataFrame对象的列表
    all_dataframes = []

    # 读取所有Excel文件，并将它们添加到all_dataframes列表中
    for file in excel_files:
        df = pd.read_excel(file)
        if not df.empty:
            all_dataframes.append(df)

            # 从每个DataFrame中随机选择一列
    random_columns = []
    for df in all_dataframes:
        if not df.empty and df.shape[1] > 0:
            random_column_name = df.columns[random.randint(0, df.shape[1] - 1)]
            random_column = df[random_column_name]
            random_columns.append(random_column)

    # 检查随机选择的列是否包含有效数据
    for m, col in enumerate(random_columns):
        print(f"Random column from file {m + 1}:")
        print(col.dropna())  # 打印非NaN值

    # 初始化一个空的Series来存储总和（使用第一个非空列作为模板）
    if random_columns:
        total_energy_demand = random_columns[0].copy()
        total_energy_demand[:] = 0  # 将所有值初始化为0，以便后续相加
    else:
        print("No valid columns to sum!")
        exit(1)  # 退出程序，因为没有有效数据可以处理

    # 将所有随机选择的列相加（确保它们对齐）
    for series in random_columns:  # 从第二列开始相加，因为第一列已经用作模板
        if series.index.equals(total_energy_demand.index):
            total_energy_demand += series
        else:
            # 如果索引不匹配，可以尝试对齐索引或重置索引后再相加
            print("Warning: Index mismatch!")
            series = series.reindex(total_energy_demand.index, fill_value=0)  # 对齐索引，缺失值填0
            total_energy_demand += series
    # 重置索引并删除原索引，然后将结果转换为列表
    total_energy_demand_list = total_energy_demand.reset_index(drop=True).tolist()
    # 将结果添加到final_results DataFrame中作为新列
    final_results[f'Sum_{i + 1}'] = total_energy_demand_list

# 将最终结果保存到Excel文件中，不包含索引和表头
final_results.to_excel('total_energy_demand.xlsx', index=False, header=False)