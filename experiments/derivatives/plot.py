import csv
import numpy as np
import matplotlib.pyplot as plt
data = {}

with open("aggregated_data.csv", "r") as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        data[line[0]] = [float(n) for n in line[1:]]

mean2 = [value[0] for key,value in data.items()]
sd2 = [value[2] for key,value in data.items()]
mean7 = [value[1] for key,value in data.items()]
sd7 = [value[3] for key,value in data.items()]
barWidth = 0.3
fig = plt.figure()
ax = plt.subplot(111)
r1 = np.arange(len(data.keys()))
r2 = [x + barWidth for x in r1]

ax.bar(r1, mean2, width = barWidth, color = 'orange', edgecolor = 'black', yerr=[sd2, sd2], capsize=7, label='1 Tag', error_kw=dict(capsize=2, elinewidth=0.5))
ax.bar(r2, mean7, width = barWidth, color = 'red', edgecolor = 'black', yerr=[sd7, sd7], capsize=7, label='7 Tage', error_kw=dict(capsize=2, elinewidth=0.5))
ax.set_xticks([r + barWidth for r in range(len(data.keys()))])
ax.set_xticklabels(data.keys(), rotation=45)
ax.set_ylabel("Keimungsrate [%]")
ax.legend(frameon=False)
ax.set_ylim([0,1])
plt.savefig("derivatives.png", dpi=600, bbox_inches='tight')