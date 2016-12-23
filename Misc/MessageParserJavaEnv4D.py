
import math
import numpy

import Misc.IMessageParser as IMessageParser 


class MessageParserJavaEnv(IMessageParser.IMessageParser):
        
    @property
    def carState(self):
        return self.cs
           
    def getSensorData(self):
        sensorData = numpy.array(self.msg[0:4]).astype(numpy.float)
        sensorData[0] = sensorData[0]/200.0
        sensorData[1] = sensorData[1]/200.0
        
        circle_rad = math.pi * 2.0
        sensorData[2] = sensorData[2]/circle_rad
        sensorData[3] = self.cs.getSpeed()/4.0
        assert sensorData[0]<= 1.0 and sensorData[1]<= 1.0 and sensorData[2]<= 1.0 and sensorData[3]<= 1.0, "sensor Data > 1.0" 
        return sensorData
    
    def getTrackState(self):
        return str(self.msg[6])
    
    def getReward(self):
        return float(self.msg[3])

        
    

        
    