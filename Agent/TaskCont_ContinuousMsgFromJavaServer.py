'''
Created on Nov 28, 2012

@author: mrfish
'''
import random
import Agent.BaseLevel
import pickle


class Task(object, Agent.BaseLevel.BaseLevel):  # has to derived from object, otherwise @property does not work
    def __init__(self, name = None):
        print "Task init"
        Agent.BaseLevel.BaseLevel.__init__(self, name)
        self.targetState = 0
        #self.environment = None
        self.representationOfEnvironment = None
        
        self.DecreaseEpsilon = True
        self.probRandomState = 1.0     #probability to go to a random stateRepresentation
#        self.probRandomState = 0.06
        self._reduceProbabilityBy = None
        
        self.goalReached = False
        self.leftGoalState = False
        self.receivedReward = False
        self._goalState = None
        self._startCondition = None
        self.negRewardStates = []
        self.init = True
        self.goalStateReachedCounter = 0
        self.updateCounter = 0
        self._useRewardFromEnvironment = False
        self.extraReward = 0.0
#        self.accumReward = 0.0
        self.minRandomState = -99999.0;
        self.action = None
        
    @property
    def reduceProbabilityBy(self):
        return self._reduceProbabilityBy
    
    @reduceProbabilityBy.setter
    def reduceProbabilityBy(self, value):
        print "set _reduceProbabilityBy to: ", value
        self._reduceProbabilityBy = value
        
    @property    
    def goalState(self):
        return self._goalState
    
    @goalState.setter   
    def goalState(self, value):
        self._goalState = value
        
    @property
    def useRewardFromEnvironment(self):
        return self._useRewardFromEnvironment
        
    @useRewardFromEnvironment.setter
    def useRewardFromEnvironment(self, value):
        self._useRewardFromEnvironment = value
        
    @property
    def startCondition(self):
        return self._startCondition
    
    @startCondition.setter
    def startCondition(self, stateRepresentation):
        self._startCondition = stateRepresentation
        
    def reward(self, value):
        assert False, "DEBUG"
        self.extraReward = value
        
    def reset(self):
        #self.environment.setAction(0)
        self.goalReached = False
        self.leftGoalState = False
        self.receivedReward = False
        self.init = True
        
    def getGoalStateLeft(self):
        return self.leftGoalState
        
    def getGoalReached(self):
        return self.goalReached
        #return self.representationOfEnvironment.getCurrentState()==self.getGoalState()
        
    def setRepresentationOfEnvironment(self, representationOfEnv):
        """To overwrite number of states in QRL module use NumberQStates and NumberQActions. Default
        is to use the parameters from representationOfEnvironment"""
        self.representationOfEnvironment = representationOfEnv

#     def initRL(self, NumberQStates=None, NumberQActions=None):
#         # only to define more q-states than in representationOfEnvironment for growing state space
#         numberOfStates = NumberQStates or self.representationOfEnvironment.getNumberOfStates()
#         numberOfActions = NumberQActions or self.representationOfEnvironment.getNumberOfActions()    
#         self.createRL(numberOfStates, numberOfActions)  #for RL
        
    def setNegRewardState(self, states):
        self.negRewardStates = states
        
    def getRewardFromEnvironment(self):
        return self.representationOfEnvironment.getRewardFromEnvironment()
    
    
    def rlNextAction(self):
        currentState = self.representationOfEnvironment.getCurrentActiveState()
        print "TaskCont: currentState: ", currentState

        possibleActions = self.representationOfEnvironment.generateActions()
        #action = self.representationOfEnvironment.getBestNextAction(currentState, self._RL.getQValues())
        action = self._RL.getBestNextAction(currentState)
        
        print "action: ", action #, "       targetState: ", targetState
        
#         #sometimes choose a random action or if no target stateRepresentation
#         if self.DecreaseEpsilon and self.probRandomState > self.minRandomState:
#             self.probRandomState -= self._reduceProbabilityBy
        print "self.probRandomState: ", self.probRandomState
        if random.uniform(0,1) < self.probRandomState:
            action = random.randint(0, len(possibleActions)-1)
            print "Random action: ",action
        
        return action
    
    def rlUpdate(self, prevState, action):
        currentState = self.representationOfEnvironment.getCurrentActiveState()
        
        reward = self.representationOfEnvironment.getRewardFromEnvironment()
#       
#        self.accumReward += reward
#        reward = reward + self.extraReward
#        self.extraReward = 0
        #self._RL.Update(prevState, currentState, reward)
        self._RL.Update(prevState, action, currentState, reward, self.representationOfEnvironment.t)
        #self.representationOfEnvironment.updateTransition(prevState, action, currentState)
        print "TaskCont_ContinuousMsg... prevState: ",prevState,"   reward: ", reward, "    currentState: ", currentState
        
        # When the environment is left, then the just left stateRepresentation gets the reward 
        # which was collected in this stateRepresentation
        # thus, when the goal stateRepresentation is left (i.e. previousState == gaoalState) then 
        # the Rep of Env should return this reward in the method getRewardFromEnvironment().
        # As the agent will stop in this stateRepresentation, the stateRepresentation transistion has to be updated when
        # tasks are switched
        
        print "rlUpdate: self.goalState: ", self.goalState
        if currentState in self.goalState:
            self.goalReached = True
            self.goalStateReachedCounter +=1
            #reward = 5.0
            reward = self.representationOfEnvironment.getRewardFromEnvironment()
            self._RL.UpdateGoalState(currentState, reward, reward)
