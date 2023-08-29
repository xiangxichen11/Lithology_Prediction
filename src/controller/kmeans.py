#imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from helpers import parse_zip 
from helpers import visualizer
from sklearn.cluster import KMeans
from yellowbrick.cluster import SilhouetteVisualizer

labels = None

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
	plt.show()

def print_silhouette(x):
	fig, ax = plt.subplots(3, 2, figsize=(15,8))
	for i in [2, 3, 4, 5, 6]:
		km = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=100, random_state=42)
		q, mod = divmod(i, 2)

		visualizer = SilhouetteVisualizer(km, colors='yellowbrick', ax=ax[q-1][mod])
		visualizer.fit(x)
		print("For", i, "clusters,  the average Silhouette score is: ", visualizer.silhouette_score_)

	plt.show()
    

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

def main():
	global labels
	data, x_train = parse_zip.get_data("../../data/100163203803W400.las")
	print_elbow(data)
	print_silhouette(data)
	output = predict(data, x_train, 4)
	print(output)
	classify(output)
	visualizer.main(data, labels)


if __name__ == "__main__":
	main()




