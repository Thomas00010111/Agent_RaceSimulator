# #BEFORE Jnius is loaded !!!
# #javapath = ".:/path/to/jar_files/*"
# export JAVAPATH='~/Dropbox/Workspace/EnvironmentServer/branches/bin'
# os.environ['CLASSPATH'] = javapath
# print 'CLASSPATH: ', os.environ['CLASSPATH']

#To find the class Environment, before starting Eclipse 
#Type in the bash
#export CLASSPATH=~/Dropbox/Workspace/EnvironmentServer/branches/bin
#export CLASSPATH=~/MrFish/RoboticsLab/Link_Dropbox_Workspace_UW/Workspace/EnvironmentServer/branches/bin
#/opt/eclipse/eclipse &

import itertools
from jnius import autoclass
import numpy
import time
#import kdtree


#import Environment.RepresentationEnvironment.SOM.StateSpaceDiscretization as StateSpaceDiscretization
import Environment.RepresentationEnvironment.KdTree.StateSpaceDiscretization as StateSpaceDiscretization

import Misc.MessageParserJavaEnv as MessageParserJavaEnv
import Misc.MessageParserJavaEnv3D as MessageParserJavaEnv3D
import Misc.MessageParserJavaEnv4D as MessageParserJavaEnv4D


#import Environment.RepresentationEnvironment.SOM.DisplayNodePositionsAndV_3D as DisplayNodePositionsAndV_3D
showHistogram = False
loadExtendedMatrices = False

DIMENSION_HIGHER = (3,2,1)
#applies a function to two adjacent elements in an iterable
NUMBER_OF_STATES_HIGHER = reduce(lambda x,y: x*y, DIMENSION_HIGHER)

DIMENSION = (10,10)
#DIMENSION = ( 8, 8, 8, 8)

#applies a function to two adjacent elements in an iterable
NUMBER_OF_STATES = reduce(lambda x,y: x*y, DIMENSION)
#NUMBER_OF_STATES = 2**(DIMENSION[0]+1)-1


levels = 12
NUMBER_OF_STATES = 2**(levels+1)-1

# ------------------------ y const -----------------------
CarPosX = 150
CarPosY = 120
CarAngle = numpy.pi*1.5
CarSpeed = 2
    
rangeCarAngle = numpy.linspace( numpy.pi, 2*numpy.pi,6)
print "rangeCarAngle: ", rangeCarAngle
    
rangeCarPosX = numpy.linspace( 140, 190,9)
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


rangeSpeed = numpy.linspace( 1, 4,4)
print "rangeSpeed: ", rangeSpeed

positions = numpy.array([x for x in itertools.product(rangeCarPosX, rangeCarPosY, rangeCarAngle, rangeSpeed, repeat=1)])
print positions

Environment = autoclass('Environment')
env = Environment(True)
 
AngleXYCoordinate= autoclass('AngleXYCoordinate')
anglexy = AngleXYCoordinate(CarPosX, CarPosY, CarAngle)
env.setEnvironment(anglexy)
 
#stateRepresentation_higher = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION_HIGHER)
stateRepresentation = StateSpaceDiscretization.StateSpaceDiscetization()
stateRepresentation.createRepresentation(DIMENSION, levels)
goalStates = set()
 
for pos in positions:
    msg_higher = [pos[0], pos[1], pos[2], 0, 0, 0, 0]
    msg = [pos[0], pos[1], pos[2], 0, 0, 0, 0, pos[3]]
 
 #   carState_higher = MessageParserJavaEnv3D.MessageParserJavaEnv()
 #   carState_higher.update(msg)
 #   print "carState_higher.getSensorData(): ", carState_higher.getSensorData()
     
    carState = MessageParserJavaEnv.MessageParserJavaEnv()
    carState.update(msg)
    print "carState.getSensorData(): ", carState.getSensorData()
     
    currentState = stateRepresentation.getState(carState.getSensorData())[-1]
#    currentState_higher = stateRepresentation_higher.getState(carState_higher.getSensorData())
     
#    print "currentState_higher: ", currentState_higher
    print "currentState: ", currentState
    
    anglexy = AngleXYCoordinate(pos[0], pos[1], pos[2])
    env.setEnvironment(anglexy)
    env.paintComponent()
    time.sleep(0.1)
    
    goalStates.add(currentState)
 
print "goalStates: ", goalStates
while True:
    time.sleep(5)
        


    