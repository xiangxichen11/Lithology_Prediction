#imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from controller.helpers import parse_zip 
from controller.helpers import visualizer
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import scipy.cluster.hierarchy as shc
from sklearn.neighbors import NearestCentroid
from yellowbrick.cluster import KElbowVisualizer
import time
import sys

labels = None
hyperparameter:int = 0

def dendrogram(x, linkage):
	plt.figure(figsize=(10, 7))
	plt.title("Customer Dendograms")
	shc.dendrogram(shc.linkage(x, method=linkage))

	plt.savefig('templates/images/hier_dendro')

def print_elbow(x):
	agglo = AgglomerativeClustering()
	fig, ax1 = plt.subplots(figsize=(9, 6)) 
	viza = KElbowVisualizer(agglo, k=(2,30), timings=False, ax=ax1) 
	viza.fit(x)
	viza.show("templates/images/hier_elbow")
	viza.poof()

	fig, ax2 = plt.subplots(figsize=(9, 6)) 
	vizb = KElbowVisualizer(agglo, k=(2,30), metric='silhouette', timings=False, ax=ax2)
	vizb.fit(x)
	vizb.show("templates/images/hier_sil")


def predict(data, x, linkage, num_clusters: int):
	global labels
	model = AgglomerativeClustering(n_clusters=num_clusters, metric='euclidean', linkage=linkage)
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


def main(file, linkage):
	global labels
	global hyperparameter
	matplotlib.use('agg') 
	hyperparameter = 0
	data, x_train = parse_zip.get_data(file)
	dendrogram(x_train, linkage)
	print_elbow(x_train)
	while (hyperparameter == 0):
		time.sleep(1)
	output = predict(data, x_train, linkage, hyperparameter)
	classify(output)
	visualizer.main(data, labels)


if __name__ == "__main__":
	main(sys.argv[1:])