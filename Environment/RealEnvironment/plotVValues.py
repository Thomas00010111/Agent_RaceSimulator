import numpy
import sys

import matplotlib.pyplot as plt


#sys.stdout = open('output_plotVValues.txt', 'w')

# f = open('StepsVsGoal.txt', 'rb')
# lines = f.readlines()
# splitInto = lines[0].strip().count(";") + 1
# data = [line.strip().split(";",splitInto) for line in lines]
# f.close()
# 
# print data

# #add a plot
# y = [float(y)+10 for y in yLst] 
# plt.scatter(x, y)

filename = "VLog_Agent2.npy"
try:
    vValuesAndState = numpy.load(filename)
except:
    print "Could not open file: ", filename
    sys.exit()
    
print vValuesAndState

maxState = max(vValuesAndState[:,0]) + 1
yComplete = numpy.zeros((maxState, vValuesAndState.shape[0]))
y=numpy.arange(0,maxState)
for index,v in enumerate(vValuesAndState):
    y[v[0]]=v[0] + v[1]
    yComplete[:,index]=y

x=numpy.arange(0,vValuesAndState.shape[0])
for y in yComplete:
    plt.plot(x, y,'-')
    
plt.show()