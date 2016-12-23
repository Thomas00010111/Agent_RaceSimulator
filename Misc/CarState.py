class CarState():
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return str(self.msg)
    
    def getDistRaced(self):
        return float(self.msg[5])
    
    def getSpeed(self):
        return float(self.msg[7])
    
    def getTicks(self):
        return int(self.msg[8])