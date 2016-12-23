
import matplotlib.pyplot as plt
import time
import kdtree
import numpy
import util
import itertools
from jnius import autoclass
import Environment.RepresentationEnvironment.KdTree.StateSpaceDiscretization as StateSpaceDiscretization








DIMENSION = 2
levels = 6
#NUMBER_OF_STATES_HL = 2**(levels_HL+1)    # actually -1, removed for extra state i.e. terminal state


#Actually the number of states in the kd-tree is  2**(levels+1)-1
# but we want an extra state
numberOfStates = 2**(levels+1)    # actually -1, removed for extra state i.e. terminal state

# ------------------------ y const -----------------------
CarPosX = 150
CarPosY = 150
CarAngle = numpy.pi*1.5
CarSpeed = 2
    
    
#rangeCarPosX = numpy.linspace( 20, 190,60)
rangeCarPosX = [170]
print "rangeCarPosX: ", rangeCarPosX
    
#rangeCarPosY = [CarPosY]
rangeCarPosY = numpy.linspace( 20, 190,60)
print "rangeCarPosY: ", rangeCarPosY
# ------------------------------------------------------------


positions = numpy.array([x for x in itertools.product(rangeCarPosX, rangeCarPosY, repeat=1)])
#temp = numpy.array([[x[1],x[0]] for x in positions])
#positions = numpy.append(positions, temp, axis = 0)
print positions

Environment = autoclass('Environment')
env = Environment(True)
 
AngleXYCoordinate= autoclass('AngleXYCoordinate')
anglexy = AngleXYCoordinate(CarPosX, CarPosY, CarAngle)
env.setEnvironment(anglexy)
 
stateRepresentation_higher = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION, levels, )




print "---------- DisplayTreeTest ----------"
#plt.figure(self.fig_values.number)
plt.title("Values")

numberOfActions = 4
no1dN = []
points = numpy.array([[0.0, 0.0], [0.0, 1.0], [ 1.0, 0.0], [1.0, 1.0]])
util.splitN(points, 0, 0, levels, no1dN)
tree = kdtree.createNewTree(no1dN)
kdtree.visualize(tree)
util.activate(tree, levels)
Q = numpy.ones((numberOfStates,numberOfActions))


msg2D = [pos[0], pos[1], 0, 0, 0, 0, 0, 0, 0, laserDistances[0], laserDistances[1], 0]
msg = msg2D
#  
carState_higher = MsgParser.MessageParserJavaEnv()
carState_higher.update(msg)
print "carState_higher.getSensorData(): ", carState_higher.getSensorData()
#      
#     carState = MsgParserLaser2D.MessageParserJavaEnv()
#     carState.update(msg)
#     print "carState.getSensorData(): ", carState.getSensorData()
#      
#     currentState = stateRepresentation.getState(carState.getSensorData())[-1]
currentState = stateRepresentation_higher.getState(carState_higher.getSensorData())



#         Q[3][0] = 0.3
#         Q[4][0] = 0.5
kdtree.plotQ2D(tree, min_coord=[0, 0], max_coord=[1, 1],Values = Q, plt=plt, plot="Q")
time.sleep(20)      