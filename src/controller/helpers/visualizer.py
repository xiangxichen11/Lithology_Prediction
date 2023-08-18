#imports
import numpy as np
import pandas as pd
import lasio 
from las_py import Laspy
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from yellowbrick.cluster import SilhouetteVisualizer
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler
from yellowbrick.cluster import KElbowVisualizer


def main(data, labels):
    logs = data.columns[1:]
    rows,cols = 1,6
    fig,ax = plt.subplots(nrows=rows, ncols=cols, figsize=(12,6), sharey=True)
    #colors = lithology_colors.values()
    #cmap = ListedColormap(colors)
    plt.suptitle('Well-100163203803W400', size=15)
    for i in range(cols):
        if i < cols-1:
            ax[i].plot(data[logs[i]], data.DEPTH, color='blue', lw=0.5)
            ax[i].set_title('%s' % logs[i])
            ax[i].grid(which='minor', linestyle=':', linewidth='0.5', color='black')
            ax[i].set_ylim(max(data.DEPTH), min(data.DEPTH))
        if i == cols-1:
            F = np.vstack((labels,labels)).T
            ax[i].imshow(F, aspect='auto', extent=[0,1,max(data.DEPTH), min(data.DEPTH)], cmap = 'terrain')
            ax[i].axes.get_xaxis().set_visible(False)
            ax[i].axes.get_yaxis().set_visible(False)
            ax[i].set_title('Lithology')
    plt.show()