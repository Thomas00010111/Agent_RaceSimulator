import Environment.RepresentationEnvironment.KdTree.StateSpaceDiscretization as StateSpaceDiscretization
import Environment.RepresentationEnvironment.RepresentationEnvironment as RepresentationEnvironment


# States are integers i.e. they are not returned as numpy arrays, because they are simple numbers

class RepresentationEnvironment_ContinuousMsgFromJavaServer(RepresentationEnvironment.RepresentationEnvironment):
    def __init__(self, numberOfActions, dimension, msgParser, filename=None, levels=None):
        #		self._stateSpaceDiscetization = StateSpaceDiscretization.StateSpaceDiscetization(dimension, number_of_states)
        # 		if number_of_states==None:
        # 			self.numberOfStates = reduce(lambda x,y: x*y, dimension)
        # 		else:
        # 			#self.numberOfStates= 2**(self.levels+1)
        # 			self.numberOfStates=self._stateSpaceDiscetization.getHighestStateId+1
#        self.numberOfStates = 2 ** (levels + 1 + 1) + 1 + 1  # positive Terminal and negative Terminal State
        self.numberOfStates =levels # positive Terminal and negative Terminal State

        print "RepresentationEnvironment_ContinuousMsgFromJavaServer: numberOfStates: ", self.numberOfStates
        RepresentationEnvironment.RepresentationEnvironment.__init__(self, numberOfActions, self.numberOfStates,
                                                                     filename)
        self.reset()
        self.messageParser = msgParser
        self._prevDistRaced = 0
        self._currentDistRaced = 0
        self._tickCounter = 0
        self._deltaDistance = None
        self._deltaTime = None
        self._prevTicks = 0
        self.reward = 0
        self._currentState = None
        self._damage = 0
        self._crashed = None
        self._previousDifferentState = None
        self._rewarded = False
        #		self._numberOfActions = numberOfActions
        # How many nodes can be created maximal? Using numberOfStates leads to at least one more node than states
        # in the transition diagram
        self._stateSpaceDiscetization = StateSpaceDiscretization.StateSpaceDiscetization()
        #		self._stateSpaceDiscetization.createRepresentation(dimension, self.levels)
        self._testCounter = 0
        self._splitted = False
        self.n1 = None
        self.n0 = None
        self.action = None

    @property
    def crashed(self):
        return self._crashed

    @crashed.setter
    def crashed(self, value):
        self._crashed = value

    @property
    def stateSpaceDiscetization(self):
        return self._stateSpaceDiscetization

    def reset(self):
        # RepresentationEnvironment.RepresentationEnvironment.reset(self)
        self.actionongoing = False
        self._tempPrevState = None
        self._newStateEntered = False
        self._previousState = None
        self._previousDifferentState = None
        self._currentState = None
        self.reward = 0
        self.t = 0
        self._accumReward = 0

    def resetContinuousActionCounter(self):
        self.t = 0

    def nextStateReached(self):
        return self._newStateEntered

    # def setAction(self, action, possibleActions): Changed 11.Sep 2015, possibleActions not used in function
    def setAction(self, action):
        print "Representation of EnvironmentContinuousMsg setAction:", action
        self.action = action
        self.actionongoing = True

    # Compare updateOld() to update()
    def update(self, msg):
        assert self._stateSpaceDiscetization is not None, "create _stateSpaceDiscetization"
        self._tickCounter += 1
        self.messageParser.update(msg)

        # self._crashed = ( self.messageParser.getSensorData().any() == -1 )

        if self._rewarded:
            self._rewarded = False
        # currentState = self.numberOfStates-1 #currentState is an index, pseudo state to reward task
        #		else:
        print "Representation of EnvironmentContinuousMsg self.messageParser: ", self.messageParser.getSensorData()
        currentState = self._stateSpaceDiscetization.getState(self.messageParser.getSensorData())

        # to compatible with function updateNew()
        self._currentState = currentState
        print "Representation of Environment: currentState: ", currentState, "     self._previousState", self._previousState

        if self._newStateEntered:
            self._newStateEntered = False
            self.reward = 0
        # self.t=0

        # init
        if self._previousState is None:
            print "Representation of Environment: init"
            self._tempPrevState = currentState
            self._previousState = currentState
            self._previousDifferentState = self._previousState

        # new stateRepresentation
        elif currentState != self._tempPrevState:
            print "Representation of Environment: currentState :", currentState, "  self._tempPrevState:", self._tempPrevState, "    t: ", self.t
            self._previousState = self._tempPrevState
            self._tempPrevState = currentState
            self._previousDifferentState = self._previousState
            self._newStateEntered = True

        elif self.messageParser.getReward() == 2.0:
            print "Representation of Environment: self.messageParser.getReward(): ", self.messageParser.getReward()
            self._previousState = currentState
            self._newStateEntered = True
            self.reward = self.messageParser.getReward()
            self._rewarded = True
            # 			currentState=self.numberOfStates
            # 			self._currentState = self.numberOfStates
            currentState = self.numberOfStates - 2
            self._currentState = self.numberOfStates - 2

        elif self.messageParser.getReward() == -1.0:  # or self.messageParser.getReward() == -2.0:
            print "Representation of Environment: self.messageParser.getReward(): ", self.messageParser.getReward()
            self._previousState = currentState
            self._newStateEntered = True
            self.reward = self.messageParser.getReward()
            #self.reward = -0.01
            self._crashed = True
            # 			currentState=self.numberOfStates + 1
            # 			self._currentState = self.numberOfStates + 1
            currentState = self.numberOfStates - 1
            self._currentState = self.numberOfStates - 1

        # # new stateRepresentation
        # 		elif currentState != self._tempPrevState:
        # 			print "Representation of Environment: currentState :",currentState,"  self._tempPrevState:", self._tempPrevState, "    t: ", self.t
        # 			self._previousState = self._tempPrevState
        # 			self._tempPrevState = currentState
        # 			self._previousDifferentState = self._previousState
        # 			self._newStateEntered=True



        # 			self._currentDistRaced = self.messageParser.messageParser.getDistRaced()
        # 			self._deltaDistance = self._currentDistRaced - self._prevDistRaced
        # 			self._prevDistRaced = self._currentDistRaced
        #
        # 			self._deltaTime = self._tickCounter - self._prevTicks
        # 			self._prevTicks = self._tickCounter
        # 			self._avgSpeedRewardRaw()
        # 			self.reward = self._accumReward
        # 			self._accumReward = 0

        else:
            # reward is accumulated over one stateRepresentation
            # self.reward += self._rewardTorcs(self.messageParser)
            self._accumReward += self._rewardJavaRaceTrack(self.messageParser)

        print "End Representation of Environment: currentState: ", currentState, "     self._previousState", self._previousState, "      self._newStateEntered: ",  self._newStateEntered

    def _avgSpeedReward(self):
        timeDiff_s = self._deltaTime / 50.0  # 20ms per tick
        avgSpeed = (self._deltaDistance / timeDiff_s) / 83.3333  # normalize, max speed 300km/h .i.e. 83.33 m/s
        print "Representation Environment: avgSpeed: ", avgSpeed

    def _avgSpeedRewardRaw(self):
        avgSpeed = self._deltaDistance / self._deltaTime
        print "self._deltaDistance: ", self._deltaDistance, "    self._deltaTime: ", self._deltaTime
        print "Representation Environment: avgSpeedRaw: ", avgSpeed

    def _negReward(self):
        return -1.0

    def _rewardJavaServerActionSquares(self, sensorData):
        return sensorData.getReward()

    def _rewardJavaRaceTrack(self, sensorData):
        return sensorData.getReward()

    def getPreviousDifferentState(self):
        return self._previousDifferentState

    def getRewardFromEnvironment(self):
        return self.reward

    def getPreviousState(self):
        if self._previousState is None:
            return None
        return int(self._previousState)

    def getNextState(self):
        assert not self._train, "Training (i.e. growing of network) has to be finished before labels can be used"
        return self._stateSpaceDiscetization.getState(self.messageParser.getSensorData())

    def getCurrentState(self):
        # assert not self._train, "Training (i.e. growing of network) has to be finished before labels can be used"
        if self._currentState is None:
            return None
        return int(self._currentState)

    def getCurrentActiveState(self):
        # assert not self._train, "Training (i.e. growing of network) has to be finished before labels can be used"
        if self._currentState is None:
            return None
        return int(self._currentState)

    def getCurrentPosition(self):
        sensorDataFloat = self.messageParser.getSensorData()
        print "sensorDataFloat: ", sensorDataFloat
        return sensorDataFloat

    def getReward(self):
        print "RepresentationEnvironment: GetReward():", self.messageParser.getReward()
        return self.messageParser.getReward()

    def ContinueAction(self, maxSteps):
        print "Representation of EnvironmentContinuousMsg ContinueAction:", self.action
        print "Representation of EnvironmentContinuousMsg t=", str(self.t)
        # action is not executed immediately
        # if (self.t <maxSteps and self.getReward()!= -1.0):
        if self.t < maxSteps:
            # self.setAction(self.action, None) #11 Sept 2015 possible actions not used in function setAction
            self.setAction(self.action)
            return True
        else:
            # do not continue action because of negative reward or timeout
            self.t = 0
            return False

    def Combine(self, V, RL, nodes):
        # for node in nodes:
        #    print "stateRepresentation: ", self._stateSpaceDiscetization.getStateFromNode(node), "    V: ", self._RL.getV(self._stateSpaceDiscetization.getStateFromNode(node)),"    pos: ",node.data.pos
        # return [[node.data.pos, self._RL.getV(self._stateSpaceDiscetization.getStateFromNode(node))] for node in nodes]
        stateRepresentation = self._stateSpaceDiscetization.getStateFromNode  # reference to shorten code
        return [
            [node.data.pos, [str(stateRepresentation(node)) + "_" + str("%0.2f" % RL.getV(stateRepresentation(node)))],
             str(stateRepresentation(node)), str(RL.getV(stateRepresentation(node)))] for node in nodes]

    def rewardTask(self):
        self._rewarded = True
