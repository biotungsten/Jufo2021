import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
data = {}
from utils.bh import benjaminiHochberg

#run this script from experiments dir with -m option
#results are in analysis.txt

#import data
with open("derivatives/aggregated_data.csv", "r") as file:
    reader = csv.reader(file, delimiter=',')
    for line in reader:
        data[line[0]] = [float(n) for n in line[1:]]


#structure data and make vars for plotting
mean2 = [value[0] for key,value in data.items()]
sd2 = [value[2] for key,value in data.items()]
mean7 = [value[1] for key,value in data.items()]
sd7 = [value[3] for key,value in data.items()]
barWidth = 0.3
r1 = np.arange(len(data.keys()))
r2 = [x + barWidth for x in r1]

#calculate statistics
p2=[]
p7=[]
ctrl=data["CTRL"]
pbonf=0.05/len(data.items())
print("Due to bonferroni correction appropriate alpha is 0.05/n -> {}".format(pbonf))
for key, value in data.items():
    _p2 = stats.ttest_ind_from_stats(value[0], value[2], 4, ctrl[0], ctrl[2], 4, equal_var=False).pvalue
    p2.append(_p2/2)#half cause one tailed calcs
    _p7 = stats.ttest_ind_from_stats(value[1], value[3], 4, ctrl[1], ctrl[3], 4, equal_var=False).pvalue
    p7.append(_p7/2)
    t2 = stats.ttest_ind_from_stats(value[0], value[2], 4, ctrl[0], ctrl[2], 4, equal_var=False).statistic
    t7 = stats.ttest_ind_from_stats(value[1], value[3], 4, ctrl[1], ctrl[3], 4, equal_var=False).statistic
    print(f"{key} p2:{round(_p2/2,4)}, p7:{round(_p7/2,4)}; t2:{round(t2,4)}, t7:{round(t7,4)}, singifcant: 2:{_p2/2<pbonf and t2<0}/7:{_p7/2<pbonf and t2<0}") #divide by two because one tailed
holm2 = benjaminiHochberg(p2, 0.05)
holm7 = benjaminiHochberg(p7, 0.05)
print("--------------")
print("Significance after Bonferroni holm correction (same order as above, not corrected for one tailed)")
print(f"Day 2: {holm2}")
print(f"Day 7: {holm7}")

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
ax.set_xticks([r + barWidth for r in range(len(data.keys()))])
ax.text(x=r1[0]-0.11,y=0.07,s="*",rotation=180, size=10)
ax.text(x=r2[0]-0.16,y=0.23,s="*",rotation=180, size=10)
ax.text(x=r1[1]-0.11,y=0.01,s="*",rotation=180, size=10)
ax.text(x=r2[1]-0.16,y=0.25,s="*",rotation=180, size=10)
ax.text(x=r1[2]-0.11,y=0.1,s="*",rotation=180, size=10)
ax.text(x=r2[2]-0.16,y=0.41,s="*",rotation=180, size=10)
#ax.text(x=r2[3]-0.11,y=0.72,s="*",rotation=180, size=10)
ax.set_xticklabels([stripNamesOfNumber(n) for n in data.keys()], rotation=45)
ax.set_ylabel("Keimungsrate [%]")
ax.set_yticklabels([0,20,40,60,80,100])
ax.legend(frameon=False)
ax.set_ylim([0,1])
plt.savefig("derivatives/derivatives.png", dpi=600, bbox_inches='tight')