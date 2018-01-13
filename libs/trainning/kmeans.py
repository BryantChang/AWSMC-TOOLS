from sklearn.cluster import KMeans
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import numpy

dataSet = []
dataSet = numpy.loadtxt(open("/Users/bryantchang/Desktop/sample_pmc_2017-12-27-15-10-56.csv","rb"),delimiter=",",skiprows=1)
sampleCount = len(dataSet)
# print(dataSet.shape)
kmeans = KMeans(n_clusters=3, init="random").fit(dataSet)
centroids = kmeans.labels_
mark = ['or', 'ob', 'og']
for i in range(sampleCount):
    plt.plot()