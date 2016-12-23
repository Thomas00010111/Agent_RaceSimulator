import numpy

class StateInformation:
    def __init__(self, rl, dimensionLaser):
        self._rl = rl
        self.prevLaser = None
#        self._currentLaser = None
#        self._previousState = None
#        self._previousAction = None
        self.avg_laser = numpy.zeros((4, 2, dimensionLaser)) #actions, som id, laser dim
        self.actionExecutionCounter = numpy.zeros(4)

    def Update(self, action, som_id, currentLaser):
        self.avg_laser[action][som_id] = (self.avg_laser[action][som_id] + currentLaser) /2.0
        print "self.avg_laser[action][som_id] ",action," ", som_id, ": ",  self.avg_laser[action][som_id]
        self.actionExecutionCounter[action]+=1

    def getSplitPointAndAxis(self, action):
        if (self.avg_laser[action][0] == 0).all():
            splitPoint = self.avg_laser[action][1]
        elif (self.avg_laser[action][1] == 0).all():
            splitPoint = self.avg_laser[action][0]
        else:
            splitPoint = (self.avg_laser[action][0] + self.avg_laser[action][1])/2.0
        deltaLaser = abs(self.avg_laser[action][0] - self.avg_laser[action][1])
        split_axis = numpy.argmax(deltaLaser)
        print "splitPoint: ", splitPoint, "    split_axis: ", split_axis
        return splitPoint, split_axis

    def actionCount(self, action):
        return self.actionExecutionCounter[action]


