import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Import frequency table
freqTable = pd.read_csv("NormalizedRelativeFrequency.csv",header=0,index_col=0,sep='\t')

#Set parameters of the ax plot 
a4_dims = (11.7, 8.27)
plt.rcParams.update({'font.size': 16})

#Plot and save
cmap_mpl = plt.get_cmap("viridis")
cmap_mpl = cmap_mpl.reversed()
fig, ax = plt.subplots(figsize=a4_dims) 
fig = sns.heatmap(freqTable,cmap=cmap_mpl)
fig.figure.savefig("NormalizedRelativeFrequency.heatmap.viridis.pdf")

#Plot and save 
cmap_mpl = plt.get_cmap("YlGnBu")
fig, ax = plt.subplots(figsize=a4_dims)
fig = sns.heatmap(freqTable,cmap=cmap_mpl)
fig.figure.savefig("NormalizedRelativeFrequency.heatmap.ylgnbu.pdf")
