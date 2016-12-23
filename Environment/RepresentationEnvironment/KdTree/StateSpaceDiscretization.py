'''
Created on Jun 23, 2013

@author: mrfish
'''
import itertools
import numpy
import math

#import Environment.RepresentationEnvironment.SOM.MyGrowingNeuralGasNode as MyGrowingNeuralGasNode 
import kdtree.kdtree as kdtree
import kdtree.util as util
import matplotlib.pyplot as plt


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
    Uses a kd-tree to discretize to stateRepresentation space
    '''
    def __init__(self, minX=0.0, maxX=1.0, minY=0.0, maxY=1.0):
        #self.numberOfStates = reduce(lambda x,y: x*y, netDimension)
        #self.numberOfActions = numberOfActions
        #assert netDimension[0]==netDimension[1], "Dimension[0]*Dimension[1] is number of nodes on the lowest level, dimensions have to be equal"
        #assert math.log(netDimension[0],2).is_integer, "each dimension of lowest level has to be multiple of 2 "
        #self.numberOfStates=8192
        
        self.fig_discretization, self.ax_discretization = plt.subplots()
        self.fig_values, self.ax_values = plt.subplots()
        self.tree = None
        
    def createRepresentation(self, netDimension, levels=None):
#         if levels is None:
#             self.numberOfStates = reduce(lambda x,y: x*y, dimension)
#         else:
#             self.numberOfStates= 2**(levels+1+1)
        nodes = []
    #         if netDimension==2:
    #             points = numpy.array([[0.0, 0.0], [0.0, 1.0], [ 1.0, 0.0], [1.0, 1.0]])
    #         elif netDimension==3:
    #             points = numpy.array([[0.0, 0.0,  0.0],[0.0 ,  0.0, 1.0], [ 0.0, 1.0, 0.0], [ 0.0, 1.0, 1.0], [1.0, 0.0,  0.0], [1.0, 0.0,  1.0], [1.0, 1.0,  0.0], [1.0, 1.0,  1.0]])
    #         elif netDimension==4:
    #             points = numpy.array([[0.0, 0.0, 0.0, 0.0],[0.0, 0.0, 0.0, 1.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 1.0, 1.0], [0.0, 1.0, 0.0, 0.0], [0.0, 1.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0], [0.0, 1.0, 1.0, 1.0], [1.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 1.0], [1.0, 0.0, 1.0, 0.0], [1.0, 0.0, 1.0, 1.0], [1.0, 1.0, 0.0, 0.0], [1.0, 1.0, 0.0, 1.0], [1.0, 1.0, 1.0, 0.0], [1.0, 1.0, 1.0, 1.0]])
    #         elif netDimension==5:
    #             points = numpy.array([[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0, 1.0], [0.0, 0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 1.0, 0.0], [0.0, 0.0, 1.0, 1.0, 1.0],
    #                                   [0.0, 1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0, 1.0], [0.0, 1.0, 1.0, 0.0, 0.0], [0.0, 1.0, 1.0, 0.0, 1.0], [0.0, 1.0, 1.0, 1.0, 0.0], [0.0, 1.0, 1.0, 1.0, 1.0],
    #                                   [1.0, 0.0, 0.0, 0.0, 0.0], [1.0, 0.0, 0.0, 0.0, 1.0], [1.0, 0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 1.0, 1.0], [1.0, 0.0, 1.0, 0.0, 0.0], [1.0, 0.0, 1.0, 0.0, 1.0], [1.0, 0.0, 1.0, 1.0, 0.0], [1.0, 0.0, 1.0, 1.0, 1.0],
    #                                   [1.0, 1.0, 0.0, 0.0, 0.0], [1.0, 1.0, 0.0, 0.0, 1.0], [1.0, 1.0, 0.0, 1.0, 0.0], [1.0, 1.0, 0.0, 1.0, 1.0], [1.0, 1.0, 1.0, 0.0, 0.0], [1.0, 1.0, 1.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0, 0.0], [1.0, 1.0, 1.0, 1.0, 1.0]])
    
        # generate all possible combinations of "0"s and "1"s
        sequence = ["".join(seq) for seq in itertools.product("01", repeat=netDimension)]
        points_temp= numpy.array([list(s) for s in sequence])
        points = numpy.array([map(float, f) for f in points_temp])
            
        util.splitN(points, 0, 0, levels, nodes)
        self.tree = kdtree.createNewTree(nodes)
        util.activate(self.tree, levels+1)
            
        print "Number of nodes: ", len(nodes), "     activated levels: ", levels, "       highestStateId: ",self.highestStateId  
            
    def createRepresentationFromFile(self, filename=None):
        print kdtree
        self.tree = kdtree.load(filename)
        print "highestStateId: ",self.highestStateId
        
    def saveRepresentationTofile(self, filename):
        kdtree.save(self.tree, filename)
        
    @property
    def highestStateId(self):
        return self.tree.getHighestNodeId
 
    def getNode(self, state):
        return kdtree.getNode(self.tree, state)      
    
    
    def getNearestNodes(self, sensorData):
        '''returns all states the point could be in i.e. an array of all possible resolutions'''
        states = numpy.array(self.tree.get_path_to_best_matching_node(sensorData))
        return states
    
    def getNearestNodes_notusingactive(self, sensorData):
        '''returns all states the point could be in i.e. an array of all possible resolutions'''
        states = numpy.array(self.tree.get_path_to_leaf(sensorData))
        return states
    
    def split(self, data, axis=None, sel_axis = (lambda axis: axis)):
        return self.tree.split2(data, axis=axis, sel_axis = (lambda axis: axis))
        
     
#     def getPosition(self,node):
#         return node.data.pos
#     
#     def getStateFromNode(self, node):
#         return node.data.label
#       

    def getState_active(self, sensorData, level="lowest_only"):
        if level == "lowest_only":
            # get current stateRepresentation from sensor data7
            print "self.tree.get_path_to_best_matching_node(sensorData): ", self.tree.get_path_to_best_matching_node(sensorData)
            labelIndex = self.tree.get_path_to_best_matching_node(sensorData)[-1].label
            print "labelIndex: ", labelIndex
            label =  numpy.array([labelIndex])
        elif level =="all":
            label = numpy.array([n.label for n in self.tree.get_path_to_best_matching_node(sensorData)])
        else:
            raise Exception("No level chosen! Choose lowest_only or all nodes in the tree")
        #assert label < self.numberOfStates, "label: " + str(label) + "     self.numberOfStates:" + str(self.numberOfStates)
        return label
    
    def getPathToLeaf(self, data):
        return self.tree.get_path_to_leaf(data)

    def getState(self, sensorData, level="lowest_only"):
        assert self.tree is not None, "No tree created, use one of the create methods to create it."
        if level == "lowest_only":
            # get current stateRepresentation from sensor data7
            print "self.tree.get_path_to_leaf(sensorData): ", self.tree.get_path_to_leaf(sensorData)
            labelIndex = self.tree.get_path_to_leaf(sensorData)[-1].label
            print "labelIndex: ", labelIndex
            label =  numpy.array([labelIndex])
        elif level =="all":
            label = numpy.array([n.label for n in self.tree.get_path_to_leaf(sensorData)])
        else:
            raise Exception("No level chosen! Choose lowest_only or all nodes in the tree")
        #assert label < self.numberOfStates, "label: " + str(label) + "     self.numberOfStates:" + str(self.numberOfStates)
        return label
    
    #Plot state space discretization 
    def update2DPlot(self, min_coord=[0, 0], max_coord=[1, 1], mark_labels=[], path_savefig=None):
        plt.figure(self.fig_discretization.number)
        plt.title("Discretization")
        kdtree.update2DPlot(self.tree, min_coord=min_coord, max_coord=max_coord,  mark_labels= mark_labels, plt=plt, path_savefig=path_savefig)
     
    #Plot state space Q or V funktion    
    def plotQ2D(self, min_coord=[0, 0], max_coord=[1, 1], Values=numpy.empty((0,0)), plot="V", path_savefig=None):
        plt.figure(self.fig_values.number)
        plt.title("Values")
        kdtree.plotQ2D(self.tree, min_coord=min_coord, max_coord=max_coord, Values=Values, plt=plt, plot="Q", path_savefig=path_savefig)
    
#     def getStateNodes(self, sensorData, level="lowest_only"):
#         
#         if level == "lowest_only":
#             # get current stateRepresentation from sensor data
#             label =  numpy.array([self.tree.get_path_to_best_matching_node(sensorData)[-1].label])
#         elif level =="all":
#             label = numpy.array([n.label for n in self.tree.get_path_to_best_matching_node(sensorData)])
#         else:
#             raise Exception("No level chosen! Choose lowest_only or all nodes in the tree")
#         #assert label < self.numberOfStates, "label: " + str(label) + "     self.numberOfStates:" + str(self.numberOfStates)
#         return label
    
    
#     def getStates(self, sensorData):
#         # get current stateRepresentation from sensor data
#         label = [n.label for n in self.getNearestNodes(sensorData)]
#         #assert label < self.numberOfStates, "label: " + str(label) + "     self.numberOfStates:" + str(self.numberOfStates)
#         return label
#     
    

if __name__== "__main__":
        dimension = ( 10, 10 )
        s = StateSpaceDiscetization(dimension)
        kdtree.visualize(s.tree)
        sensorData=[0.6, 0.6]
        print [ n.label for n in s.getNearestNodes(sensorData)] 
        kdtree.plot2D(s.tree,[1920, 1830, 1926, 1927, 1831, 1957, 1951, 1950, 1919])
        