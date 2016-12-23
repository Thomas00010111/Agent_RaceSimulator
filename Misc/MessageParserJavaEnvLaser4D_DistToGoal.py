
import math   
import numpy

import Misc.IMessageParser as IMessageParser 


class MessageParserJavaEnv(IMessageParser.IMessageParser):        
    @property
    def carState(self):
        return self.cs
    
           
    def getSensorData(self):
        sensorData = numpy.empty(5)
        
        if self.currentGoal == None:
            # x, y
            sensorData[0]=float(self.msg[0])/200.0
            sensorData[1]=float(self.msg[1])/200.0
        else:
            # dx, dy
            sensorData[0]=((self.currentGoal[0] - float(self.msg[0]))+200)/400.0
            sensorData[1]=((self.currentGoal[1] - float(self.msg[1]))+200)/400.0
        
        #laser starting from [9]
        sensorData[2]=float(self.msg[9])/200.0
        sensorData[3]=float(self.msg[10])/200.0
        circle_rad = math.pi * 2.0
        sensorData[4] = float(self.msg[2])/circle_rad
        return sensorData
    
    def getTrackState(self):
        return str(self.msg[6])
    
    def getReward(self):
        return float(self.msg[3])

        
    

        
    