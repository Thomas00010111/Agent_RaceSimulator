'''
Created on Jun 23, 2013

@author: mrfish
'''
import matplotlib.pyplot as plt
import numpy

import Environment.RepresentationEnvironment.SOM.MyGrowingNeuralGasNode as MyGrowingNeuralGasNode 
        
if __name__=="__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    s1=numpy.random.normal(1.0, 0.05, [1,1])
    s2=numpy.random.normal(4.4, 0.01, [100,1])

#    s3 = numpy.append(s1,s2, axis=0)
    s3=s2
    numpy.random.shuffle(s3)
    
    a=numpy.zeros(s3.flatten().shape)
    plt.plot(s3.flatten(), a,'+')
#    print s3.flatten()
    initPos = numpy.array([[0.0], [1.0]])
    
    gng = []
    for i in range(3):
        gng.append(MyGrowingNeuralGasNode.MyGrowingNeuralGasNode(start_poss = numpy.array([[0.0], [1.0]]), max_nodes=2, eps_n=0.03 ))
#    gng._add_node([3.0])
    
    gng[1].train(s3)
    
    for i,g in enumerate(gng):
        print "i: ", i, "   ", [node.data.pos for node in g.graph.nodes]

    s4 = numpy.random.normal(5.9, 0.01, [10, 1])
    gng[1].train(s4)

    for i, g in enumerate(gng):
        print "i: ", i, "   ", [node.data.pos for node in g.graph.nodes]
#     print "distance: ", abs(gng.graph.nodes[0].data.pos - gng.graph.nodes[1].data.pos)
#     b=numpy.zeros(pos_nodes.flatten().shape)
#     print pos_nodes
#     plt.plot(pos_nodes, b, 'or')
#     print "connected: ", gng.graph.connected_components()
#     
#     headTail = [ht.get_ends() for ht in gng.graph.edges]
#     for ht in headTail:
#         print "ht: ", ht
#         #plot line between head and tail
#         xHeadTail = [ht[0].data.pos[0], ht[1].data.pos[0]]
#         yHeadTail = [0, 0]
#         ax.plot(xHeadTail, yHeadTail, color = 'brown', marker = 'o', markersize=3)   
# #  
# #     ax.scatter([i[0] for i in x],[i[1] for i in x], color='green', s=1 )
#     plt.show()
    
    
    