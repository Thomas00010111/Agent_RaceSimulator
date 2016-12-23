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
import math
import time


#import Environment.RepresentationEnvironment.SOM.DisplayNodePositionsAndV_3D as DisplayNodePositionsAndV_3D
DIMENSION_HIGHER = (3,2,1)
#applies a function to two adjacent elements in an iterable
#NUMBER_OF_STATES_HIGHER = reduce(lambda x,y: x*y, DIMENSION_HIGHER)

DIMENSION = (12,12,12,2)
#applies a function to two adjacent elements in an iterable
#NUMBER_OF_STATES = reduce(lambda x,y: x*y, DIMENSION)

CarPosX = 160
CarPosY = 120
#CarAngle = -math.pi/2
CarAngle = 7.0 * math.pi/4.0

Environment = autoclass('Environment')
env = Environment(True)

AngleXYCoordinate= autoclass('AngleXYCoordinate')
myCoordinates = AngleXYCoordinate(CarPosX, CarPosY, CarAngle)
print myCoordinates.toString()
env.setEnvironment(myCoordinates)



carClass = autoclass('Car')
car=carClass(env)

speed = 10.0
action = 2  #forward

myActionStr = "ACTION:" + str(action) + ":" + str(speed)
output = env.processInput(myActionStr)
time.sleep(0.1)
env.paintComponent()

#car driver "up", thus y decreases
print env.myCoordinates.toString()
print output

while True:
    time.sleep(5)



# stateRepresentation_higher = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION_HIGHER)
# stateRepresentation = StateSpaceDiscretization.StateSpaceDiscetization(DIMENSION)
# 
# msg_higher = [CarPosX, CarPosY, CarAngle, 0, 0, 0, 0]
# msg = [CarPosX, CarPosY, CarAngle, 0, 0, 0, 0, CarSpeed]
# 
# carState_higher = MessageParserJavaEnv3D.MessageParserJavaEnv()
# carState_higher.update(msg)
# print "carState_higher.getSensorData(): ", carState_higher.getSensorData()
# 
# carState = MessageParserJavaEnv.MessageParserJavaEnv()
# carState.update(msg)
# print "carState.getSensorData(): ", carState.getSensorData()
# 
# currentState = stateRepresentation.getState(carState.getSensorData())
# currentState_higher = stateRepresentation_higher.getState(carState_higher.getSensorData())
# 
# print "currentState_higher: ", currentState_higher
# print "currentState: ", currentState
# 
# #DisplayNodePositionsAndV_3D.DisplayNodePositionsAndV_3D(stateRepresentation.getNodePositions())
# 
# while True:
#     time.sleep(1)

# for i in range(1,20,2):
#     anglexy1 = AngleXYCoordinate(CarPosX, CarPosY + i, CarAngle)
#     env.setEnvironment(anglexy1)
#     env.paintComponent()
#     time.sleep(0.5)
    