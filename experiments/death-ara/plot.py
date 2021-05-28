import csv
from scipy.stats import ttest_ind_from_stats
import matplotlib.pyplot as plt

def benjaminiHochberg(pvals, globalAlpha):
    from numpy import argsort, array
    """Returns list indicating which p-values are significant after benjamini hochberg correction.
    This is also known as Holm-Bonferroni method
    Args:
        pvals ([float]): Array of all p-values
        globalAlpha (float): The global alpha ot be used.
    """
    mapOrdered = argsort(array(pvals))
    for idx, p in enumerate(mapOrdered):
        pvals[p] = pvals[p] < globalAlpha/(len(pvals)-idx)
        if pvals[p]==0:
            for j in range(idx, len(pvals)):
                pvals[mapOrdered[j]] = False
            break
    return pvals

data1 = dict()
data2 = dict()
with open("death-ara/aggregated.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    for idx, row in enumerate(reader):
        if idx==0:
            continue
        if row[0] == "MA": continue
        data1[row[0]] = [float(row[1]) , float(row[4])] #indexing follows from csv structure
        data2[row[0]] = [float(row[2]) , float(row[3])]

ctrl1 = data1["CTRL"]
p1=[]
ctrl2 = data2["CTRL"]
p2=[]
# pbonf = 0.05/(len(data1.keys())-2) #-2 because no test is effectively performed for malonic acid and CTRL

# #make p val calculations for simple bonferroni correction, halve p value cause one sided
# print("Results for day2")
# for key,val in data1.items():
#     if key == "CTRL" or key =="MA": continue
#     stat = ttest_ind_from_stats(val[0], val[1], 4, ctrl1[0], ctrl1[1], 4, equal_var=False)
#     p1.append(stat.pvalue)
#     print("{} \t\t has p={} and t={} \t significance:{}".format(key, round(stat.pvalue, 3), round(stat.statistic, 3), stat.pvalue/2<pbonf))
# print("\nResults for day7")
# for key,val in data2.items():
#     if key == "CTRL" or key == "MA": continue
#     stat = ttest_ind_from_stats(val[0], val[1], 4, ctrl2[0], ctrl2[1], 4, equal_var=False)
#     p2.append(stat.pvalue/2)
#     print("{} \t\t has p={} and t={} \t significance:{}".format(key, round(stat.pvalue/2, 3), round(stat.statistic, 3), stat.pvalue/2<pbonf))

# print("\nBonferroni corrected alpha is {}".format(round(pbonf, 3)))

# #make p val calculations for bonferroni holm correction
# holm1 = benjaminiHochberg(p1, 0.05)
# holm2 = benjaminiHochberg(p2, 0.05)
# print("\nBonferroni corrected alpha is {}".format(round(pbonf, 3)))
# print("-----------")
# print("Bonferroni-Holm significances (in same order as results)")
# print("day2", *holm1)
# print("day7", *holm2)

fig = plt.figure()
ax = plt.subplot(111)
ax.bar([n-0.2 for n in range(len(data1.values()))],[n[0] for n in data1.values()], width=0.4, color="orange", label="Tag 2", yerr=[n[1] for n in data1.values()], edgecolor = 'black', capsize=7, error_kw=dict(capsize=2, elinewidth=0.5))
ax.bar([n+0.2 for n in range(len(data2.values()))],[n[0] for n in data2.values()], width=0.4, color="red", label="Tag 7", yerr=[n[1] for n in data2.values()], edgecolor = 'black', capsize=7, error_kw=dict(capsize=2, elinewidth=0.5))
ax.set_xticks([r for r in range(len(data1.values()))])
for n in range(len(data1.values())):
    if n == 2:
        ax.text(x=n-0.25,y=list(data1.values())[n][0]+list(data1.values())[n][1]+0.03,s="*",rotation=180, size=10)
    if n in [1,2,3,4]:continue
    ax.text(x=n-0.25,y=list(data1.values())[n][0]+list(data1.values())[n][1]+0.03,s="*",rotation=180, size=10)
    ax.text(x=n+0.15,y=list(data2.values())[n][0]+list(data2.values())[n][1]+0.03,s="*",rotation=180, size=10)
ax.set_xticklabels(data1.keys(), rotation=45)
ax.set_ylabel("Überlebensrate [%]")
ax.set_yticklabels([0,20,40,60,80,100])
ax.set_title("Überlebensrate von A. thaliana")
ax.set_ylim([0,1.1])
ax.legend(frameon=False)
fig.savefig("death-ara/combined.png", dpi=600, bbox_inches='tight')
