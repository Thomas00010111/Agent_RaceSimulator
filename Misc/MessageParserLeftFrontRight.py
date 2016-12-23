
import numpy

import Misc.IMessageParser as IMessageParser
import SimplePythonClient.CarState as CarState


class MessageParserLeftFrontRight(IMessageParser.IMessageParser):
    def __init__(self):
        self.cs = None 
        self.msg = None
        
    @property
    def carState(self):
        return self.cs
    
    def update(self, msg):
        self.cs = CarState.CarState(msg)
        print "car state: ", str(self.cs)
        
    def getSensorData(self):
#         sensorL = cs.getTrack(5)/200
#         sensorM = cs.getTrack(9)/200
#         sensorR = cs.getTrack(13)/200
#         speed = cs.getSpeedX()/200      #max 200km/h
        frontAndSpeed = numpy.array([self.cs.getTrack(5), self.cs.getTrack(9), self.cs.getTrack(13)]).astype(numpy.float)/200.0
        return frontAndSpeed
    
    def getReward(self):
        # From where should the reward come from??
        #return float(self.msg[3])
        return 0

        
    

        
    