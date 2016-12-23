from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np


STATESORIENTATION = 10
NUMBEROFSTATESONEDIRECTION = 10

def update_position(e):
    i = 0
    for ix in range(0,NUMBEROFSTATESONEDIRECTION):
        for iy in range(0,NUMBEROFSTATESONEDIRECTION):
            for iz in range(0, STATESORIENTATION):
                if(V[NUMBEROFSTATESONEDIRECTION*NUMBEROFSTATESONEDIRECTION*ix + NUMBEROFSTATESONEDIRECTION*iy + iz]):
                    ix2, iy2, _ = proj3d.proj_transform(ix,iy,iz, ax.get_proj())     
                    label[i].xy = ix2,iy2
                    label[i].update_positions(fig.canvas.renderer)
                    i+=1
    fig.canvas.draw()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

V = pickle.load(open( "V.txt", 'rb' ))

#state = NUMBEROFSTATESONEDIRECTION*NUMBEROFSTATESONEDIRECTION*ix + NUMBEROFSTATESONEDIRECTION*iy + iz
x,y,z,c,s,label = [],[],[],[],[],[]

for ix in range(0,NUMBEROFSTATESONEDIRECTION):
    for iy in range(0,NUMBEROFSTATESONEDIRECTION):
        for iz in range(0, STATESORIENTATION):
            # comment if statement to see all values
            if(V[NUMBEROFSTATESONEDIRECTION*NUMBEROFSTATESONEDIRECTION*ix + NUMBEROFSTATESONEDIRECTION*iy + iz]):
                x.append(ix)
                y.append(iy)
                z.append(iz)
                size = abs(V[NUMBEROFSTATESONEDIRECTION*NUMBEROFSTATESONEDIRECTION*ix + NUMBEROFSTATESONEDIRECTION*iy + iz] * 160)
                s.append(max(size,1))   #if size is 0 plot a small dot with size 1
                c.append(V[NUMBEROFSTATESONEDIRECTION*NUMBEROFSTATESONEDIRECTION*ix + NUMBEROFSTATESONEDIRECTION*iy + iz])
                                
scatter = ax.scatter(x, y, z,s=s,c=c)

i=0
for ix in range(0,NUMBEROFSTATESONEDIRECTION):
    for iy in range(0,NUMBEROFSTATESONEDIRECTION):
        for iz in range(0, STATESORIENTATION):
            if(V[NUMBEROFSTATESONEDIRECTION*NUMBEROFSTATESONEDIRECTION*ix + NUMBEROFSTATESONEDIRECTION*iy + iz]):
                ix2, iy2, _ = proj3d.proj_transform(ix,iy,iz, ax.get_proj())
                vValueStr="{:1.1f}".format(float(V[NUMBEROFSTATESONEDIRECTION*NUMBEROFSTATESONEDIRECTION*ix + NUMBEROFSTATESONEDIRECTION*iy + iz]))
                label.append(plt.annotate( vValueStr, xy=(ix2,iy2), xytext = (0, 0),  textcoords = 'offset points' ))     
                i+=1

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')


fig.canvas.mpl_connect('motion_notify_event', update_position)
plt.show()