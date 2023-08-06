import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

X, Y = np.meshgrid(np.linspace(-3, 3, 128), np.linspace(-3, 3, 128))
Z = (1 - X/2 + X**5 + Y**3) * np.exp(-X**2 - Y**2)

pc = plt.pcolormesh(X, Y, Z, vmin=-1, vmax=1, cmap='RdBu_r')
# plt.show()
print(Z)

exit()
print()

fields = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
colors = ['#1D2F6F', '#8390FA', '#6EAF46', '#FAC748']
labels = ['NA', 'EU', 'JP', 'Others']

# figure and axis
fig, ax = plt.subplots(1, figsize=(12, 10))
# plot bars
df_grouped = df.groupby('Platform').sum()[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']]
left = len(df_grouped) * [0]
for idx, name in enumerate(fields):
    plt.barh(df_grouped.index, df_grouped[name], left=left, color=colors[idx])
    left = left + df_grouped[name]
需要达到与贷款利率相同的理财产品才能保证每个月有足够的钱还款
# title, legend, labels
plt.title('Video Game Sales By Platform and Region\n', loc='left')
plt.legend(labels, bbox_to_anchor=([0.55, 1, 0, 0]), ncol=4, frameon=False)
plt.xlabel('Millions of copies of all games')
# remove spines
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
# adjust limits and draw grid lines
plt.ylim(-0.5, ax.get_yticks()[-1] + 0.5)
ax.set_axisbelow(True)
ax.xaxis.grid(color='gray', linestyle='dashed')
plt.show()
