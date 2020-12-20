#!/usr/bin/env python
# coding: utf-8

# In this notebook the greenhouse data on Resorcinol (RE), Catechol (CAT or CA), Tropic acid (TA) and Hydroquinone (HY) will be analysed.

# # Imports

# In[41]:


import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import scipy.optimize as opt


# # Global definitions

# In[40]:


DATA_DIR = "/Users/David_Sauer/Documents/Data/Greenhouse_countings/january-february/plants.csv"
HEADERS = ["experiment", "solution", "plant", "internal_reproduction", "usable", "total_seeds", "germination_1", "germination_2", "biomass", "notes", "external_reproduction"]
SUBSTANCES = ["Catechol", "Resorcinol", "Hydroquinone", "Tropic acid"]
SUBSTANCES_SHORT = ["C", "R", "H", "TA"]
EXPERIMENT_NAMES = ["CATL1", "CATL2", "CATL3", "REL1", "REL2", "REL3", "HYL1", "HYL2", "HYL3", "TAL1", "TAL2", "TAL3"]
df = pd.read_csv(DATA_DIR, names=HEADERS, sep=";") 
df = df.loc[df["experiment"].isin(EXPERIMENT_NAMES)]

def hill(conc, ec50, n):
    return 1/(1+(conc/ec50)**n)


# # Code

# In[47]:


fig, axs = plt.subplots(2,2, squeeze=True, sharey=True)
ctrls=[]
for idx, ax in enumerate(axs.flatten()):
    ec50_estimate = 60
    max_val = 120
    text_offset = 1
    if idx==3:
        ec50_estimate = 25
        max_val = 50
        text_offset = 0.5
    local_df = df.loc[df["experiment"].isin(EXPERIMENT_NAMES[idx*3:(idx+1)*3])]
    local_control = local_df.loc[local_df["solution"] == "CTRL"]
    control_germ_percentage = np.mean(local_control["germination_2"])/np.mean(local_control["total_seeds"])
    local_data = local_df.loc[local_df["solution"] != "CTRL"]
    local_data.loc[:, ("solution")] = [n.split(SUBSTANCES_SHORT[idx])[1] for n in local_data.loc[:, ("solution")]]
    concs = local_data["solution"].unique()
    true_concs = [int(n) for n in local_data["solution"]]
    effects = []
    true_effects = [row["germination_2"]/row["total_seeds"] for index, row in local_data.iterrows()]
    errors = []
    for conc in concs:
        conc_data =local_data.loc[local_data["solution"] == conc]
        local_effects = conc_data["germination_2"]/conc_data["total_seeds"]
        effect = np.mean(conc_data["germination_2"])/np.mean(conc_data["total_seeds"])
        errors.append(stats.sem(local_effects))
        effects.append(effect)
    print(errors)
    concs = [int(n) for n in concs]
    params, pcov = opt.curve_fit(hill, true_concs, true_effects, p0=(ec50_estimate,1))
    ax.plot([0,max_val],[control_germ_percentage, control_germ_percentage], color="grey", linewidth=0.5, alpha=0.5, label="CTRL")
    ax.plot(np.linspace(0,ec50_estimate*2, num=100), [hill(n, params[0], params[1]) for n in np.linspace(0,ec50_estimate*2, num=100)], "--r", linewidth=0.7, label="model")
    ax.errorbar(concs, effects, yerr=errors, linestyle='None', marker="x", color="k", elinewidth=0.5, capsize=2, markersize=3, mew=0.5, label="measurements")
    ax.set_title(SUBSTANCES[idx])
    ax.set_xlim([0, max_val])
    ax.set_ylim([0,1])
    pcov = np.sqrt(np.diag(pcov))
    ctrls.append(control_germ_percentage)
    ax.text(max_val+text_offset, 0.25, "D0:{:03.2f}±{:03.2f}, n:{:03.2f}±{:03.2f}".format(params[0],pcov[0],params[1],pcov[1]), rotation=-90, fontsize=5)
    if idx==3:
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc=1, bbox_to_anchor=(1.23, 0.975), fontsize=7, frameon=False, shadow=False)
print(np.mean(control_germ_percentage))
print(ctrls)
plt.tight_layout()

fig.add_subplot(111, frame_on=False)
plt.tick_params(labelcolor="none", bottom=False, left=False)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.25, hspace=0.45)
plt.xlabel("concentration [mM]", labelpad=10)
plt.ylabel("germination rate", labelpad=20)
fig.savefig("figure.png", dpi=600, bbox_inches='tight')

