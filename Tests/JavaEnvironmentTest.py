# #BEFORE Jnius is loaded !!!
# #javapath = ".:/path/to/jar_files/*"
# javapath = '~/Dropbox/Workspace/EnvironmentServer/branches/bin'
# os.environ['CLASSPATH'] = javapath
# print 'CLASSPATH: ', os.environ['CLASSPATH']

#To find the class Environment, before starting Eclipse 
#Type in the bash
#export CLASSPATH=~/Dropbox/Workspace/EnvironmentServer/branches/bin
#/opt/eclipse/eclipse &

from jnius import autoclass
import numpy
import sys
import time

import Environment.RepresentationEnvironment.ExtendedDiscreteTransitionMatrix as ExtendedDiscreteTransitionMatrix
import Environment.RepresentationEnvironment.SOM.StateSpaceDiscretization as StateSpaceDiscretization
import Misc.MessageParserJavaEnv3D as MessageParserJavaEnv3D
import Misc.MessageParserJavaEnv4D as MessageParserJavaEnv
import matplotlib.pyplot as plt


#import Environment.RepresentationEnvironment.SOM.DisplayNodePositionsAndV_3D as DisplayNodePositionsAndV_3D
showHistogram = False
loadExtendedMatrices = False

DIMENSION_HIGHER = (3,2,1)
#applies a function to two adjacent elements in an iterable
NUMBER_OF_STATES_HIGHER = reduce(lambda x,y: x*y, DIMENSION_HIGHER)

DIMENSION = (12,12,12,2)
#applies a function to two adjacent elements in an iterable
NUMBER_OF_STATES = reduce(lambda x,y: x*y, DIMENSION)


#driver1.mySimpleAgent.goalState =[1680, 1656, 1632, 1682, 1658, 1704, 1710, 1686, 1662, 1660,1684]
CarPosX = 170
CarPosY = 135
CarAngle = -numpy.pi/2
CarSpeed = 2



Environment = autoclass('Environment')
env = Environment(True)
 
AngleXYCoordinate= autoclass('AngleXYCoordinate')
anglexy = AngleXYCoordinate(CarPosX, CarPosY, CarAngle)
env.setEnvironment(anglexy)
 
stateRepresentation_higher = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION_HIGHER)
stateRepresentation = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION)
 
msg_higher = [CarPosX, CarPosY, CarAngle, 0, 0, 0, 0]
msg = [CarPosX, CarPosY, CarAngle, 0, 0, 0, 0, CarSpeed]
 
carState_higher = MessageParserJavaEnv3D.MessageParserJavaEnv()
carState_higher.update(msg)
print "carState_higher.getSensorData(): ", carState_higher.getSensorData()
 
carState = MessageParserJavaEnv.MessageParserJavaEnv()
carState.update(msg)
print "carState.getSensorData(): ", carState.getSensorData()
 
currentState = stateRepresentation.getState(carState.getSensorData())
currentState_higher = stateRepresentation_higher.getState(carState_higher.getSensorData())
 
print "currentState_higher: ", currentState_higher
print "currentState: ", currentState
 
 
if loadExtendedMatrices:
    # load files and show probability matrix
    print "Loading Matrices"
    currentState = 1678
    extendedMatrix = ExtendedDiscreteTransitionMatrix.ExtendedDiscreteTransitionMatrix(8,12*12*12*2, "matrix", "../Environment/RealEnvironment/ExtendedTransitionMatrices")
    extendedMatrix.displayProbabilityMatrix(currentState)


if not showHistogram:
    while True:
        time.sleep(1)
        
probabilityFlattened= extendedMatrix.getProbabilityMatricesFlattened()
print numpy.histogram(probabilityFlattened, [ 0.,0.000001 ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1. ])
plt.hist(probabilityFlattened, bins=( 0.000001 ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1.))
plt.savefig("histogramProbability")
plt.show()
#DisplayNodePositionsAndV_3D.DisplayNodePositionsAndV_3D(stateRepresentation.getNodePositions())

# while True:
#     time.sleep(1)


    