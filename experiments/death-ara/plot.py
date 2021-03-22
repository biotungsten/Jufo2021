import csv
from scipy.stats import ttest_ind_from_stats
data1 = dict()
data2 = dict()
with open("aggregated.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    for idx, row in enumerate(reader):
        if idx==0:
            continue
        data1[row[0]] = [float(row[1]) , float(row[4])]
        data2[row[0]] = [float(row[2]) , float(row[3])]

ctrl1 = data1["CTRL"]
ctrl2 = data2["CTRL"]
pbonf = 0.05/(len(data1.keys())-2) #-2 because no test is effectively performed for malonic acid and CTRL
print("Results for day2")
for key,val in data1.items():
    if key == "CTRL" or key == "MA": continue
    stat = ttest_ind_from_stats(val[0], val[1], 4, ctrl1[0], ctrl1[1], 4, equal_var=False)
    data1[key] = [stat.pvalue, stat.statistic]
    print("{} \t\t has p={} and t={} \t significance:{}".format(key, round(data1[key][0], 3), round(data1[key][1], 3), data1[key][0]<pbonf))
print("\nResults for day7")
for key,val in data2.items():
    if key == "CTRL" or key == "MA": continue
    stat = ttest_ind_from_stats(val[0], val[1], 4, ctrl2[0], ctrl2[1], 4, equal_var=False)
    data2[key] = [stat.pvalue, stat.statistic]
    print("{} \t\t has p={} and t={} \t significance:{}".format(key, round(data2[key][0], 3), round(data2[key][1], 3), data2[key][0]<pbonf))
print("\nBonferroni corrected alpha is {}".format(round(pbonf, 3)))