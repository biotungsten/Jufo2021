import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
data = {}

#run this script from experiments dir with -m option
#results are in analysis.txt

#import data
with open("aggregated_data.csv", "r") as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        if (line[0] not in ["C100", "CA10", "PA10", "CTRL"]):
            continue
        if (line[0] == "CTRL"):
            interm = "Kontrolle"
        if (line[0] == "C100"):
            interm = "Catechol"
        if (line[0] == "CA10"):
            interm = "Dihydrokaffeesäure"
        if (line[0] == "PA10"):
            interm = "Phloretinsäure"
        data[interm] = [float(n) for n in line[1:]]


def swap(pos1, pos2, arr2):
    arr = arr2
    temp = arr[pos1]
    arr[pos1] = arr[pos2]
    arr[pos2] = temp
    return arr

#structure data and make vars for plotting
data_items = list(data.values())
data_items = swap(1,2,(swap(1,3, data_items)))
data_keys = list(data.keys())
data_keys = swap(1,2,(swap(1,3, data_keys)))
mean2 = [value[0] for value in data_items]
sd2 = [value[2] for value in data_items]
mean7 = [value[1] for value in data_items]
sd7 = [value[3] for value in data_items]
barWidth = 0.3
r1 = np.arange(len(data_keys))
r2 = [x + barWidth for x in r1]

#helper function
def stripNamesOfNumber(str):
    new_str = ""
    for n in str:
        if n.isnumeric():
            pass
        else:
            new_str += n
    return new_str

#plotting
fig = plt.figure()
ax = plt.subplot(111)
ax.bar(r1, mean2, width = barWidth, color = 'orange', edgecolor = 'black', yerr=[sd2, sd2], capsize=7, label='1 Tag', error_kw=dict(capsize=2, elinewidth=0.5))
ax.bar(r2, mean7, width = barWidth, color = 'red', edgecolor = 'black', yerr=[sd7, sd7], capsize=7, label='6 Tage', error_kw=dict(capsize=2, elinewidth=0.5))
ax.set_xticks([r +barWidth/2 for r in range(len(data_keys))])
ax.text(x=r1[0]-0.04,y=0.07,s="*",rotation=180, size=10)
ax.text(x=r2[0]-0.04,y=0.23,s="*",rotation=180, size=10)
#ax.text(x=r2[3]-0.11,y=0.72,s="*",rotation=180, size=10)
ax.set_xticklabels([stripNamesOfNumber(n) for n in data_keys], rotation=0)
ax.set_ylabel("Keimungsrate [%]")
ax.set_yticklabels([0,20,40,60,80,100])
ax.legend(frameon=False)
ax.set_ylim([0,1])
plt.savefig("derivatives.png", dpi=600, bbox_inches='tight')