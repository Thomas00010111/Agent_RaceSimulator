import math
import numpy

import matplotlib.pyplot as plt


#plt.ion()
theta = -numpy.pi/4
step = 1

dx = math.cos(theta)
dy = math.sin(theta) 

startPointX = 10
startPointY = 10

newPosX = startPointX
newPosY = startPointY

for i in range(0,10):
    newPosX=newPosX+dx*step
    newPosY=newPosY+dy*step
    plt.plot(newPosX, newPosY, "o")
    
plt.show()

