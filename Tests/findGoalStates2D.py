# #BEFORE Jnius is loaded !!!
# #javapath = ".:/path/to/jar_files/*"
# javapath = '~/Dropbox/Workspace/EnvironmentServer/branches/bin'
# os.environ['CLASSPATH'] = javapath
# print 'CLASSPATH: ', os.environ['CLASSPATH']

#To find the class Environment, before starting Eclipse 
#Type in the bash
#export CLASSPATH=~/Dropbox/Workspace/EnvironmentServer/branches/bin
#/opt/eclipse/eclipse &

import itertools
from jnius import autoclass
import numpy
import time
import kdtree


#import Environment.RepresentationEnvironment.SOM.StateSpaceDiscretization as StateSpaceDiscretization
import Environment.RepresentationEnvironment.KdTree.StateSpaceDiscretization as StateSpaceDiscretization
import Misc.MessageParserJavaEnv as MsgParser2D
import Misc.MessageParserJavaEnvLaser2D as MsgParserLaser2D


#import Environment.RepresentationEnvironment.SOM.DisplayNodePositionsAndV_3D as DisplayNodePositionsAndV_3D
showHistogram = False
loadExtendedMatrices = False


DIMENSION = MsgParserLaser2D.Dimension

#ACTION_TIME_COUNTER = 1000
ACTION_TIMEOUT_COUNTER = 5000

NUMBER_OF_ACTIONS_HL = 4    #left, right, up, down
DIMENSION_HL = MsgParser2D.Dimension
GOAL_STATE_HL = 3
levels_HL = 4
#NUMBER_OF_STATES_HL = 2**(levels_HL+1)    # actually -1, removed for extra state i.e. terminal state


#Actually the number of states in the kd-tree is  2**(levels+1)-1
# but we want an extra state
levels = 7
NUMBER_OF_STATES = 2**(levels+1)    # actually -1, removed for extra state i.e. terminal state

# ------------------------ y const -----------------------
CarPosX = 150
CarPosY = 150
CarAngle = numpy.pi*1.5
CarSpeed = 2
    
    
rangeCarPosX = numpy.linspace( 20, 190,9)
print "rangeCarPosX: ", rangeCarPosX
    
rangeCarPosY = [CarPosY]
print "rangeCarPosY: ", rangeCarPosY
# ------------------------------------------------------------

# ----------------------- x const ---------------------------
# pi*1.5 to 0.5pi
# CarPosX = 100
# CarPosY = 160
# CarAngle = 0.5
# CarSpeed = 2
#    
# rangeCarAngle = numpy.concatenate((numpy.linspace( 0, numpy.pi/2.0 ,3), numpy.linspace( 3.0*numpy.pi/2.0, 2.0*numpy.pi ,3))) 
# print "rangeCarAngle: ", rangeCarAngle
#    
# rangeCarPosX = [CarPosX]
# print "rangeCarPosX: ", rangeCarPosX
#    
# rangeCarPosY = numpy.linspace( 140, 190,9)
# print "rangeCarPosY: ", rangeCarPosY
# # -----------------------------------------------------------------


positions = numpy.array([x for x in itertools.product(rangeCarPosX, rangeCarPosY, repeat=1)])
print positions

Environment = autoclass('Environment')
env = Environment(True)
 
AngleXYCoordinate= autoclass('AngleXYCoordinate')
anglexy = AngleXYCoordinate(CarPosX, CarPosY, CarAngle)
env.setEnvironment(anglexy)
 
stateRepresentation_higher = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION_HL, levels_HL)
stateRepresentation = StateSpaceDiscretization.StateSpaceDiscetization()
stateRepresentation.createRepresentation(DIMENSION, levels, )

while(stateRepresentation.tree is None):
    pass

goalStates = set()  #create a set to save goal states
 
for pos in positions:
    anglexy = AngleXYCoordinate(pos[0], pos[1], 0)
    env.setEnvironment(anglexy)
    laserDistances = env.triggerLaserObstacles()
    print "laserDistances: ", laserDistances
    env.paintComponent()
    
    msg_higher = [pos[0], pos[1], 0, 0, 0, 0, 0]
    msg = [pos[0], pos[1], 0, 0, 0, 0, 0, 0, 0, laserDistances[0], laserDistances[1], 0]
 
    carState_higher = MsgParser2D.MessageParserJavaEnv()
    carState_higher.update(msg)
    print "carState_higher.getSensorData(): ", carState_higher.getSensorData()
     
    carState = MsgParserLaser2D.MessageParserJavaEnv()
    carState.update(msg)
    print "carState.getSensorData(): ", carState.getSensorData()
     
    currentState = stateRepresentation.getState(carState.getSensorData())[-1]
    currentState_higher = stateRepresentation_higher.getState(carState_higher.getSensorData())
     
    print "currentState_higher: ", currentState_higher
    print "currentState: ", currentState
    
    anglexy = AngleXYCoordinate(pos[0], pos[1], 0)
    env.setEnvironment(anglexy)
    env.paintComponent()
    time.sleep(0.1)
    
    goalStates.add(currentState)
 
print "goalStates: ", goalStates
while True:
    time.sleep(5)
        


    