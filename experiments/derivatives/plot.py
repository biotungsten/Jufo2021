import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
dataRaw = {}

with open("aggregated_data.csv", "r") as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        dataRaw[line[0]] = [float(n) for n in line[1:]]

keysForPlot = ["C100", "R100", "H100", "CTRL"]
namesForPlot = ["Catechol", "Resorcinol", "Hydrochinon", "Kontrolle"]
data = {key: dataRaw[key] for key in keysForPlot}

mean2 = [value[0] for key,value in data.items()]
sd2 = [value[2] for key,value in data.items()]
mean7 = [value[1] for key,value in data.items()]
sd7 = [value[3] for key,value in data.items()]
barWidth = 0.3
fig = plt.figure()
ax = plt.subplot(111)
r1 = [0.9*n for n in np.arange(len(data.keys()))]
r2 = [((1/0.9)*x + barWidth)*0.9 for x in r1]

ctrl=data["CTRL"]
for key, value in data.items():
    p2 = stats.ttest_ind_from_stats(value[0], value[2], 4, ctrl[0], ctrl[2], 4, equal_var=False).pvalue
    p7 = stats.ttest_ind_from_stats(value[1], value[3], 4, ctrl[1], ctrl[3], 4, equal_var=False).pvalue
    t2 = stats.ttest_ind_from_stats(value[0], value[2], 4, ctrl[0], ctrl[2], 4, equal_var=False).statistic
    t7 = stats.ttest_ind_from_stats(value[1], value[3], 4, ctrl[1], ctrl[3], 4, equal_var=False).statistic
    print(f"{key} p2:{round(p2/2,4)}, p7:{round(p7/2,4)}; t2:{round(t2,4)}, t7:{round(t7,4)}") #divide by two because one tailed
def stripNamesOfNumber(str):
    new_str = ""
    for n in str:
        if n.isnumeric():
            pass
        else:
            new_str += n
    return new_str

ax.bar(r1, mean2, width = barWidth, color = 'orange', edgecolor = 'black', yerr=[sd2, sd2], capsize=7, label='1 Tag', error_kw=dict(capsize=2, elinewidth=0.5))
ax.bar(r2, mean7, width = barWidth, color = 'red', edgecolor = 'black', yerr=[sd7, sd7], capsize=7, label='6 Tage', error_kw=dict(capsize=2, elinewidth=0.5))
ax.set_xticks([0.9*r + barWidth/2 -0.03 for r in range(len(data.keys()))])
ax.text(x=r1[0]-0.05,y=0.07,s="**",rotation=180, size=8)
ax.text(x=r2[0]-0.05,y=0.23,s="**",rotation=180, size=8)
ax.text(x=r1[1]-0.05,y=0.03,s="**",rotation=180, size=8)
ax.text(x=r2[1]-0.05,y=0.25,s="**",rotation=180, size=8)
ax.text(x=r1[2]-0.05,y=0.1,s="**",rotation=180, size=8)
ax.text(x=r2[2]-0.05,y=0.41,s="**",rotation=180, size=8)
ax.set_xticklabels(namesForPlot)
ax.set_ylabel("Keimungsrate [%]")
ax.set_yticklabels([0,20,40,60,80,100])
ax.legend(frameon=False)
ax.set_ylim([0,1])
plt.savefig("derivatives.png", dpi=600, bbox_inches='tight')