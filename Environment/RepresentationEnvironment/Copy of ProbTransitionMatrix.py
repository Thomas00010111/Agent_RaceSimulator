'''
Created on Nov 18, 2012

@author: mrfish
'''

import numpy
import pandas
import sys
import cPickle as pickle


UNINITALLIZED = -1

class ProbTransitionMatrix:
    '''
        A matrix which stores the actions that lead from one stateRepresentation on level N-1
        to another stateRepresentation on level N.
        
         [[ 0  1  2 -1 -1 -1 -1]
         [ 0  1  2 -1 -1 -1 -1]
         [ 0  1  2  3 -1 -1 -1]
         [ 0  1  2 -1  4  5  6]
         [ 0 -1 -1 -1 -1 -1 -1]
         [ 0  1  2 -1 -1 -1  6]
         [-1 -1 -1 -1 -1 -1 -1]]
        
        If in stateRepresentation 0 action 1 (in this case target stateRepresentation 1) is executed the agent
        goes to stateRepresentation 1. 
        ( because target stateRepresentation and action are the same in the current implementation,
        action n also leads to stateRepresentation n)
    '''
     
    def __init__(self, noOfActions, noOfStates, filename=None, loadId=None):
        self._noOfStates = noOfStates
        self._noOfActions = noOfActions
        #print "Init ", self.getClassName(), " self._noOfActions: ", self._noOfActions, "   self._noOfStates: ", self._noOfStates
        
#        if path:
#            print self.getClassName() + " loading _probabilityMatrix and _transitionMatrix from: ", path  
#            self._probabilityMatrix = numpy.load(path + "_probabilityMatrix")
#            self._transitionMatrix = numpy.load(path + "_transitionMatrix")
#        else:
#            # probability to reach a stateRepresentation with a given action
#            self._probabilityMatrix = numpy.empty((noOfActions,noOfStates), dtype = float)
#            self._probabilityMatrix.fill(0.0)
#            
#            # count transitions to stateRepresentation s' with action a
#            self._transitionMatrix = numpy.empty((noOfActions,noOfStates), dtype = int)
#            self._transitionMatrix.fill(0)

        if filename:
            f = open(filename + str(loadId) + "_probabilityMatrix")
            self._probabilityMatrix = pickle.load(f)
            f.close()
            f = open(filename + str(loadId) + "_transitionMatrix")
            self._transitionMatrix = pickle.load(f)
            f.close()
            self._noOfStates = self._probabilityMatrix.shape[1]
            self._noOfActions = self._probabilityMatrix.shape[0]
        else:
            # probability to reach a stateRepresentation with a given action
            self._probabilityMatrix = numpy.empty((noOfActions, noOfStates), dtype = float)
            self._probabilityMatrix.fill(0.0)
            
            # count transitions to stateRepresentation s' with action a
            self._transitionMatrix = numpy.empty((noOfActions, noOfStates), dtype = int)
            self._transitionMatrix.fill(0)
                
    def reset(self):
        # probability to reach a stateRepresentation with a given action
        self._probabilityMatrix = numpy.empty(( self._noOfActions,self._noOfStates), dtype = float)
        self._probabilityMatrix.fill(0.0)
        # count transitions to stateRepresentation s' with action a
        self._transitionMatrix = numpy.empty(( self._noOfActions,self._noOfStates), dtype = int)
        self._transitionMatrix.fill(0)
        
    def __str__(self):
        strProbMatrix = str(self._probabilityMatrix.tolist()).replace("], [", "] \n [")
        strTransMatrix = str(self._transitionMatrix.tolist()).replace("], [", "] \n [")
        return "probabilityMatrix:\n" + strProbMatrix + "\n" + "transitionMatrix:\n" + strTransMatrix 
    
    @property
    def probabilityMatrix(self):
        return self._probabilityMatrix
    
    def getProbabilityMatrixFlattened(self):
        return self._probabilityMatrix.flatten()
    
    def getRowprobabilityMatrix(self, row):
        return self._probabilityMatrix[row]  
    
    def getProbabilityMatrixAsList(self):
        return self._probabilityMatrix.tolist()   
      
    def getNumberOfStates(self):
        return self._noOfStates
    
    def getNumberOfActions(self):
        return self._noOfActions
      
    def updateProbability(self, action, currentState):
        '''To answer the question how often an action lead from prevState to currentState '''
        print "updateProbability: action:" , action, "    currentState: ", currentState
        self._transitionMatrix[action][currentState] += 1
        sumRow = numpy.sum(self._transitionMatrix[action])
        self._probabilityMatrix[action] = self._transitionMatrix[action]/float(sumRow)
        #print  "transitionMatrix: \n", self._transitionMatrix  
        #print  "probabilityMatrix: \n", self._probabilityMatrix
        
    def getActionsToReachState(self, stateRepresentation):
        actionProbability = []
        for a in range(0,self._noOfActions):
            #transitions = self._transitionMatrix[a][stateRepresentation]
            probability = self._probabilityMatrix[a][stateRepresentation]
            actionProbability.append([a,probability] )    
        return actionProbability

    
    def getReachableStates(self):
        '''
        returns list with all states, the best action to reach this stateRepresentation, 
        and the probability to reach this stateRepresentation with the given action 
        '''
        actionProbability = []        
        for s in range(0,self._noOfStates):
            actions = self.getActionsToReachState(s)
            #append action with highest probability
            actionProbability.append([s, max(actions,key=lambda x: x[1])])
        return actionProbability   

        
    def getProbability(self, action, stateRepresentation):
        return self._probabilityMatrix[action][stateRepresentation]

    def getSumActionCalled(self, action):
        return numpy.sum(self._transitionMatrix[action])

    def CalcBestAction(self, stateValues):
        assert (self.getNumberOfStates() == len(stateValues)), "self.getNumberOfStates(): %r   len(stateValues): %r" % (self.getNumberOfStates(),  len(stateValues))  
