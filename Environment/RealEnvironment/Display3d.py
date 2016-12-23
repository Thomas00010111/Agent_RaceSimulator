from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import Environment.RepresentationEnvironment.SOM.MyGrowingNeuralGasNode as MyGrowingNeuralGasNode 
import matplotlib.pyplot as plt
import numpy as np


#load data
sensorDataFloatTemp = np.load(open("sensors.pkl", 'r'))
#sensorDataFloatCounter = np.load(open("sensorsCounter.pkl", 'r'))
#sensorDataFloat = np.array([sd for sd in sensorDataFloatTemp if not np.array_equal(sd, np.array([0,0,0]))])
sensorDataFloat = sensorDataFloatTemp
print sensorDataFloat   


nodes = np.zeros((5, 3))
gng = MyGrowingNeuralGasNode.MyGrowingNeuralGasNode(start_poss = nodes, max_nodes=10)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#plot nodes before training 
nodePosX = [node.data.pos[0] for node in gng.graph.nodes]
nodePosY = [node.data.pos[1] for node in gng.graph.nodes]
nodePosZ = [node.data.pos[2] for node in gng.graph.nodes]
ax.scatter(nodePosX, nodePosY, nodePosZ, color='green', s=240)

#train
gng.train(sensorDataFloat[:,0:3])
gng.stop_training()

nodePosX = [node.data.pos[0] for node in gng.graph.nodes]
nodePosY = [node.data.pos[1] for node in gng.graph.nodes]
nodePosZ = [node.data.pos[2] for node in gng.graph.nodes]

ax.scatter(nodePosX, nodePosY, nodePosZ, color='red', s=120)                            
ax.scatter(sensorDataFloat[:,0], sensorDataFloat[:,1], sensorDataFloat[:,2])

ax.set_xlabel('left')
ax.set_ylabel('front')
ax.set_zlabel('right')

# plot track and states
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

# replay sensor data
states = np.zeros((np.size(sensorDataFloat,0),1))
for i,sensorData in enumerate(sensorDataFloat):
    (n0, n1), (dist0, dist1) = gng._get_nearest_nodes(sensorData[0:3])
    states[i-1] = n0.data.label

xpos =sensorDataFloat[:,3]
ypos =sensorDataFloat[:,4]

stateOld = None
for i,stateRepresentation in enumerate(states):
    if stateOld != stateRepresentation:
        ax2.text(xpos[i-1], ypos[i-1], str(stateRepresentation))
        stateOld = stateRepresentation
         
ax2.plot(xpos, ypos)

# plot lap times in seconds
laptime = sensorDataFloat[:,6]
damage = sensorDataFloat[:,7]
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.plot(laptime, 'r')
ax3.set_ylabel('laptime', color='r')
ax4 = ax3.twinx() 
ax4.plot(damage, 'b')
ax4.set_ylabel('damage', color='b')
plt.show()