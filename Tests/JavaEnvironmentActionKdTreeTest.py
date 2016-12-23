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
import Environment.RepresentationEnvironment.KdTree.StateSpaceDiscretization as StateSpaceDiscretization
import Misc.MessageParserJavaEnv3D as MessageParserJavaEnv3D
import Misc.MessageParserJavaEnv4D as MessageParserJavaEnv
import kdtree
import matplotlib.pyplot as plt


#import Environment.RepresentationEnvironment.SOM.DisplayNodePositionsAndV_3D as DisplayNodePositionsAndV_3D
showHistogram = False
loadExtendedMatrices = False

DIMENSION = (12,12,12,2)
#DIMENSION = (2,2,2,2)
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
 
stateRepresentation = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION)

msg = [CarPosX, CarPosY, CarAngle, 0, 0, 0, 0, CarSpeed]
 
carState = MessageParserJavaEnv.MessageParserJavaEnv()
carState.update(msg)
print "carState.getSensorData(): ", carState.getSensorData()
currentStates = stateRepresentation.getStates(carState.getSensorData())
print "currentState: ", currentStates
 
kdtree.visualize(stateRepresentation.tree)
 
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


    