#        print "CalcBestAction: self._probabilityMatrix: \n", self._probabilityMatrix
#        print "CalcBestAction: stateValues: \n", stateValues
        states = numpy.dot(self._probabilityMatrix, stateValues)
        print "CalcBestAction: states: \n", states
        return states.argmax()
    
    def displayProbabilityMatrix(self):
        pandas.set_option('display.width', 4000)
        pandas.set_option('max_rows',200)
        pandas.set_option('max_columns',4000)
        row_labels = range(0,self._noOfActions)
        column_labels = range(0,self._noOfStates)

        df=pandas.DataFrame(self._probabilityMatrix, columns=column_labels, index=row_labels)
        df=df[df.columns[(df != 0).any()]]
        print df

    
    def display(self):
        ''' print numpy array is not possible, there seems to be a bug in array2string function'''
        strProbMatrix = str(self._probabilityMatrix.tolist()).replace("], [", "] \n [")
        strTransMatrix = str(self._transitionMatrix.tolist()).replace("], [", "] \n [")
        print strProbMatrix
        print strTransMatrix
        
        
    def dumpToFile(self, filename):
        try:
            f_ex = open(filename + "_probabilityMatrix", 'wb')
            #numpy.save( self._probabilityMatrix, f_ex)
            self._probabilityMatrix.dump(f_ex)
            f_ex.close()
            
            f_ex = open(filename + "_transitionMatrix", 'wb')
            #numpy.save( self._transitionMatrix, f_ex)
            self._transitionMatrix.dump(f_ex)
            f_ex.close()
            print self.getClassName(), " dumped ", str(filename)
        except:
            print "WARNING: Could not save probability and transition matrix!"
            print  sys.exc_info()[0]
                
#    def saveToFile(self, filename):
#        filenameprob = filename + '_probabilityMatrix.txt'
#        print "probabilityMatrix saving to :", filenameprob
#        strProbMatrix = str(self._probabilityMatrix.tolist()).replace("], [", "] \n [")

#        filenametrans = filename + '_transitionMatrix.txt'
#        print "transitionMatrix saving to :", filenametrans
#        strTransMatrix = str(self._transitionMatrix.tolist()).replace("], [", "] \n [")
#        print strTransMatrix
     
    
    def getClassName(self):
        return self.__class__.__name__
        
                      
        