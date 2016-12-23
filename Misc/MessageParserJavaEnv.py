
import numpy

import Misc.IMessageParser as IMessageParser 

Dimension = 2

class MessageParserJavaEnv(IMessageParser.IMessageParser):
        
    @property
    def carState(self):
        return self.cs
           
    def getSensorData(self):
        return numpy.array(self.msg[0:2]).astype(numpy.float)/200.0
    
    def getTrackState(self):
        return str(self.msg[6])
    
    def getReward(self):
        return float(self.msg[3])

        
    

        
    