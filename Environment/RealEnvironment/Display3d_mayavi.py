'''
Created on Feb 11, 2013

@author: mrfish
'''
import mayavi.mlab
import mdp.nodes
import numpy
from reportlab.lib.colors import transparent

import Environment.RepresentationEnvironment.SOM.MyGrowingNeuralGasNode as MyGrowingNeuralGasNode 


def findNonzeroCoord(startPos, x, step=1):
        """ the first three values are sensor measurements """
        i = startPos
        while (x[i,0:3] == numpy.array([0.0,0.0,0.0])).all():
            i+=step
        return i        
 

white = (1, 1, 1)
black = (0, 0, 0)
red = (1, 0, 0)        
        
x_temp= numpy.load(open("sensors.pkl", 'r'))

firstSensorValue=findNonzeroCoord(0,x_temp)
lastSensorValue = findNonzeroCoord(len(x_temp)-1,x_temp,-1)

x = x_temp[firstSensorValue:lastSensorValue, 0:3]

#numpy.save(open("sensors_test.pkl", 'wb'), x)


print "number of sensor measurements: ", len(x)
print x

#train
#nodes = numpy.zeros((2, 3))
#nodes = numpy.random.rand(4,3)
nodes = numpy.array([[0.0, 0.0, 0.0],[0.0, 1.0, 0.0]])
gng = MyGrowingNeuralGasNode.MyGrowingNeuralGasNode(start_poss = nodes, max_nodes=10)
#[gng.addNode(node) for node in nodes[2:]]
#gng = mdp.nodes.GrowingNeuralGasNode(start_poss = nodes, max_nodes=5)

STEP = 1
for i in range(0,x.shape[0],STEP): 
    gng.train(x[i:i+STEP])
    print "i: ", i, "   nodes: ", len (gng.graph.nodes)
gng.stop_training()

print "Number of nodes in network: ", len (gng.graph.nodes)    

# plot connections between nodes
headTail = [ht.get_ends() for ht in gng.graph.edges]
for ht in headTail:
        #plot line between head and tail
        xHeadTail = [ht[0].data.pos[0], ht[1].data.pos[0]]
        yHeadTail = [ht[0].data.pos[1], ht[1].data.pos[1]]
        zHeadTail = [ht[0].data.pos[2], ht[1].data.pos[2]]
        mayavi.mlab.plot3d(xHeadTail, yHeadTail, zHeadTail, tube_radius=0.01, color=red, transparent=True, opacity=0.3)

# plot nodes and sensor values       
nodePosX = [node.data.pos[0] for node in gng.graph.nodes]
nodePosY = [node.data.pos[1] for node in gng.graph.nodes]
nodePosZ = [node.data.pos[2] for node in gng.graph.nodes]
        
mayavi.mlab.points3d(nodePosX, nodePosY, nodePosZ, transparent=True, opacity=0.3)
mayavi.mlab.points3d(nodePosX, nodePosY, nodePosZ, scale_factor=.01, color=red)
mayavi.mlab.points3d(x[:,0], x[:,1], x[:,2], scale_factor=.01, color=black)

# plot axes
mayavi.mlab.axes()
mayavi.mlab.xlabel('left')
mayavi.mlab.ylabel('front')
mayavi.mlab.zlabel('right')
mayavi.mlab.outline()
mayavi.mlab.colorbar()
mayavi.mlab.show()

#save gng
#nodePos = [node.data.pos for node in gng.graph.nodes]
#numpy.save(open("gng_nodePos_Test.pkl", "wb"), numpy.array(nodePos))

        
