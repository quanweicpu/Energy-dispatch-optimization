import pandas as pd

# 读取两个Excel文件
df1 = pd.read_excel('total_energy_demand.xlsx', header=None)
df2 = pd.read_excel('total_energy_demand2.xlsx', header=None)

# 垂直连接（在行上追加）
result = pd.concat([df1, df2], ignore_index=False)
# 创建一个全零的DataFrame来代替全零的行
zero_row_df = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], columns=result.columns)

# 使用pd.concat来合并DataFrame
result = pd.concat([result, zero_row_df], ignore_index=True)
# 将结果写入新的Excel文件
result.to_excel('total_energy_demand3.xlsx', index=False, header=False)