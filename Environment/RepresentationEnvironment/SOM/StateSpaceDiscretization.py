'''
Created on Jun 23, 2013

@author: mrfish
'''
import itertools
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
        



class StateSpaceDiscetization:
    '''
    Uses a growing neural network to discretize to stateRepresentation space
    If grow is set to True, the gng will start at the minimum number of nodes and grow to the maximal number
    of numberOfStates states. 
    '''
    def __init__(self, netDimension, grow=False, minX=0.0, maxX=1.0, minY=0.0, maxY=1.0):
        self.numberOfStates = reduce(lambda x,y: x*y, netDimension)
        #self.numberOfActions = numberOfActions
        self.nodeIndex = 0
        dimension = netDimension
                
        # init gng
        if not grow:
#             print "Init GNG with 2D sensor input"
#             upperFloat = math.sqrt(self.numberOfStates)
#             upper = int(math.sqrt(self.numberOfStates))
#             if(upperFloat-upper):
#                 print "ERROR: At the moment nodes can only be arranged as nxn"
#                 sys.exit()  # At the moment nodes can only be arranged as nxn, otherwise number of nodes > then indexed nodes
            
            range0=numpy.linspace( 1.0/(dimension[0]*2), 1.0-(1.0/(dimension[0]*2)),dimension[0] )
            range1=numpy.linspace( 1.0/(dimension[1]*2), 1.0-(1.0/(dimension[1]*2)),dimension[1] )
            if len(dimension)==2:
                nodes = numpy.array([x for x in itertools.product(range0, range1, repeat=1)])
            if len(dimension)==3:
                range2 = numpy.linspace( 1.0/(dimension[2]*2), 1.0-(1.0/(dimension[2]*2)),dimension[2] )
                nodes = numpy.array([x for x in itertools.product(range0, range1, range2, repeat=1)])
            if len(dimension)==4:
                range2 = numpy.linspace( 1.0/(dimension[2]*2), 1.0-(1.0/(dimension[2]*2)),dimension[2] )
                range3 = numpy.linspace( 1.0/(dimension[3]*2), 1.0-(1.0/(dimension[3]*2)),dimension[3] )
                nodes = numpy.array([x for x in itertools.product(range0, range1, range2,range3, repeat=1)])
            if len(dimension)==5:
                range2 = numpy.linspace( 1.0/(dimension[2]*2), 1.0-(1.0/(dimension[2]*2)),dimension[2] )
                range3 = numpy.linspace( 1.0/(dimension[3]*2), 1.0-(1.0/(dimension[3]*2)),dimension[3] )
                range4 = numpy.linspace( 1.0/(dimension[4]*2), 1.0-(1.0/(dimension[4]*2)),dimension[4] )
                nodes = numpy.array([x for x in itertools.product(range0, range1, range2,range3, range4, repeat=1)])
            
            
