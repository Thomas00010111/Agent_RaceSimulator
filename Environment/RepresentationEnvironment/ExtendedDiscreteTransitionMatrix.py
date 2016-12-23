'''
Created on Nov 18, 2012

@author: mrfish
'''
import numpy
import os
import pickle

import ProbTransitionMatrix


UNINITALLIZED = -1

class ExtendedDiscreteTransitionMatrix:
    '''
        A matrix which stores the actions that lead from one stateRepresentation on level N-1
        to another stateRepresentation on level N.
        
         State 0:
         [[ 0  1  2 -1 -1 -1 -1]
         [ 0  1  2 -1 -1 -1 -1]
         [ 0  1  2  3 -1 -1 -1]
         [ 0  1  2 -1  4  5  6]
         [ 0 -1 -1 -1 -1 -1 -1]
         [ 0  1  2 -1 -1 -1  6]
         [-1 -1 -1 -1 -1 -1 -1]]
         
         State 1:
         [[ 0  1  2 -1 -1 -1 -1]
         [ 0  1  2 -1 -1 -1 -1]
         [ 0  1  2  3 -1 -1 -1]
         [ 0  1  2 -1  4  5  6]
         [ 0 -1 -1 -1 -1 -1 -1]
         [ 0  1  2 -1 -1 -1  6]
         [-1 -1 -1 -1 -1 -1 -1]]
         
         State n:
         ...
        
        Each stateRepresentation has its own transition transition
        
        If in stateRepresentation 0 action 1 (in this case target stateRepresentation 1) is executed the agent
        goes to stateRepresentation 1. 
        ( because target stateRepresentation and action are the same in the current implementation,
        action n also leads to stateRepresentation n)
    '''  
    def __init__(self, noOfActions, noOfStates, filename = None, directory=".", loadAll=False):
        '''lazy implementation, matrixes should only be loaded when needed because of memory'''
#    def __init__(self, noOfStates, noOfActions, fileName="", loadFromFile=False):
        self._noOfActions = noOfActions
        self._noOfStates = noOfStates
        self.transitionMatrices = []
        self.directory = directory
        self.preFixFilename = filename
    
        if filename and loadAll:
            self.loadFromFile(directory, filename)
        elif filename:
            pass #load when needed
        else:
            for i in range(0,noOfStates):
                #m = ProbTransitionMatrix.ProbTransitionMatrix(noOfActions, noOfStates)
                #self.transitionMatrices.append(m)
                self.transitionMatrices.append(ProbTransitionMatrix.ProbTransitionMatrix(noOfActions, noOfStates))
                               
    def __getitem__(self, stateRepresentation):
        ''' Transition probabilities of a stateRepresentation can be accessed with 
        the [] operator, e.g. extendedDiscreteTransitionMatrix[stateRepresentation]'''
        assert(stateRepresentation < len(self.transitionMatrices)), "stateRepresentation: " + str(stateRepresentation) + "    len(self.transitionMatrices):" + str(len(self.transitionMatrices))
        assert (type(stateRepresentation) is int or type(stateRepresentation) is numpy.int32 or type(stateRepresentation) is numpy.int64), "stateRepresentation is of type: " + str(type(stateRepresentation)) + "    size: " + str(stateRepresentation.size)
        return self.transitionMatrices[stateRepresentation]        
    
#    def CalcBestAction(self, currentNstate, stateValues):
#        return self._probabilityMatrix[currentNstate].CalcBestAction(stateValues)
    
    def getNumberOfActions(self):
        return self._noOfActions
    
    def getNumberOfStates(self):
        return self._noOfStates
    
    def getClassName(self):
        return self.__class__.__name__
    
    def saveMatrizes(self, filename):
        for i in range(0,self._noOfStates):
            self.transitionMatrices[i].saveToFile(filename + str(i))
            
    def getReachableStates(self,currentState):
        return self.transitionMatrices[currentState].getReachableStates()
            
    def reset(self):
        [i.reset() for i in self.transitionMatrices]
        
    def displayProbabilityMatrix(self, state):
        print "Probability Matrix: ", state
        self.getProbabilityMatrixFromFile(state).displayProbabilityMatrix()

        
    def getProbabilityMatricesFlattened(self):
        dim = self._noOfActions*self._noOfStates*self._noOfStates
        concatPropArray=numpy.empty(dim)
        for i in range(0, self._noOfStates):
            indexStart = i*self._noOfStates*self._noOfActions
            indexEnd = (i+1)*self._noOfStates*self._noOfActions
            concatPropArray[indexStart:indexEnd] = self.getProbabilityMatrixFromFile(i).getProbabilityMatrixFlattened()
        return concatPropArray
                                     

    def dumpToFile(self, filename):
        for i,f in enumerate(self.transitionMatrices):
            f.dumpToFile(filename + str(i))
        print self.getClassName(), " dumped"
        
    def getProbabilityMatrixFromFile(self, state):
        path = self.directory + "/" + self.preFixFilename
        return ProbTransitionMatrix.ProbTransitionMatrix(0, 0, path, state)
        
    def loadFromFile(self, directory, filen):
        self.transitionMatrices = []
        print os.listdir(directory)
        loadFiles=[filename for filename in os.listdir(directory) if filename.startswith(filen)]
        for i in range(0,len(loadFiles)/2):
            m = ProbTransitionMatrix.ProbTransitionMatrix(self._noOfActions, self._noOfStates, directory+"/"+filen, i)
            self.transitionMatrices.append(m)
            
    def exists(self, filen):
        return len([filename for filename in os.listdir('.') if filename.startswith(filen)])

        
        
    

       

        
            
    


                    
    
        