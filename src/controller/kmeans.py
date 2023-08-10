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

def get_keys():
    las = lasio.read("./data/100163203803W400.las")
    mnemonic = las.keys()
    return mnemonic

def get_data():
    data = np.loadtxt("data parameter", skiprow = X)
    data = pd.DataFrame(data, columms=get_keys())
    return data

def transform_data():
    x = get_data().iloc[:,1:6]
    x.drop('NPHI', inplace=True, axis=1)
    return x

def print_wcss():
    wcss = []
    for i in range(1, 11):
			kmeans = KMeans(n_clusters = i, init='k-means++', random_state = 42, n_init=10)
			kmeans.fit(x)
			wcss.append(kmeans.inertia_)
    
		plt.plot(range(1, 11), wcss)
		plt.xlabel('Number of clusters')
		plt.ylabel('WCSS') 	
    
def print_silhouette():
	fig, ax = plt.subplots(3, 2, figsize=(15,8))
	for i in [2, 3, 4, 5, 6]:
    km = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=100, random_state=42)
    q, mod = divmod(i, 2)
    
    visualizer = SilhouetteVisualizer(km, colors='yellowbrick', ax=ax[q-1][mod])
    visualizer.fit(x) 
    print("For", i, "clusters,  the average Silhouette score is: ", visualizer.silhouette_score_)

def train():
	kmeans = KMeans(n_clusters = 4, init = "k-means++", random_state = 42, n_init = 10)
	y_kmeans = kmeans.fit_predict(x)
	data_with_clusters = data.copy()
	data_with_clusters['Clusters'] = y_kmeans
    


    


