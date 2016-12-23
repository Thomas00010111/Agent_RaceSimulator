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
import matplotlib.colors as colors
import matplotlib.cm as cm


#import Environment.RepresentationEnvironment.SOM.StateSpaceDiscretization as StateSpaceDiscretization
import Environment.RepresentationEnvironment.KdTree.StateSpaceDiscretization as StateSpaceDiscretization
import Misc.MessageParserJavaEnvLaser5D as MsgParser
#import Misc.MessageParserJavaEnvLaser2D as MsgParser


#import Environment.RepresentationEnvironment.SOM.DisplayNodePositionsAndV_3D as DisplayNodePositionsAndV_3D
init = True
prevState = None


#***************************************************
#ATTENTION: Set the correct Sensor in Parser module
#****************************************************

postfix_added_by_save = "_Q_log"
filename = "../Environment/RealEnvironment/rl" + postfix_added_by_save
filename_tree = "../Environment/RealEnvironment/StateSpaceRep_opponent"

q = numpy.load(open(filename + ".npy", 'rb'))
print "q: ", q
print "q.min(): ", q.min(), "     q.max(): ",  q.max()
q_without_ones = [x for x in q.flatten() if x != 1.0]   #q is initialized with "1"s... why remove those?
plt.hist(q_without_ones, bins=20)
plt.show()
norm = colors.Normalize(q.min(), 11.0)

stateRepresentation_higher = StateSpaceDiscretization.StateSpaceDiscetization()
stateRepresentation_higher.createRepresentationFromFile(filename_tree)


# ------------------------ y const -----------------------
# CarPosX = 150
# CarPosY = 150
# CarAngle = numpy.pi*1.5
# CarSpeed = 2
    
minCoordinate = 10
maxCoordinate = 190    
rangeCarPosX = numpy.linspace( minCoordinate, maxCoordinate,80)
#rangeCarPosX = [170]
print "rangeCarPosX: ", rangeCarPosX
    
#rangeCarPosY = [CarPosY]
rangeCarPosY = numpy.linspace( minCoordinate, maxCoordinate,80)
print "rangeCarPosY: ", rangeCarPosY
# ------------------------------------------------------------
#positions with actions down and right
positions = numpy.array([x for x in itertools.product(rangeCarPosX, rangeCarPosY, [0], repeat=1)])
temp = numpy.array([[x[1],x[0], 1] for x in positions])
positions = numpy.append(positions, temp, axis = 0)
print positions

Environment = autoclass('Environment')
env = Environment(True)
 
AngleXYCoordinate= autoclass('AngleXYCoordinate')

DistBoarder = 2 # for drawing function values next to border between states
occuredStates = set()

fig_v2d = plt.figure(figsize=(16, 8), dpi=150)
ax1_v2d = plt.gcf().gca()


for pos in positions:
    anglexy = AngleXYCoordinate(pos[0], pos[1], 0)
    env.setEnvironment(anglexy)
    laserDistances = env.triggerLaserObstacles() + env.triggerLaserOpponents()
    
    print "laserDistances: ", laserDistances
    
    env.paintComponent()

    carState_higher = MsgParser.MessageParserJavaEnv()
                                                            #***************************************************
    carState_higher.setSensorType(MsgParser.OpponentSensor) #ATTENTION: Set the correct Sensor in Parser module
                                                            #****************************************************
    msg= [pos[0], pos[1], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
   
    for i in range(0, MsgParser.Dimension_OpponentSensor + MsgParser.Dimension_DistanceSensor):
            msg[MsgParser.SensorDataStart + i]=laserDistances[i]

    carState_higher.update(msg)
    print "carState_higher.getSensorData(): ", carState_higher.getSensorData()

    currentState = int(stateRepresentation_higher.getState(carState_higher.getSensorData()))
    print "currentState: ", currentState
    occuredStates.add(currentState)
    
    if init or pos[0] == minCoordinate  or pos[1] == minCoordinate:
        prevState = currentState
        init = False
    
    #draw state borders
    if int(currentState) != int(prevState):
        
        #check moving direction
        if pos[2] == 0: #down
            q_up = q[currentState][2]    #-y
            q_down = q[prevState][3]     #+y
            plt.plot(pos[0],pos[1]+DistBoarder, "bo",color=cm.jet(norm( float(q_up) )), markersize=4)
            plt.plot(pos[0],pos[1]-DistBoarder, "bo", color=cm.jet(norm( float(q_down) )), markersize=4)
            plt.plot(pos[0],pos[1], "_k", markersize=10)
            
        if pos[2] == 1:#right
            q_left = q[currentState][0]  # -x
            q_right = q[prevState][1]    #+x
            plt.plot(pos[0]+DistBoarder,pos[1], "bo",color=cm.jet(norm( float(q_left) )), markersize=4)
            plt.plot(pos[0]-DistBoarder,pos[1], "bo", color=cm.jet(norm( float(q_right) )), markersize=4)
            plt.plot(pos[0],pos[1], "|k", markersize=10)              
        #plt.draw()
        prevState = currentState
    print "currentState: ", currentState
    
# When added the rest disappears    
# cax = ax1_v2d.imshow(q, interpolation='nearest', cmap=cm.jet)
# number_bins_colorbar = 20
# ticks = numpy.linspace(q.min(), q.max(), number_bins_colorbar)
# cbar = fig_v2d.colorbar(cax, ticks=[ticks], orientation='vertical')
print "occuredStates: ", occuredStates
plt.xlim([0,200])
plt.ylim([0,200])
plt.show() 

while True:
    time.sleep(5)
        


    