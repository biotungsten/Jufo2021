import csv
from scipy.stats import ttest_ind_from_stats
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
data = dict()
with open("aggregated.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    for idx, row in enumerate(reader):
        if idx==0:
            continue
        data[row[0]+row[1]] = [float(row[2]) , float(row[3])]

ctrl = data["CTRLm"]
p = []
pbonf = 0.05/(len(data.keys())-4) #-4 because no test is effectively performed for malonic acid and CTRL
for key,val in data.items():
    if key in ["MAh", "MAm", "MAl", "CTRLm"]:
        continue
    stat = ttest_ind_from_stats(val[0], val[1], 4, ctrl[0], ctrl[1], 4, equal_var=False)
    p.append(stat.pvalue)
    data[key] = [stat.pvalue, stat.statistic]
    print("{} \t\t has p={} and t={} \t significance:{}".format(key, round(data[key][0], 3), round(data[key][1], 3), data[key][0]<pbonf))
holm = benjaminiHochberg(p, 0.05)
print("\nBonferroni corrected alpha is {}".format(round(pbonf, 3)))
print("-----------")
print("Bonferroni-Holm significances (in same order as results)")
print(*holm)