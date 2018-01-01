from sklearn.cluster import KMeans
from sklearn.externals import joblib
import numpy

dataSet = []
dataSet = numpy.loadtxt(open("/Users/bryantchang/Desktop/sample_pmc_2017-12-27-15-10-56.csv","rb"),delimiter=",",skiprows=1)
# print(dataSet.shape)
kmeans = KMeans(n_clusters=3).fit(dataSet)
print(kmeans.cluster_centers_)

