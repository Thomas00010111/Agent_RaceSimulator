'''
Created on Feb 11, 2013

@author: mrfish
'''
import numpy

import Environment.RepresentationEnvironment.SOM.DisplayNodePositionsAndV_3D as DisplayNodePositionsAndV
import Environment.RepresentationEnvironment.SOM.StateSpaceDiscretization as StateSpaceDiscretization


testNodes = StateSpaceDiscretization.StateSpaceDiscetization(15*15*15)
nodes = testNodes.getNodePositions()
for i in range(0,nodes.shape[0]):
    print "node:  ",i, "  ", nodes[i]
V = numpy.zeros(nodes.shape[0])

#node:   0    [ 0.  0.  0.]
V[0] = 1
#V[0] is at X,Y = 0;  Theta = 1
#V[14] = 1

#node:   210    [ 0.  1.  0.]
V[210] = 1
#node:   660   [ 0.14285714  1.          0. ]
V[660]=1


#draw nodes
graph = DisplayNodePositionsAndV.DisplayNodePositionsAndV_3D(nodes)
scalars = V.reshape(1,V.shape[0])[0]
print "scalars:", scalars 
graph.update(nodes, scalars)
graph.show()




        
