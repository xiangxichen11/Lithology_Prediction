#imports
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

lithology_labels =   {  30000: 'Sandstone',        
                        65000: 'Shale',        
                        70000: 'Limestone',       
                        90000: 'Coal',        
                        93000: 'Siltstone'  }

lithology_numbers =   { 30000:   0 ,  
                        65000:   2 , 
                        70000:   5 , 
                        90000:   10, 
                        93000:   11}

lithology_colors  =   { 3:    '#FFFF00',
                        4:    '#800000',
                        6:    '#228B22',
                        7:    '#191970',
                        8:    '#6495ED' }

lith_num =          {  'Sandstone' :   3, 
                       'Siltstone' :   4,
                       'Shale'     :   6,
                       'Coal'      :   7,
                       'Limestone' :   8   }


def main(data, labels):
    matplotlib.use("agg")
    logs = data.columns[1:]
    rows,cols = 1,len(logs)+2
    fig,ax = plt.subplots(nrows=rows, ncols=cols, figsize=(12,6), sharey=True)
    colors = lithology_colors.values()
    cmap = ListedColormap(colors)
    for i in range(0, cols):
        if i < cols-2:
            print(i)
            ax[i].plot(data[logs[i]], data.DEPTH, color='blue', lw=0.5)
            ax[i].set_title('%s' % logs[i])
            ax[i].grid(which='minor', linestyle=':', linewidth='0.5', color='black')
            ax[i].set_ylim(max(data.DEPTH), min(data.DEPTH))
        if i == cols-2:
            # F = np.vstack((labels,labels)).T
            # ax[i].imshow(F, aspect='auto', extent=[0,1,max(data.DEPTH), min(data.DEPTH)], cmap = cmap)
            # ax[i].axes.get_xaxis().set_visible(False)
            # ax[i].axes.get_yaxis().set_visible(False)
            # ax[i].set_title('Lithology')
            ax[i].plot(labels, data.DEPTH, color='black', linewidth=0.5)
            ax[i].set_xlabel("Lithology",fontsize = '12' )
            ax[i].set_xlim(0, 1)
            ax[i].xaxis.label.set_color("black")
            ax[i].tick_params(axis='x', colors="black")
            ax[i].spines["top"].set_edgecolor("black")
            ax[i].set_xticks([0, 1]) 

            # for key in lithology_colors.keys():
            #     color = lithology_colors[key]
            for key in lithology_colors.keys():
                color = lithology_colors[key]
                ax[i].fill_betweenx(data.DEPTH, 0, labels, where=(labels == key), facecolor = color)
        if i == cols-1:
            ax[i].legend(lith_num.keys())

    plt.savefig("templates/images/final")