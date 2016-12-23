import Misc.CarState as CarState  

class IMessageParser():
    def __init__(self):
        self.cs = None 
        self.msg = None
        self.currentGoal=None
        self.sensordimension = None
                
#    def update(self, msg):
#        raise NotImplementedError( "Should have implemented this" )
    
    def getSensorData(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def getReward(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def getDimension(self):
        raise NotImplementedError( "Should have implemented this" )
    
    def update(self, msg, currentGoal=None):
        self.msg = msg
        print "MessageParserJavaEnv: update: self.msg : ", self.msg
        self.currentGoal = currentGoal
        self.cs = CarState.CarState(msg)
        print "car state: ", str(self.cs)
    
    def __str__(self):
        return str(self.msg)
        
    

        
    