#             range0=[i/float(dimension[0]) for i in range(1, dimension[0]+1)]
#             range1=[i/float(dimension[1]) for i in range(1,dimension[1]+1)]
#             if len(dimension)==2:
#                 nodes = numpy.array([x for x in itertools.product(range0, range1, repeat=1)])
#             if len(dimension)==3:
#                 range2=[i/float(dimension[2]) for i in range(1,dimension[2]+1)] 
#                 nodes = numpy.array([x for x in itertools.product(range0, range1, range2, repeat=1)])
#             if len(dimension)==4:
#                 range2=[i/float(dimension[2]) for i in range(1,dimension[2]+1)] 
#                 range3=[i/float(dimension[3]) for i in range(1,dimension[3]+1)]
#                 nodes = numpy.array([x for x in itertools.product(range0, range1, range2,range3, repeat=1)])
            #nodes = nodes/float(max(dimension)-1)
            print "nodes: ", nodes
    
            initPos = numpy.array(nodes[0:2])
            #initPos = numpy.array([MyGrowingNeuralGasNode._NGNodeData(nodes[0], 0)])       
            #self.gng = mdp.nodes.GrowingNeuralGasNode(start_poss = initPos, max_nodes=numberOfStates, eps_b=0.0, eps_n=0.0, max_age = 1000, lambda_ = sys.maxint)
            self.gng = MyGrowingNeuralGasNode.MyGrowingNeuralGasNode(start_poss = initPos, max_nodes=self.numberOfStates, eps_b=0.2, eps_n=0.006, max_age = 1000, lambda_ = 100)
            #[self.gng._add_node(node, label="test") for node in nodes[2:]]
            #abc = self.gng.graph.add_node(data)
            #[self.gng.addNode(MyGrowingNeuralGasNode._NGNodeData(node, self.nodeIndex)) for self.nodeIndex,node in enumerate(nodes[2:])]
            [self.gng.addNode(node) for node in nodes[2:]]
        else:
            print "Init GNG with 3D sensor input"
            initPos = numpy.random.rand(2,3)
            self.gng = MyGrowingNeuralGasNode.MyGrowingNeuralGasNode(start_poss = initPos, max_nodes=self.numberOfStates )
        
    
    def addNode(self, nodePosition):
        self.gng.addNode(nodePosition)
    
    
    def generateLabels(self):
        """During training, nodes are added and removed, thus a unique matching from label to
        node is not possible. When training is finished labels can be added to the nodes."""
        for labelIdx, node in enumerate(self.gng.graph.nodes):
            node.data.label = labelIdx
            print "generateLabels node.label: ", node.data.label
        
        assert self.gng.graph.nodes[-1].data.label == len(self.gng.graph.nodes)-1, "Last node label must be equal to number_of_nodes 1"
        
        
    def getNearestNode(self, sensorData):
        (n0, n1), (dist0, dist1) = self.gng._get_nearest_nodes(sensorData)
        assert dist0 <= dist1, "Assumption was wrong!! dist0 > dist1"
        return n0
    
    def getPosition(self,node):
        return node.data.pos
    
    def getStateFromNode(self, node):
        return node.data.label
      
#     def getState(self, sensorData):
#         # get current stateRepresentation from sensor data
#         n0 = self.getNearestNode(sensorData)
#         assert n0.data.label < self.numberOfStates, "n0.data.label: " + str(n0.data.label) + "     self.numberOfStates:" + str(self.numberOfStates)
#         return n0.data.label
    
    def getState(self, sensorData):
        # get current stateRepresentation from sensor data
        n0 = self.getNearestNode(sensorData)
        assert n0.data.label < self.numberOfStates, "n0.data.label: " + str(n0.data.label) + "     self.numberOfStates:" + str(self.numberOfStates)
        return numpy.array([n0.data.label])
        
    def getPositionsBelongingToNodes(self): 
        positions, states = [], []
        xCoord = numpy.linspace(0.0, 1.0, 20)
        yCoord = numpy.linspace(0.0, 1.0, 20)
        for x in xCoord:
            for y in yCoord:
                positon = numpy.array([x,y])
                stateRepresentation = self.getState(positon)
                positions.append(positon)
                states.append(stateRepresentation)
        print "getPositionsBelongingToNodes(): \n states:\n", states
        return positions, states
    
    def train(self, sensorData):
        print "State Space Discretization: training gng"
        self.gng.train(sensorData)
        print "State Space Discretization: number of nodes: ", len(self.gng.graph.nodes)
#        self.gng.stop_training() 
    
    
    def saveNodes(self, filename):
        #nodePos = [node.data.pos for node in self.gng.graph.nodes]
        nodePos = self.getNodePositions()
        numpy.save(open("gng_nodePos_" + filename + ".pkl", "wb"), nodePos)
    
    def getNodePositions(self):
        return numpy.array([node.data.pos for node in self.gng.graph.nodes]) 
        
    def getClassName(self):
        return self.__class__.__name__