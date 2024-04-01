import matplotlib.pyplot as plt
import numpy as np

data1 = [1221.032727,
         1231.598949,
         1231.563938,
         1223.560085,
         1225.126343,
         1238.496369,
         1225.353854,
         1228.77061,
         1229.158406,
         1229.708942,
         1231.05076,
         1222.663851,
         651.5564883,
         1231.765298,
         1243.181511,
         1231.729989,
         1272.237496,
         1223.659618,
         1228.407774,
         1239.430234,
         1263.469664,
         1209.012341,
         247.6100247,
         0]
# RGB颜色设置，每个分量的取值范围是0到1
color1 = (60/255, 64/255, 91/255)  #
color2 = (223/255, 122/255, 94/255)  #
color3 = (242/255, 204/255, 142/255)  #
color4 = (244/255, 241/255, 222/255)  #
color5 = (230/255, 111/255, 81/255)
color6 = (69/255, 123/255, 157/255)
# 创建一个足够大的图形
plt.figure(figsize=(16, 10.9))  # 宽度为8英寸，高度为4英寸
# 设置柱状图的x轴位置
x = np.arange(len(data1))

# 设置柱状图的宽度
width = 0.35
plt.bar(x, data1, width=width, color=color6, label='grid')
# 设置x轴的标签
plt.xlabel('Hour')
# 设置y轴的标签
plt.ylabel('Energy demand')
# 设置图表的标题
plt.title('24h Energy demand')


# 显示图例
plt.legend(bbox_to_anchor=(1.01, 0), loc='lower left', borderaxespad=0.)

# 显示图表
plt.show()
# 显示图形
plt.show()
