import csv
from scipy.stats import ttest_ind_from_stats
data = dict()
with open("aggregated.csv", 'r') as csvfile:
    reader = csv.reader(csvfile)
    for idx, row in enumerate(reader):
        if idx==0:
            continue
        data[row[0]+row[1]] = [float(row[2]) , float(row[3])]

ctrl = data["CTRLm"]
pbonf = 0.05/(len(data.keys())-4) #-4 because no test is effectively performed for malonic acid and CTRL
for key,val in data.items():
    if key in ["MAh", "MAm", "MAl", "CTRLm"]:
        continue
    stat = ttest_ind_from_stats(val[0], val[1], 4, ctrl[0], ctrl[1], 4, equal_var=False)
    data[key] = [stat.pvalue, stat.statistic]
    print("{} \t\t has p={} and t={} \t significance:{}".format(key, round(data[key][0], 3), round(data[key][1], 3), data[key][0]<pbonf))

print("Bonferroni corrected alpha is {}".format(round(pbonf, 3)))