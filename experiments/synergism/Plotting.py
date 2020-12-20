#!/usr/bin/env python
# coding: utf-8

# In[7]:


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# In[15]:


df = pd.read_csv("prediction-dev.csv")
aij = np.loadtxt(open("aij.csv", "r"), delimiter=",")
drugs = ["CA", "RE", "HQ", "MA"]


# In[149]:


fig, axs = plt.subplots(nrows=1, ncols=2)

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=1.2, hspace=None)
cax = fig.add_axes([0.40, 0.31, 0.03, 0.37])
ax=axs[0]
img =ax.imshow(np.log10(aij), cmap='inferno')
fig.colorbar(img, cax=cax, orientation='vertical')

ax.set_xticks(range(0,4))
ax.set_xticklabels(drugs)
ax.set_yticks(range(0,4))
ax.set_yticklabels(drugs)
ax.text(-1.8,0,"a)", fontweight="bold")
ax=axs[1]
ax.set_aspect('equal')

ax.plot(df["experiment"], df["model"], "b+", ms=2.5, mew=0.5)
ax.plot(df["experiment"], df["bliss"], "ro", ms=2.5, fillstyle='none', mew=0.5)
ax.plot([0,1], [0,1], "k", linewidth=0.5)
ax.set_xlim(xmin=0, xmax=1)
ax.set_ylim(ymin=0, ymax=1)
ax.set_xlabel("Experiment")
ax.set_ylabel("Modell")
ax.text(-0.5,0.9,"b)", fontweight="bold")
fig.savefig("combined.png", dpi=400, bbox_inches="tight")

