
# 
# Use Lasers to detect Opponents
#
import numpy

import Misc.IMessageParser as IMessageParser

DistanceSensor = 0
OpponentSensor = 1
 
SensorDataStart = 9
Dimension_DistanceSensor = 2
Dimension_OpponentSensor = 5

#Dimension = Dimension_DistanceSensor

class MessageParserJavaEnv(IMessageParser.IMessageParser):        
    @property
    def carState(self):
        return self.cs
    
    @property
    def Dimension(self):
        return self.sensordimension
    
    def setSensorType(self, sensorType):
        if sensorType == DistanceSensor:
            self.sensordimension = 2
            self.getSensorDataFct = self.getSensorDataDistance
        elif sensorType == OpponentSensor:
            self.sensordimension = 5
            self.getSensorDataFct = self.getSensorDataOpponent
        else:
            self.sensordimension = None
            self.getSensorDataFct = None
    
    def getDimension(self):
        return self.sensordimension
        
           
    def getSensorData(self):
        return self.getSensorDataFct()
#        return self.getSensorDataDistance()
#        return self.getSensorDataOpponent()
    
    def getSensorDataDistance(self):
        sensorData = numpy.empty(self.sensordimension)
        
        #laser starting from [9]
        for i in range(Dimension_DistanceSensor):
            sensorData[i]=float(self.msg[SensorDataStart + i])/200.0
            #circle_rad = math.pi * 2.0
            #sensorData[3] = float(self.msg[2])/circle_rad

            assert sensorData[i]<= 1.0, "sensor Data > 1.0" 
        return sensorData       
           
    def getSensorDataOpponent(self):
        sensorData = numpy.empty(self.sensordimension)
        
        #laser starting from [9]
        StartIndex = SensorDataStart + Dimension_DistanceSensor
        for i in range(Dimension_OpponentSensor):
            sensorData[i]=float(self.msg[StartIndex + i])/150.0        
        
#         sensorData[0]=float(self.msg[12])/150.0
#         sensorData[1]=float(self.msg[13])/150.0
#         sensorData[2]=float(self.msg[14])/150.0
#         sensorData[3]=float(self.msg[15])/150.0
#         sensorData[4]=float(self.msg[16])/150.0
        #circle_rad = math.pi * 2.0
        #sensorData[3] = float(self.msg[2])/circle_rad

            assert sensorData[i]<= 1.0, "sensor Data > 1.0"  
            
        return sensorData
    
    def getTrackState(self):
        return str(self.msg[6])
    
    def getReward(self):
        return float(self.msg[3])

        
    

        
    