#imports
import numpy as np
import matplotlib.pyplot as plt


def main(data, labels):
    logs = data.columns[1:]
    print(logs)
    rows,cols = 1,len(logs)+1
    fig,ax = plt.subplots(nrows=rows, ncols=cols, figsize=(12,6), sharey=True)
    #colors = lithology_colors.values()
    #cmap = ListedColormap(colors)
    plt.suptitle('Well-100163203803W400', size=15)
    for i in range(0, cols):
        if i < cols-1:
            print(i)
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