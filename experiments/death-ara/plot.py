import csv
from scipy.stats import ttest_ind_from_stats
import matplotlib.pyplot as plt
from utils.bh import benjaminiHochberg

#run this script from experiments dir with -m option
#results are in analysis.txt

#import data
data1 = dict()
data2 = dict()
with open("death-ara/aggregated.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    for idx, row in enumerate(reader):
        if idx==0: #skip colnames
            continue
        data1[row[0]] = [float(row[1]) , float(row[4])] #indexing follows from csv structure
        data2[row[0]] = [float(row[2]) , float(row[3])]

#store control data explicitly
ctrl1 = data1["CTRL"]
ctrl2 = data2["CTRL"]

#create empty lists for storing p-values
p1=[]
p2=[]

#calculate bonferroni corrected alpha
pbonf = 0.05/(len(data1.keys())-2) #-2 because no test is effectively performed for malonic acid and CTRL

#make p val calculations for simple bonferroni correction
print("Results for day2")
for key,val in data1.items():
    if key == "CTRL" or key == "MA": continue
    stat = ttest_ind_from_stats(val[0], val[1], 4, ctrl1[0], ctrl1[1], 4, equal_var=False)
    p1.append(stat.pvalue)
    print("{} \t\t has p={} and t={} \t significance:{}".format(key, round(stat.pvalue, 3), round(stat.statistic, 3), stat.pvalue<pbonf))

print("\nResults for day7")
for key,val in data2.items():
    if key == "CTRL" or key == "MA": continue
    stat = ttest_ind_from_stats(val[0], val[1], 4, ctrl2[0], ctrl2[1], 4, equal_var=False)
    p2.append(stat.pvalue)
    print("{} \t\t has p={} and t={} \t significance:{}".format(key, round(stat.pvalue, 3), round(stat.statistic, 3), stat.pvalue<pbonf))

print("\nBonferroni corrected alpha is {}".format(round(pbonf, 3)))

#make p val calculations for bonferroni holm correction
holm1 = benjaminiHochberg(p1, 0.05)
holm2 = benjaminiHochberg(p2, 0.05)
print("-----------")
print("Bonferroni-Holm significances (in same order as results)")
print("day2", *holm1)
print("day7", *holm2)

#plot results
fig = plt.figure()
ax = plt.subplot(111)
ax.bar([n for n in range(len(data1.values()))],[n[0] for n in data1.values()], color="orange", yerr=[n[1] for n in data1.values()], edgecolor = 'black', capsize=7, label='1 Tag', error_kw=dict(capsize=2, elinewidth=0.5))
ax.set_xticks([r for r in range(len(data1.values()))])
ax.set_xticklabels(data1.keys(), rotation=45)
ax.set_ylabel("Überlebensrate [%]")
ax.set_yticklabels([0,20,40,60,80,100])
ax.set_title("Überlebensrate von A. thaliana nach 2 Tagen")
ax.set_ylim([0,1.1])
fig.savefig("death-ara/day2.png", dpi=600, bbox_inches='tight')

fig = plt.figure()
ax = plt.subplot(111)
ax.bar([n for n in range(len(data2.values()))],[n[0] for n in data2.values()], color="orange", yerr=[n[1] for n in data2.values()], edgecolor = 'black', capsize=7, label='1 Tag', error_kw=dict(capsize=2, elinewidth=0.5))
ax.set_xticks([r for r in range(len(data2.values()))])
ax.set_xticklabels(data2.keys(), rotation=45)
ax.set_ylabel("Überlebensrate [%]")
ax.set_yticklabels([0,20,40,60,80,100])
ax.set_title("Überlebensrate von A. thaliana nach 7 Tagen")
ax.set_ylim([0,1.1])
fig.savefig("death-ara/day7.png", dpi=600, bbox_inches='tight')