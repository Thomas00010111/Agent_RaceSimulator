'''
Created on Nov 18, 2012

@author: mrfish
'''

import numpy
import itertools

InitalValueDeltaV = 99999
NUMBEROFLOGVALUES = 1000000


class RL(object):
    def __init__(self, numberOfStates):
        self.V = numpy.zeros((numberOfStates,1))
        #self.V = numpy.ones((numberOfStates,1))
        self.deltaV = numpy.full((numberOfStates,1), InitalValueDeltaV, dtype=numpy.float)
        self._alpha = 0.5
        self.gamma = 0.7
        print "self.gamma",self.gamma
        #save stateRepresentation transitions that were rewarded
        #self.rewardedTransitions = numpy.zeros((numberOfStates,numberOfStates),dtype = int)
        
        self.VlogCounter = 0
        self.Vlog=numpy.zeros((NUMBEROFLOGVALUES, 2))
        
    
    @property
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        print "self.alpha = ", self._alpha
        self._alpha = value
        
        
    def Update(self, prevState, currentState, reward, t=1):
        # Sutton, formula (6.2)
        oldV = self.V[prevState].copy()
        self.V[prevState] = self.V[prevState] + self._alpha * (reward + self.gamma**t * self.V[currentState]-self.V[prevState])
        #print "V:", self.V
        self.deltaV[prevState]=abs(oldV-self.V[prevState])
        
#         if reward != 0:
#             self.rewardedTransitions[prevState][currentState] += 1
            
        #log
        self.Vlog[self.VlogCounter]=[prevState, self.V[prevState]]
        self.VlogCounter+=1    
            
    def UpdateGoalState(self, goalState, vValueVirtualState, reward):
        # the virtual stateRepresentation in which the agent "slides" is never updated,
        # thus always equal 0
        oldV = self.V[goalState].copy()
        self.V[goalState] = self.V[goalState] + self._alpha * (reward + self.gamma * vValueVirtualState -self.V[goalState])
        self.deltaV[goalState]=abs(oldV-self.V[goalState])
        
        #log
        self.Vlog[self.VlogCounter]=[goalState, self.V[goalState]]
        self.VlogCounter+=1    
    
    def getVStates(self):
        return self.V
    
    def getDeltaV(self, state):
        return self.deltaV[state]

    def getV(self, stateRepresentation):
        return self.V[stateRepresentation].copy()
    
    def setV(self, stateRepresentation, value):
        self.V[stateRepresentation] = value
        
#     def getRewardedTransitions(self, fromState, toState):
#         print "self.rewardedTransitions: ", self.rewardedTransitions
#         return self.rewardedTransitions[fromState][toState]
#     
    def writeLogfile(self, filename):
        print "RL: writeLogfile"
        numpy.save(filename, self.Vlog[0: self.VlogCounter])
        
        
    def save(self, filename):
        # write V-values as columns

        filename = filename + '_V_log.csv'
        f = open(filename, 'w')
        print "RL: saving to :", filename
        
        for state,v in enumerate(self.V):
            for item in v:
                f.write(str(state) + ": " + str(item) + ";")
            f.write("\n")
        f.close()
        numpy.save(filename+".pkg", self.V)
            
        
        
        