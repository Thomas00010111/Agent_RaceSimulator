'''
Created on Feb 11, 2013

@author: mrfish
'''
import itertools
import mayavi.mlab
import numpy
from reportlab.lib.colors import transparent
import time


def findNonzeroCoord(startPos, x, step=1):
        """ the first three values are sensor measurements """
        i = startPos
        while (x[i,0:3] == numpy.array([0.0,0.0,0.0])).all():
            i+=step
        return i        
 

white = (1, 1, 1)
black = (0, 0, 0)
red = (1, 0, 0)        

def updateWithNumpy2():
    
    import Environment.RepresentationEnvironment.SOM.Scatterplot4D as Scatterplot4D       
    upper = 7
    DimensionData = 3
    nodes = numpy.array([x for x in itertools.product(range(upper), repeat=DimensionData)])
    nodes = nodes/float(upper-1)
    print "nodes: ", nodes
                    
    graph1=Scatterplot4D.Scatterplot4D(nodes)

    # plot nodes and sensor values       
    s = numpy.ones(nodes.shape[0])
    s[0] = 0.0
    s[10] = 0.5
    print "scalars: ", s

    for i in range(2,4):
        time.sleep(2)
        nodes = nodes/float(i)
        print "nodes:", nodes
        s = s/float(i)
        print "scalars: ", s
        graph1.update(nodes, s)
        
    graph1.show()


def updateWithNumpy():        
    upper = 7
    DimensionData = 3
    nodes = numpy.array([x for x in itertools.product(range(upper), repeat=DimensionData)])
    nodes = nodes/float(upper-1)
    print "nodes: ", nodes
    #print "nodes[:,0]: ", nodes[:,0]
            
    # plot nodes and sensor values       
    s = numpy.ones(nodes.shape[0])
    s[0] = 0.0
    s[10] = 0.5
    print "scalars: ", s
            
    graph1=mayavi.mlab.points3d(nodes[:,0], nodes[:,1], nodes[:,2], s, transparent=True, scale_factor=.05, opacity=0.3)
    
    # plot axes
    mayavi.mlab.axes()
    mayavi.mlab.xlabel('left')
    mayavi.mlab.ylabel('front')
    mayavi.mlab.zlabel('right')
    mayavi.mlab.outline() 
    mayavi.mlab.colorbar()
    
    for i in range(2,4):
        time.sleep(2)
        nodes = nodes/float(i)
        print "nodes:", nodes
        s = s/float(i)
        print "scalars: ", s
        graph1.mlab_source.set(points=nodes, scalars=s)
        
    mayavi.mlab.show()

        
        
def updateWithLists():        
    upper = 7
    DimensionData = 3
    numberOfStates = 7*7*7
    nodes = numpy.array([x for x in itertools.product(range(upper), repeat=DimensionData)])
    nodes = nodes/float(upper-1)
    print "nodes: ", nodes
            
    # plot nodes and sensor values       
    nodePosX = [node[0] for node in nodes]
    nodePosY = [node[1] for node in nodes]
    nodePosZ = [node[2] for node in nodes]
    
    s = [1.0]*len(nodePosX)
    s[0] = 0.0
    s[10] = 0.5
    print "scalars: ", s
            
    graph1=mayavi.mlab.points3d(nodePosX, nodePosY, nodePosZ, s, transparent=True, scale_factor=.05, opacity=0.3)
    #graph2=mayavi.mlab.points3d(nodePosX, nodePosY, nodePosZ, scale_factor=.01, color=red)
    #mayavi.mlab.points3d(x[:,0], x[:,1], x[:,2], scale_factor=.01, color=black)
    
    # plot axes
    mayavi.mlab.axes()
    mayavi.mlab.xlabel('left')
    mayavi.mlab.ylabel('front')
    mayavi.mlab.zlabel('right')
    mayavi.mlab.outline() 
    mayavi.mlab.colorbar()
    #mayavi.mlab.show()
    
    
    for i in range(2,4):
        time.sleep(2)
        nodes = nodes/float(i)
        print "nodes:", nodes
        s[:] = [x / float(i) for x in s]
        print "scalars: ", s
        #print scalars
    #    nodePosX = [node[0] for node in nodes]
    #    nodePosY = [node[1] for node in nodes]
    #    nodePosZ = [node[2] for node in nodes]
                  
        graph1.mlab_source.set(points=nodes, scalars=s)
        
    mayavi.mlab.show()



if __name__ == '__main__':
    updateWithNumpy2()
        
