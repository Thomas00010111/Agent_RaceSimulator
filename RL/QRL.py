'''
Created on Nov 18, 2012

@author: mrfish
'''

import numpy
import pickle

NUMBEROFLOGVALUES = 1000000

class RL(object):
    def __init__(self, numberOfStates, numberOfActions):
        self.Q = numpy.ones((numberOfStates,numberOfActions))
        self.Q_variance = numpy.zeros((numberOfStates,numberOfActions))
        self.Q_variance.fill(numpy.NaN) 
        self.Q_reliable = numpy.zeros((numberOfStates,numberOfActions))
        self._alpha = 0.1
        self.updateQ = None
        #self.gamma = 0.9
        self.gamma = 0.99 # using t, 0.9 might decay too fast 0.9^5= 0.59
#        self._numberOfStates = numberOfStates
        
#         self._alpha = 0.5
#         self.gamma = 0.7
        
#        self.VlogCounter = 0
#        self.Vlog=numpy.zeros((NUMBEROFLOGVALUES, 2))
    
    @property
    def alpha(self):
        return self._alpha
    
    @alpha.setter
    def alpha(self, value):
        print "self._alpha = ", self._alpha
        self._alpha = value
    
    def getNumberOfStates(self):
        return self.Q.shape[0]
        
    def Update(self, prevState, action, currentState, reward, t=1):
        assert t>0, "QRL: t <= 0"
        self.Q_reliable[prevState][action]+=1 
        Q_old = self.Q[prevState][action].copy()
        bestAction = numpy.argmax(self.Q[currentState])
        # Sutton, formula (6.6), off-policy because of chosinf best action. compare (6.5)
        self.updateQ = reward + self.gamma**t * self.Q[currentState][bestAction]
        self.Q[prevState][action] = self.Q[prevState][action] + self._alpha * (self.updateQ-self.Q[prevState][action])
        
        # Warum den max wert aus Q_prev und Q_current? Macht Sinn die aenderung relativ zum vorherigen bzw. aktuellen Q-Wert zu sehen und nicht absolut aber
        # warum max?
        self.Q_variance[prevState][action] = abs(Q_old-self.Q[prevState][action]) / max([abs(Q_old), self.Q[prevState][action]])
        print "QRL Q:\n", self.Q
        
    def UpdateGoalState(self, goalState, qValueVirtualAction, reward):
        # goal state is a state in which all actions lead to a virtual state with only very high valued action
        oldQ = self.Q[goalState].copy()
        self.Q[goalState] = self.Q[goalState] + self._alpha * (reward + self.gamma * numpy.full(oldQ.shape,qValueVirtualAction)-self.Q[goalState])
        #self.V[goalState] = self.V[goalState] + self._alpha * (reward + self.gamma * vValueVirtualState -self.V[goalState])
        #self.deltaV[goalState]=abs(oldV-self.V[goalState])
        
        #log
        #self.Vlog[self.VlogCounter]=[goalState, self.V[goalState]]
#        self.VlogCounter+=1    
    
    def getVariance(self):
        min_var = numpy.nanmin(self.Q_variance)
        mean = numpy.nansum(self.Q_variance)/(~numpy.isnan(self.Q_variance)).sum() # number of not NaNs in array 
        max_var = numpy.nanmax(self.Q_variance)  
        return [min_var, mean, max_var]
    
    def getDeltaNormalized(self, state, action):
        return self.Q_variance[state][action]
    
    def getQValues(self):
        return self.Q

    def getQ(self, stateRepresentation, action):
        return self.Q[stateRepresentation][action]
    
    def getQvalues(self, state):
        return self.Q[state]
    
    def setQvalues(self, state, values):
        self.Q[state]=values
    
    def setQ(self, stateRepresentation, action, value):
        self.Q[stateRepresentation][action] = value
        
    def getBestNextAction(self, currentNstate):
        return numpy.argmax(self.Q[currentNstate])  
        
    def save(self, filename):
        # write Q-values as columns

        filename = filename + '_Q_log'
        numpy.save(filename, self.Q)
        pickle.dump(self, open(filename + ".pkl", 'wb'))
#         f = open(filename, 'w')
#         print "RL: saving to :", filename
#         
#         for q in self.Q:
#             for item in q:
#                 f.write(str(item) + ";")
#             f.write("\n")
#         f.close()
            
        
        
        