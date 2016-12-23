
# 
# Use Lasers to detect Opponents
#

import math   
import numpy

import Misc.IMessageParser as IMessageParser 

Dimension = 4

class MessageParserJavaEnv(IMessageParser.IMessageParser):        
    @property
    def carState(self):
        return self.cs
           
    def getSensorData(self):
        sensorData = numpy.empty(4)
        
        #laser starting from [9]
        sensorData[0]=float(self.msg[13])/200.0
        sensorData[1]=float(self.msg[14])/200.0
        sensorData[2]=float(self.msg[15])/200.0
        sensorData[3]=float(self.msg[16])/200.0
        #circle_rad = math.pi * 2.0
        #sensorData[3] = float(self.msg[2])/circle_rad
        assert sensorData[0]<= 1.0 and sensorData[1]<= 1.0 and sensorData[2]<= 1.0 and sensorData[3]<= 1.0, "sensor Data > 1.0" 
        return sensorData
    
    def getTrackState(self):
        return str(self.msg[6])
    
    def getReward(self):
        return float(self.msg[3])

        
    

        
    