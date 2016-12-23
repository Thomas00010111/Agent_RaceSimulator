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
import matplotlib.pyplot as plt

import Environment.RepresentationEnvironment.KdTree.StateSpaceDiscretization as StateSpaceDiscretization
import Misc.MessageParserJavaEnvLaser2D as MsgParser

init = True
prevState = None

plt.ion()

DIMENSION = MsgParser.Dimension
levels = 6

#Actually the number of states in the kd-tree is  2**(levels+1)-1
# but we want an extra state
NUMBER_OF_STATES = 2**(levels+1)    # actually -1, removed for extra state i.e. terminal state

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
 
stateRepresentation= StateSpaceDiscretization.StateSpaceDiscetization()
stateRepresentation.createRepresentation(DIMENSION, levels, )
goalStates = set()  #create a set to save goal states
 
for pos in positions:
    x_env = pos[0]
    y_env = pos[1]
    anglexy = AngleXYCoordinate(x_env, y_env, 0)
    env.setEnvironment(anglexy)
    #laserDistances = env.triggerLaserOpponents()
    laserDistances = env.triggerLaserObstacles()
    print "laserDistances: ", laserDistances
    env.paintComponent()
    
    msg = [x_env, y_env, 0, 0, 0, 0, 0, 0, 0, laserDistances[0], laserDistances[1], 0]
#  
    carState = MsgParser.MessageParserJavaEnv()
    carState.update(msg)
    
    print "carState.getSensorData(): ", carState.getSensorData()
    currentState = stateRepresentation.getState(carState.getSensorData())
    
    if init:
        prevState = currentState
        init = False
    
    if int(currentState) != int(prevState):
        prevState = currentState
        plt.plot(pos[0],pos[1], "bo", markersize=2)
        plt.draw()
#      
    print "currentState: ", currentState
    
    goalStates.add(currentState[0])
 
print "goalStates: ", goalStates
while True:
    time.sleep(5)
        


    