#            self._RL.Update(prevState, currentState, reward, 0)
            print "prevState: ",prevState,"   reward: ", reward, "    currentState: ", currentState
        
#         if self.useRewardFromEnvironment:
#             self.goalReached = True
#             reward = self.getRewardFromEnvironment()
#             self._RL.UpdateGoalState(currentState, reward, reward)
#             print "useRewardFromEnvironment prevState: ",prevState,"   reward: ", reward  ,"    currentState: ", currentState
#         
#         if currentState in self.negRewardStates:            
#         if self.representationOfEnvironment.getReward() == -1.0:
#             self.receivedReward = True
#             self._RL.UpdateGoalState(currentState, -1.0, -1.0)
      
#        deltaRL = abs(self._RL.getV(prevState) - self._RL.getV(currentState))
        return self.goalReached
        

    def Update(self):
        print "---- Update(): ", self.name, " ------"
        self.updateCounter += 1
        if self.init:
            print "Update init"
            if not self.representationOfEnvironment.getCurrentState() in self.goalState:
                self.init = False
                #select new action
                #self.prevState = self.representationOfEnvironment.getCurrentState()
                self.action = self.rlNextAction()
                #possibleActions = self.representationOfEnvironment.generateActions()
                #self.representationOfEnvironment.setAction(self.action, possibleActions) #11 Sept 2015 possible actions not used in function setAction
                self.representationOfEnvironment.setAction(self.action) 
            else:
                self.goalReached = True
                self.init = False
            
            return self.action
        
        # reduce probability with every primitive action
        if self.DecreaseEpsilon and self.probRandomState > self.minRandomState:
            self.probRandomState -= self._reduceProbabilityBy
        
        #continue action while in same (or goal) stateRepresentation 
        if not self.representationOfEnvironment.nextStateReached():
            print "Task: Same stateRepresentation, continue action"
            if (self.representationOfEnvironment.ContinueAction(10000)): # 20ms*10000=200s i.e. no change in stateRepresentation
                return None
#             if self.goalReached:
#                 print "Task: In goal stateRepresentation, continue action"
#                 self.representationOfEnvironment.ContinueAction(9999999999)
#                 return None
#             elif (self.representationOfEnvironment.ContinueAction(10000)): # 20ms*10000=200s i.e. no change in stateRepresentation
#                 return None

            
#         if self.representationOfEnvironment._splitted:
#             self._RL.setV(self.representationOfEnvironment.n0, self._RL.getV(self.representationOfEnvironment.getPreviousState()))
#             self._RL.setV(self.representationOfEnvironment.n1, self._RL.getV(self.representationOfEnvironment.getPreviousState()))
            
        # goal stateRepresentation entered
        if self.representationOfEnvironment.nextStateReached() and self.getGoalReached():
            print "Task: left goal stateRepresentation"
            self.leftGoalState = True
            return None

            
#        #new stateRepresentation, i.e. action finished update RL   
#        if(self.rlUpdate(self.representationOfEnvironment.getPreviousState(), self.action)):
#            return None

        #new stateRepresentation, i.e. action finished update RL
        self.rlUpdate(self.representationOfEnvironment.getPreviousState(), self.action)
        if self.getGoalReached():
            return None
        
        #select new action
        self.action = self.rlNextAction()
        #possibleActions = self.representationOfEnvironment.generateActions() 11 Sept 2015 possible actions not used in function setAction
        self.representationOfEnvironment.resetContinuousActionCounter()
        #self.representationOfEnvironment.setAction(self.action, possibleActions)
        self.representationOfEnvironment.setAction(self.action) 
        
        return self.action    
       
    
    def getBestNextState(self, currentNstate, reachableStates):
        bestNState = None
        maxV = -1.0
        action = 0
        index = 0

        for r in reachableStates:
            V = float(self._RL.getV(r))
            if V > maxV:
                maxV = V
                bestNState = r
                action = index
            index+=1    
                
        return action, bestNState
    
    def log(self):
        logStr= str(self.updateCounter) + ";" + str(self.goalStateReachedCounter) + ";" + str( self.probRandomState)
        filename = "StepsVsGoal_" + str(self.name) + ".txt"
        super(Task,self).log(logStr, filename, 'ab')
        
    def loadGoalStatesFromFile(self, filename):
        self._goalState = pickle.load(open(filename + ".pkl", 'rb'))
    
        
    def dumpGoalStates(self, filename):
        pickle.dump(self._goalState, open(filename + ".pkl", 'wb'))             
        
      

# Method is not used. Remove, because it uses reference to environment    
#     def getRandomAction(self):
#         randAction = random.randint(0, self.environment.getNumberOfStates() -1)            
#         print "SimpleAgent: getBestNextState: Random maxAction = ", randAction
#         return randAction
                

                    