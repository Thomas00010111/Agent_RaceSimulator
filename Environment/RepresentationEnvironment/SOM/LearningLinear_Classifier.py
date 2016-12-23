'''
Created on Jun 23, 2013

@author: mrfish
'''
import matplotlib.pyplot as plt
import numpy

import Environment.RepresentationEnvironment.SOM.MyGrowingNeuralGasNode as MyGrowingNeuralGasNode
from sklearn.svm import LinearSVC
from sklearn.datasets import load_iris


iris = load_iris()

#print iris.data
#print iris.target

fig = plt.figure()
ax = fig.add_subplot(111)

s1=numpy.random.normal(1.0, 0.05, [10,2])
s2=numpy.random.normal(4.4, 0.01, [10,2])

trainlabels1 = numpy.zeros((s1.shape[0], 1))
trainlabels2 = numpy.ones((s2.shape[0], 1))

trainData = numpy.append(s1,s2, axis=0)
trainLabels = numpy.append(trainlabels1, trainlabels2, axis=0)
# s3=s2

# train the linear regression clasifier
print("[INFO] training Linear SVM classifier...")
model = LinearSVC()

print trainData
model.fit(trainData, numpy.ravel(trainLabels))

print model.predict([[3.0, 2.0]])
    
    
    