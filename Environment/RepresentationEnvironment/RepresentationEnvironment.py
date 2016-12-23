'''
Created on Nov 28, 2012

@author: mrfish
'''



import numpy
import random

import Action
import Environment.IEnvironment
#import Environment.RepresentationEnvironment.ExtendedDiscreteTransitionMatrix as ExtendedDiscreteTransitionMatrix 
import GenerateDotFile_neat as GenerateDotFile


class RepresentationEnvironment(Environment.IEnvironment.IEnvironment):
    def __init__(self, numberOfActions, numberOfStates, filename=None):
        self.environment = self
        self.additionalActions = []
        self.actions = []
        self.currentState = None
        self.environmentActions = numpy.arange(0,numberOfActions)
        self._numberOfStates = numberOfStates
        self._numberOfActions = numberOfActions
#        self.numberOfActions = numberOfActions
#        self.numberOfStates = numberOfStates
#         if filename:
#             self._probabilityMatrix = ExtendedDiscreteTransitionMatrix.ExtendedDiscreteTransitionMatrix(numberOfActions, numberOfStates, filename)
#         else:
#             self._probabilityMatrix = ExtendedDiscreteTransitionMatrix.ExtendedDiscreteTransitionMatrix( numberOfActions, numberOfStates)
    
    @property
    def probabilityMatrix(self):
        return self._probabilityMatrix
    
    #----------------------
    def GotoRandomState(self, currentNState):
        ''' returns a random state that can be reached'''
        reachableNStates = self._probabilityMatrix.getReachableStates(currentNState)
        index = random.randint(0, reachableNStates.length())
        return reachableNStates[index]
     
#    def getProbability(self, state, targetState):
#        probability = self._probabilityMatrix[state].getExtendedProbability(targetState)
#        return probability
    
        
#    def updateTransition(self, prevState, action, currentState):
#        self._probabilityMatrix[prevState].updateProbability(action, currentState)
    
        
#     def getBestNextAction(self, currentNstate, vValues):
#         ''' based on the current N state and the probabilities between reachable N-1
#         states calculate the best next N-1 state. Chose N-1 so that N will be best''' 
#         return self._probabilityMatrix[currentNstate].CalcBestAction(vValues)    
        
    #-------------------       
    def getNumberOfActions(self):
        return self._numberOfActions
    
      
    def getNumberOfStates(self):
        return self._numberOfStates
    
    def generateBaseActions(self):    
        possibleActions = []
        
        for index, action in enumerate(self.environmentActions):
            possibleActions.append(Action.Action(index, action))
                               
        print "Environment: possibleActions: ", possibleActions
        #return indexActions, reachableStates
        return possibleActions
    
    def generateActions(self):    
        reachableStates = []
        indexActions = []
         
        #combine primitive actions (from environment) and extended actions
        possibleActions = self.generateBaseActions()
        
        # append extended actions to simple actions     
        for action in self.additionalActions:
            if action.getStartCondition() == self.getCurrentState():
                possibleActions.append(Action.Action(action, action.getGoalState()))
                
        for i, action in enumerate(possibleActions):
            indexActions.append(i)
            reachableStates.append(action.getGoalState())
                           
        print "RepresentationEnvironment indexActions: ",indexActions,"   targetStates(extended Action): ", reachableStates
        #return indexActions, reachableStates
        return possibleActions
        
    def setEnvironment(self, IEnvironment):
        self.environment = IEnvironment
        
    def setAdditionalActions(self, actions):
        for a in actions:
            self.additionalActions.append(a)
            
    def getAdditionalAction(self, action):
        return self.additionalActions[action]
        
    def generateGraphvicFile(self, RL, path):
        #path = "/home/mrfish/Link to MrFish/Source Code/Workspace/MountainCar/MountainCarGui"
        path = ""
        GenerateDotFile.generateGraphvicFile( self._probabilityMatrix,RL, path )
        
#    def getProbabilityMatrix(self):
#        return self._probabilityMatrix

        
        

            
