import numpy as numpy
import math as math
# import matrix
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# matplotlib inline
from sklearn.decomposition import PCA

# dataSet = []
# dataSet = numpy.loadtxt(open("/Users/bryantchang/Desktop/study/Research/experiment/for_remote/sample_pmc_2018-01-03-10-45-25.csv","rb"),delimiter=",",skiprows=1)
# pca=PCA(n_components='mle')
# newData = pca.fit(dataSet)
# print(pca.explained_variance_ratio_)
vector_kmeans1 = numpy.mat([13.04,10.00,76.00,6299.33,1.73])
vector_kmeans2 = numpy.mat([13.04,9.00,77.00,6228.13,1.73])
vector_lr = numpy.mat([15.07,8.00,83.00,7885.65,1.77])
vector_shortestpaths = numpy.mat([37.68,11.00,63.00,3453.66,1.14])


dis_manhaton_kmeans1_kmeans2 = numpy.sum(numpy.abs(vector_kmeans1-vector_kmeans2))
dis_manhaton_kmeans1_lr = numpy.sum(numpy.abs(vector_kmeans1-vector_lr))
dis_manhaton_kmeans1_shortestpaths = numpy.sum(numpy.abs(vector_kmeans1-vector_lr))


dis_ou_kmeans1_kmeans2 = numpy.sqrt(numpy.sum(numpy.square(vector_kmeans1 - vector_kmeans2)))
dis_ou_kmeans1_lr = numpy.sqrt(numpy.sum(numpy.square(vector_kmeans1 - vector_lr)))
dis_ou_kmeans1_shortestpaths = numpy.sqrt(numpy.sum(numpy.square(vector_kmeans1 - vector_shortestpaths)))

dis_qie_kmeans1_kmeans2=numpy.max(numpy.abs(vector_kmeans1-vector_kmeans2))
dis_qie_kmeans1_lr=numpy.max(numpy.abs(vector_kmeans1-vector_lr))
dis_qie_kmeans1_shortestpath=numpy.max(numpy.abs(vector_kmeans1-vector_shortestpaths))
# dis_cos_kmeans1_kmeans2 = numpy.dot(vector_kmeans1,vector_kmeans2)/(numpy.linalg.norm(vector_kmeans1)*numpy.linalg.norm(vector_kmeans2))
# dis_cos_kmeans1_lr = numpy.dot(vector_kmeans1,vector_lr)/(numpy.linalg.norm(vector_kmeans1)*numpy.linalg.norm(vector_lr))
# dis_cos_kmeans1_shortestpaths = numpy.dot(vector_kmeans1,vector_shortestpaths)/(numpy.linalg.norm(vector_kmeans1)*numpy.linalg.norm(vector_shortestpaths))

print(dis_manhaton_kmeans1_kmeans2, dis_manhaton_kmeans1_lr, dis_manhaton_kmeans1_shortestpaths)
print(dis_ou_kmeans1_kmeans2, dis_ou_kmeans1_lr, dis_ou_kmeans1_shortestpaths)
print(dis_qie_kmeans1_kmeans2, dis_qie_kmeans1_lr, dis_manhaton_kmeans1_shortestpaths)