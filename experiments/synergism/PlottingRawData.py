import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#read in data
df = pd.read_csv("data/combinations.csv")
df2 = pd.read_csv("data/single_doses.csv")

#process data
df["germination"] = df["day7"]/df["appl"]
mean_germ = df.groupby(["combination", "concs"]).mean().reset_index()
std_germ = df.groupby(["combination", "concs"]).std().reset_index()
df2["germination"] = df2["day7"]/df["appl"]
mean_germ2 = df2.groupby("combination").mean().reset_index()
std_germ2 = df2.groupby("combination").std().reset_index()

#data extraction
means = mean_germ.loc[mean_germ['combination'] == "V"][["germination", "concs"]]
means.columns = ["mean", "combination"]
stds = std_germ.loc[std_germ['combination'] == "V"][["germination", "concs"]]
stds.columns = ["std", "combination"]
combined = pd.merge(means, stds, how="inner")
means2 = mean_germ2.loc[mean_germ2['combination'].isin(["C90", "R120", "C50", "R50", "C30", "R30"])][["germination", "combination"]]
means2.columns = ["mean", "combination"]
stds2 = std_germ2.loc[std_germ2['combination'].isin(["C90", "R120", "C50", "R50", "C30", "R30"])][["germination", "combination"]]
stds2.columns = ["std", "combination"]
singles = pd.merge(means2, stds2, how="inner")
combined = combined.append(singles)

#plotting
barWidth = 0.3
fig = plt.figure()
ax = plt.subplot(111)
r1 = np.arange(11)
means = combined["mean"]
sd = combined["std"]
ax.bar(r1, means, width = barWidth, color = 'orange', edgecolor = 'black', yerr=[sd, sd], capsize=11, label='6 Tage', error_kw=dict(capsize=2, elinewidth=0.5))
ax.set_xticks([r for r in range(11)])
ax.set_xticklabels(["ll","lm", "ml", "mm", "hh", "C-30", "C-50", "C-90", "R-120", "R-30", "R-50"], rotation=45)
ax.set_ylabel("Keimungsrate [%]")
ax.text(1.5,-0.2, "CA-RE")
trans = ax.get_xaxis_transform()
ax.plot([-.3,4.2],[-.13,-.13], color="k", linewidth=.5, transform=trans, clip_on=False)
ax.set_yticklabels([0,20,40,60,80,100])
ax.set_ylim([0,1])
plt.savefig("germination.eps", dpi=600, bbox_inches='tight')
