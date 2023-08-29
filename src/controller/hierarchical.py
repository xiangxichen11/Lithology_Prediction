#imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from helpers import parse_zip 
from helpers import visualizer
from sklearn.preprocessing import StandardScaler
from matplotlib.colors import ListedColormap
from yellowbrick.cluster import SilhouetteVisualizer
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import scipy.cluster.hierarchy as shc
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestCentroid
from yellowbrick.cluster import KElbowVisualizer

labels = None

def dendrogram(x):
		plt.figure(figsize=(10, 7))
		plt.title("Customer Dendograms")
		dendrogram = shc.dendrogram(shc.linkage(x, method='ward'))

		plt.show()

def print_elbow(x):
	agglo = AgglomerativeClustering()
	# k is range of number of clusters.
	visualizer = KElbowVisualizer(agglo, k=(2,30), timings=False)
	# Fit data to visualizer
	visualizer.fit(x)
	# Finalize and render figure
	visualizer.show()

def print_silhouette(x):
	agglo = AgglomerativeClustering()
	# k is range of number of clusters.
	visualizer = KElbowVisualizer(agglo, k=(2,30), metric='silhouette', timings=False)
	# Fit data to visualizer
	visualizer.fit(x)
	# Finalize and render figure
	visualizer.show()

def predict(data, x, num_clusters: int):
	global labels
	model = AgglomerativeClustering(n_clusters=num_clusters, affinity='euclidean', linkage='ward')
	y_model = model.fit_predict(x)
	data_with_clusters = data.copy()
	data_with_clusters['Clusters'] = y_model

	labels = model.labels_

	clf = NearestCentroid()
	clf.fit(x, y_model)
	output = pd.DataFrame(clf.centroids_, columns=['GR', 'PE', 'DEN', 'AC'])
	output = np.round_(output, decimals=1)
	output['Lithology'] = None
	return output

def classify(output):
	for i in range(len(output)):
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
	dendrogram(x_train)
	print_elbow(x_train)
	print_silhouette(x_train)
	output = predict(data, x_train, 5)
	classify(output)
	visualizer.main(data, labels)


if __name__ == "__main__":
	main()