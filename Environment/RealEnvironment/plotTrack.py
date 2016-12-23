import itertools
import numpy
import sys

import SimplePythonClient.CarControl as CarControl
import SimplePythonClient.CarState as CarState
import matplotlib.pyplot as plt


# f = open('StepsVsGoal.txt', 'rb')
# lines = f.readlines()
# splitInto = lines[0].strip().count(";") + 1
# data = [line.strip().split(";",splitInto) for line in lines]
# f.close()
# 
# print data
# #add a plot
# y = [float(y)+10 for y in yLst] 
# plt.scatter(x, y)
filename = 'log_msg_action.txt'
#try:
f = open(filename, 'rb')
speedOld = -1

#lines = f.readlines()

line = f.readline()
while line:
    #msg
    cs = CarState.CarState(line[0:len(line)-1])
    
    #action   
    speed = float(f.readline())
    if speed != speedOld:
        speedOld = speed
        print "---------------"
        print "Speed: ", speed
        print "Time: ", f.readline().strip()
        print "Active Task: ", f.readline().strip() 
        line = f.readline() 
        cc = CarControl.CarControl(0,0,0,0,0,0,0)
        cc.parse(line[0:len(line)-1])
        print "Dist from Start:", cs.getDistFromStart(),"  Speed:",cs.getSpeedX() ,"   damage: ", cs.getDamage(),  " Accel: ", cc.accel
    else:
        f.readline()
        f.readline()
        f.readline()    
    
    line = f.readline()   
        
        
    
    

    
#print f.next()


#  what do the * mean in the original line?:  for line1,line2 in itertools.izip_longest(f,f):    
# for line1,line2 in itertools.izip_longest(f,f):
# #    print line1
#     cs = CarState.CarState(line1[0:len(line1)-1])
#     cc = CarControl.CarControl(0,0,0,0,0,0,0)
#     cc.parse(line2[0:len(line2)-1])
#     if cc.accel != accelOld:
#         accelOld = cc.accel
#         print "Dist from Start:", cs.getDistFromStart(), "   damage: ", cs.getDamage(),  " Accel: ", cc.accel
    
    #print line3
        
f.close()
#except:
#    print "Could not open file: ", filename
#    sys.exit()

# # xLst, yLst = zip(*data)
# x = [float(d[0]) for d in data]
# y1 = [float(d[1]) for d in data]
# fig, ax1 = plt.subplots()
# ax1.plot(x, y1, 'b-')
# 
# if splitInto > 2:
#     y2 = [float(d[2]) for d in data]
#     ax2 = ax1.twinx()
#     ax2.plot(x, y2, 'r-')
#  
# #plt.scatter(x, y)
# plt.show()