# #BEFORE Jnius is loaded !!!
# #javapath = ".:/path/to/jar_files/*"
# javapath = '~/Dropbox/Workspace/EnvironmentServer/branches/bin'
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
import sys
import time

import Environment.RepresentationEnvironment.ExtendedDiscreteTransitionMatrix as ExtendedDiscreteTransitionMatrix
#import Environment.RepresentationEnvironment.SOM.StateSpaceDiscretization as StateSpaceDiscretization
import Environment.RepresentationEnvironment.KdTree.StateSpaceDiscretization as StateSpaceDiscretization
import Misc.MessageParserJavaEnv3D as MessageParserJavaEnv3D
import Misc.MessageParserJavaEnvLaser4D as MessageParserJavaEnv



#import Environment.RepresentationEnvironment.SOM.DisplayNodePositionsAndV_3D as DisplayNodePositionsAndV_3D
showHistogram = False
loadExtendedMatrices = False

DIMENSION_HIGHER = (3,2,1)
#applies a function to two adjacent elements in an iterable
NUMBER_OF_STATES_HIGHER = reduce(lambda x,y: x*y, DIMENSION_HIGHER)

#DIMENSION = (12,12,12,2)
DIMENSION = ( 10,10,10,10)

#applies a function to two adjacent elements in an iterable
NUMBER_OF_STATES = reduce(lambda x,y: x*y, DIMENSION)

# ------------------------ y const -----------------------
# CarPosX = 150
# CarPosY = 120
# CarAngle = numpy.pi*1.5
# CarSpeed = 2
#       
# rangeCarAngle = numpy.linspace( numpy.pi, 2*numpy.pi,10)
# #rangeCarAngle = numpy.linspace( 0, 2*numpy.pi,10)
# print "rangeCarAngle: ", rangeCarAngle
#       
# rangeCarPosX = numpy.linspace( 150, 190,9)
# #rangeCarPosX = numpy.linspace( 20, 50,9)
# print "rangeCarPosX: ", rangeCarPosX
#       
# rangeCarPosY = [CarPosY]
# print "rangeCarPosY: ", rangeCarPosY
# ------------------------------------------------------------

# ----------------------- x const ---------------------------
#pi*1.5 to 0.5pi
CarPosX = 100
CarPosY = 160
CarAngle = 0.5
CarSpeed = 2
      
rangeCarAngle = numpy.concatenate((numpy.linspace( 0, numpy.pi/2.0 ,15), numpy.linspace( 3.0*numpy.pi/2.0, 2.0*numpy.pi ,15))) 
print "rangeCarAngle: ", rangeCarAngle
      
rangeCarPosX = [CarPosX]
print "rangeCarPosX: ", rangeCarPosX
      
rangeCarPosY = numpy.linspace( 150, 180,12)
print "rangeCarPosY: ", rangeCarPosY
# # -----------------------------------------------------------------


# rangeSpeed = numpy.linspace( 1, 4,4)
# print "rangeSpeed: ", rangeSpeed
# 
# positions = numpy.array([x for x in itertools.product(rangeCarPosX, rangeCarPosY, rangeCarAngle, rangeSpeed, repeat=1)])
# print positions
# goalLocations = [[100, 170], [150, 110]]
# carXYPosition = [67.1220111523263, 180.41121176135704]
# use GOAL number ...
# GOAL=1
# 
# if GOAL == 0:
#     #rangeCarAngle = numpy.concatenate((numpy.linspace( 0, numpy.pi/2.0 ,3), numpy.linspace( 3.0*numpy.pi/2.0, 2.0*numpy.pi ,3)))
#     rangeCarAngle = numpy.concatenate((numpy.linspace( 0, numpy.pi/2.0 ,6), numpy.linspace( 3.0*numpy.pi/2.0, 2.0*numpy.pi ,6)))
# elif GOAL == 1:
#     rangeCarAngle = numpy.linspace( numpy.pi, 2*numpy.pi,5) 
#  
# print "rangeCarAngle: ", rangeCarAngle
 
rangeSpeed = numpy.linspace( 1, 4,4)
print "rangeSpeed: ", rangeSpeed

positions = numpy.array([x for x in itertools.product(rangeCarPosX, rangeCarPosY, rangeCarAngle, rangeSpeed, repeat=1)])

# Goal, use variable GOAL to find goals for tasksNUMBER_OF_STATES_HIGHER
#positions = numpy.array([x for x in itertools.product([goalLocations[GOAL][0]], [goalLocations[GOAL][1]], rangeCarAngle, rangeSpeed, repeat=1)])

# Set car a certain position
#positions = numpy.array([x for x in itertools.product([carXYPosition[0]], [carXYPosition[1]], rangeCarAngle, rangeSpeed, repeat=1)])

print positions

Environment = autoclass('Environment')
env = Environment(True)
 
AngleXYCoordinate= autoclass('AngleXYCoordinate')
# anglexy = AngleXYCoordinate(CarPosX, CarPosY, CarAngle)
# env.setEnvironment(anglexy)
# env.triggerLaser() 
 


#stateRepresentation_higher = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION_HIGHER)
stateRepresentation = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION)

currentState_higher = None
currentState = None

goalStates = set()
 
for pos in positions:
    anglexy = AngleXYCoordinate(pos[0], pos[1], pos[2])
    env.setEnvironment(anglexy)
    laserDistances = env.triggerLaser()
    print "laserDistances: ", laserDistances
    env.paintComponent()
    
    msg_higher = [pos[0], pos[1], pos[2], 0, 0, 0, 0]
    msg = [pos[0], pos[1], pos[2], 0, 0, 0, 0, pos[3], 0, laserDistances[0], laserDistances[1], laserDistances[2]]
 
    carState_higher = MessageParserJavaEnv3D.MessageParserJavaEnv()
    carState_higher.update(msg)
    print "carState_higher.getSensorData(): ", carState_higher.getSensorData()
     
    carState = MessageParserJavaEnv.MessageParserJavaEnv()
    #carState.update(msg, goalLocations[GOAL])
    carState.update(msg)
    print "carState.getSensorData(): ", carState.getSensorData()
     
    currentState = stateRepresentation.getState(carState.getSensorData())
#    currentState_higher = stateRepresentation_higher.getState(carState_higher.getSensorData())
     
    print "currentState_higher: ", currentState_higher
    print "currentState: ", currentState
    
    
    time.sleep(0.1)
    
    goalStates.add(int(currentState))
 
print "goalStates: ", goalStates
while True:
    time.sleep(5)
        


    