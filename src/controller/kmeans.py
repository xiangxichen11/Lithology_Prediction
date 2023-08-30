#imports
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from controller.helpers import parse_zip 
from controller.helpers import visualizer
from sklearn.cluster import KMeans
from yellowbrick.cluster import SilhouetteVisualizer
import os
import time

labels = None
hyperparameter: int = 0

def transform_data(data):
    x = data.iloc[:,1:6]
    return x

def print_elbow(x):
	wcss = []
	for i in range(1, 11):
		kmeans = KMeans(n_clusters = i, init='k-means++', random_state = 42, n_init=10)
		kmeans.fit(x)
		wcss.append(kmeans.inertia_)

	plt.plot(range(1, 11), wcss)
	plt.xlabel('Number of clusters')
	plt.ylabel('WCSS')
	plt.savefig('../frontend/images/k-means_elbow')

def print_silhouette(x):
	fig, ax = plt.subplots(3, 2, figsize=(15,8))
	for i in [2, 3, 4, 5, 6]:
		km = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=100, random_state=42)
		q, mod = divmod(i, 2)

		visualizer = SilhouetteVisualizer(km, colors='yellowbrick', ax=ax[q-1][mod])
		visualizer.fit(x)
		print("For", i, "clusters,  the average Silhouette score is: ", visualizer.silhouette_score_)

	plt.savefig('../frontend/images/k-means_sil')
    

def predict(data, x, num_clusters: int):
	global labels
	kmeans = KMeans(n_clusters = num_clusters, init = "k-means++", random_state = 42, n_init = 10)
	kmeans = kmeans.fit(x)
  
	# include Lithology column in data
	labels = kmeans.labels_

	output = pd.DataFrame(kmeans.cluster_centers_, columns=['GR', 'PE', 'DEN', 'AC'])
	output = np.round_(output, decimals=2)

	return output

def classify(output):
	for i in range(0, len(output)):
		if (output.at[i, 'GR'] < 45 and 2.0 <= output.at[i, 'DEN'] <= 2.4):
			output.at[i, 'Lithology'] = 'Sandstone'
		elif (output.at[i, 'GR'] < 80 and output.at[i, 'DEN'] < 2.0):
			output.at[i, 'Lithology'] = 'Coal'
		elif (output.at[i, 'GR'] < 80 and output.at[i, 'DEN'] > 2.45):
			output.at[i, 'Lithology'] = 'Limestone'
		elif (45 <= output.at[i, 'GR'] <= 80  and 2.0 <= output.at[i, 'DEN'] <= 2.4):
			output.at[i, 'Lithology'] = 'Siltstone'
		elif (output.at[i, 'GR'] >  80):
			output.at[i, 'Lithology'] = 'Shale'

def main(file):
	global labels
	global hyperparameter
	matplotlib.use('agg')
	data, x_train = parse_zip.get_data(file)
	print(data)
	print_elbow(data)
	print_silhouette(data)
	while(hyperparameter == 0):
		time.sleep(5)
	
	output = predict(data, x_train, hyperparameter)
	classify(output)
	visualizer.main(data, labels)
hyperparameter = 0


if __name__ == "__main__":
	import sys
	main(sys.argv[1:])
	#main()




