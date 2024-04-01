import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

params = {
    'figure.figsize': '6, 4'
}
plt.rcParams.update(params)
plt.rc('font',family='Times New Roman')
fig, ax = plt.subplots()
fig.subplots_adjust(right=0.65)

label = ['L1','L2','L3']
color = ["#FF9900", "#4674D1", "#DC3912"]

Data = pd.DataFrame()
Data['group'] = list(range(1,11))
Data['d1']    = [4.4,-2.22,2.31,1.56,2.37,0.1,-2,1.5,2,0.3]
Data['d2']    = [5.4,1.45,1.29,1.05,-1.68,1.56,2.37,0.1,-2,1]
Data['d3']    = [-1.6,0.4,1.32,2.56,2.37,1.45,1.29,1.05,-1.6,0.6]
Data['ss']    = [-1.4,.29,1.05,.05,-4,2.37,0.1,-2,1.5,3]

split_1 = Data["d1"]
split_2 = Data["d2"]
split_3 = Data["d3"]
data = np.array([split_1, split_2, split_3])

def fun(f, **kwargs):
    cum = f.clip(**kwargs)
    cum = np.cumsum(cum, axis=0)
    d = np.zeros(np.shape(f))
    d[1:] = cum[:-1]
    return d
data_min0 = fun(data, min=0)
data_max0 = fun(data, max=0)

isneg = (data < 0)
data_min0[isneg] = data_max0[isneg]
stack = data_min0

id_ = Data["group"]
x_lab = "G" + (Data["group"]).map(int).map(str)
ax.set_xticks(Data["group"])
rects2 = ax.plot(id_, Data["ss"].values,
                 marker='^', color='green',
                 label="SS", linestyle=':')

data_shape = np.shape(data)
for i in np.arange(0, data_shape[0]):
    ax.bar(id_, data[i],
           bottom=stack[i],
           label=label[i], color=color[i])

ax.set_xticklabels(x_lab.values, rotation=45)
plt.xlabel('Group')
plt.ylabel('Proxy')
plt.tick_params(labelsize=10)


fig.legend(ncol=1, loc='upper right',
           bbox_to_anchor=(1, 1),
           bbox_transform=ax.transAxes)

plt.annotate('By: Mr Figurant', xy = (5, 5), xytext = (5, 5))
plt.show()