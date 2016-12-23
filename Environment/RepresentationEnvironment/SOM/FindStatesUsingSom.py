'''
Created on Jun 23, 2013

@author: mrfish
'''
import matplotlib.pyplot as plt
import numpy

import Environment.RepresentationEnvironment.SOM.MyGrowingNeuralGasNode as MyGrowingNeuralGasNode 


UNDEFINED = -1

# class _NGNodeData(object):
#     """Data associated to a node in a Growing Neural Gas graph."""
#     def __init__(self, pos, label, error=0.0, hits=0):
#         # reference vector (spatial position)
#         self.pos = pos
#         # cumulative error
#         self.cum_error = error
#         self.hits = 0
#         self.label = label
        
if __name__=="__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    s1=numpy.random.normal(1.0, 0.05, [100,1])
    s2=numpy.random.normal(5.5, 0.05, [100,1])

#    s3 = numpy.append(s1,s2, axis=0)
    s3=s2
    numpy.random.shuffle(s3)
    
    a=numpy.zeros(s3.flatten().shape)
    plt.plot(s3.flatten(), a,'+')
#    print s3.flatten()
    initPos = numpy.array([[0.0], [1.0]])
    gng = MyGrowingNeuralGasNode.MyGrowingNeuralGasNode(start_poss = initPos, max_nodes=2, eps_n=0.016 )
#    gng._add_node([3.0])
    gng.train(s3)
    
    pos_nodes =  numpy.array([node.data.pos for node in gng.graph.nodes])
    print "distance: ", abs(gng.graph.nodes[0].data.pos - gng.graph.nodes[1].data.pos)
    b=numpy.zeros(pos_nodes.flatten().shape)
    print pos_nodes
    plt.plot(pos_nodes, b, 'or')
    print "connected: ", gng.graph.connected_components()
    
    headTail = [ht.get_ends() for ht in gng.graph.edges]
    for ht in headTail:
        print "ht: ", ht
        #plot line between head and tail
        xHeadTail = [ht[0].data.pos[0], ht[1].data.pos[0]]
        yHeadTail = [0, 0]
        ax.plot(xHeadTail, yHeadTail, color = 'brown', marker = 'o', markersize=3)   
#  
#     ax.scatter([i[0] for i in x],[i[1] for i in x], color='green', s=1 )
    plt.show()
    
    
    