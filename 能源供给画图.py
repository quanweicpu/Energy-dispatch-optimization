import matplotlib.pyplot as plt
import numpy as np

# 创建四个数组的数据
data1 = [1117.43908747, 1089.4913158,  1076.46252842, 1063.92506923,  944.10489578,
 1088.38344577, 1015.20278366,  920.81720152,  945.8719314,   927.83373191,
 1033.63621116, 1037.3238083,   487.47243647, 1058.26307628, 1079.21933601,
  994.50440326, 1163.16663548, 1026.86701467, 1089.00046038, 1182.04650802,
 1033.98087516, 1064.49371543,   85.33182234,  0]
data2 = [-35.7034782,    0.61862637,   0.9659858,  -12.26423289,  88.15544888,
 -58.09493521, -28.97989067,  59.44115116,  30.71444284,  64.01547521,
 -16.55629321,  -4.64519045,   0.73293146,  25.92078209,  21.45288774,
  95.42832836, -28.75410697,  59.63062873,   2.85699693, -80.44606906,
  85.19978396,   0.62937924, 22.26149007, -67.58498218]
data3 = np.array([140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 140
                     , 140, 140, 140, 140, 0])
data4 = np.array([0, 0, 0, 0, 0, 0, 5, 15, 50, 80, 120, 130, 140, 140, 100, 80, 60, 30, 5, 0, 0, 0, 0, 0])
# 创建一个足够大的图形
plt.figure(figsize=(16, 10.9))  # 宽度为8英寸，高度为4英寸
# 设置柱状图的x轴位置
x = np.arange(len(data1))

# 设置柱状图的宽度
width = 0.35


# RGB颜色设置，每个分量的取值范围是0到1

color1 = (60/255, 64/255, 91/255)  #
color2 = (223/255, 122/255, 94/255)  #
color3 = (242/255, 204/255, 142/255)  #
color4 = (244/255, 241/255, 222/255)  #

# 绘制第一个数组的柱状图
plt.bar(x, data1, width=width, color=color1, label='grid')
# 将data2分成正数和负数两部分
data2_positive = np.clip(data2, 0, None)
data2_negative = np.clip(data2, None, 0)
# 处理data2的正数部分，直接堆叠在data1上
bottom2_positive = data1
plt.bar(x, data2_positive, width=width, bottom=bottom2_positive, color=color2, label='Hydrogen energy (positive)')

# 处理data2的负数部分，在x轴下方绘制
# 我们需要创建一个新的x轴来展示负数值
plt.gca().invert_yaxis()  # 翻转y轴以便负数在下面
plt.bar(x, data2_negative, width=width, color=color2, label='Hydrogen energy (negative)')

# 恢复y轴方向以便之后的堆叠是正确的
plt.gca().invert_yaxis()

# 现在bottom2应该是data1与data2_positive堆叠后的结果
bottom2 = bottom2_positive + data2_positive

# 接下来的堆叠继续正常处理...
bottom3 = bottom2  # 由于我们单独处理了负数，这里不再累加data2_negative
# 绘制第三个数组的柱状图
plt.bar(x, data3, width=width, bottom=bottom3, color=color3, label='wind energy')

# 计算第四个柱状图的底部位置（即前三个柱状图堆叠后的顶部位置）
bottom4 = bottom3 + np.array(data3)
# 绘制第四个数组的柱状图
plt.bar(x, data4, width=width, bottom=bottom4, color=color4, label='solar energy')

# 设置x轴的标签
plt.xlabel('Hour')
# 设置y轴的标签
plt.ylabel('Energy supply')
# 设置图表的标题
plt.title('Energy usage by type')


# 显示图例
plt.legend(bbox_to_anchor=(1.01, 0), loc='lower left', borderaxespad=0.)

# 显示图表
plt.show()