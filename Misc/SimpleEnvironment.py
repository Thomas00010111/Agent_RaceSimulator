'''
Created on Nov 28, 2012

@author: mrfish
'''

# number of columns in Environment Matrix
NUMBER_OF_SIMPLE_ACTIONS = 4

# primitive actions + extended actions 
NUMBER_OF_ACTIONS = NUMBER_OF_SIMPLE_ACTIONS + 0

#number of rows
NUMBER_OF_STATES = 20

# index, i.e. row-1
GOAL_STATE = 19

import random

import Agent.Task as Agent
import Environment.IEnvironment
import Environment.RepresentationEnvironment.Action as Action
import Environment.RepresentationEnvironment.RepresentationEnvironment as RepresentationEnvironment 


class SimpleEnvironment(Environment.IEnvironment.IEnvironment):
    def __init__(self):
        ''' matrix with i rows j columns
        i: current state
        j: resulting state if action is executed
        
                        resulting state
                           [[2, 1, 3],
         current state      [3, 3, 3],
                            [2, 1, 3]]
        
        e.g. Executing action 1 in state 2 results in state 1
      
        '''
#         self.EnvironmentMatrix = [[0, 0, 0, 0, 1, 2, 2],
#                                   [0, 0, 0, 0, 1, 2, 2],
#                                   [2, 1, 0, 1, 1, 3, 2],
#                                   [2, 6, 0, 4, 1, 5, 2],
#                                   [0, 0, 0, 0, 0, 0, 0],
#                                   [2, 6, 0, 6, 1, 6, 2],
#                                   [0, 0, 0, 0, 0, 0, 0]]    #Goal
#         #                         [-1, -1, -1, -1, -1, -1, -1]]   #terminal
        
        self.EnvironmentMatrix = [[ 1, 1, 1, 1],
                                  [ 2, 2, 2, 2],
                                  [ 3, 3, 3, 3],
                                  [ 4, 4, 4, 4],
                                  [ 5, 5, 5, 5],
                                  [ 6, 6, 6, 6],
                                  [ 7, 7, 7, 7],
                                  [ 8, 8, 8, 8],
                                  [ 9, 9, 9, 9],
                                  [ 10, 10, 10, 10],
                                  [ 11, 11, 11, 11],
                                  [ 12, 12, 12, 12],
                                  [ 13, 13, 13, 13],
                                  [ 14, 14, 14, 14],
                                  [ 15, 15, 15, 15],
                                  [ 16, 16, 16, 16],
                                  [ 17, 17, 18, 18],
                                  [ 0, 0, 0, 0],
                                  [ 19, 19, 19, 19],
                                  [ 0, 0, 0, 0]]    #Goal
        #                         [-1, -1, -1, -1, -1, -1, -1]]   #terminal
        
#         # no action leads to current state
#         self.EnvironmentMatrix = [[1, 1, 1, 1, 1, 2, 2],
#                                   [0, 0, 0, 0, 2, 2, 2],
#                                   [1, 1, 0, 1, 1, 3, 3],
#                                   [2, 6, 0, 4, 1, 5, 2],
#                                   [0, 0, 0, 0, 0, 0, 0],
#                                   [2, 6, 0, 6, 1, 6, 2],
#                                   [0, 0, 0, 0, 0, 0, 0]]    #Goal
#         #                         [-1, -1, -1, -1, -1, -1, -1]]   #terminal
        self.prevState = 0
        
    
#     def executeAction(self, action):
#         self.prevState = self.EnvironmentMatrix[self.prevState][action]
#         print "Agent is going to state: ", self.prevState
    
    def getCurrentState(self):
        return self.prevState
    
    def getNumberOfStates(self):
        return NUMBER_OF_STATES
    
#     def getReachableStates(self):
#         reachableStates = []
#         action = []
#         for index, item in enumerate(self.EnvironmentMatrix[self.prevState]):
#             #if reachableStates.count(item) == 0:
#             reachableStates.append(item)
#             action.append(item)
#                     
#         print "getReachableStates: self.EnvironmentMatrix[self.prevState]:", reachableStates
#         return action, reachableStates
    
    def GotoRandomState(self, currentNState):
        ''' returns a random state that can be reached'''
        index = random.randint(0, NUMBER_OF_SIMPLE_ACTIONS-1)
        return index, self.EnvironmentMatrix[self.prevState][index]
    
    def setAction(self, action, possibleActions = None):
        self.prevState = self.EnvironmentMatrix[self.prevState][action]
        print "SimpleEnvironment: Agent is going to state: ", self.prevState
        
    
    def getRewardFromEnvironment(self):
        '''This is a hack!! Environment has to provide a reward!!!'''
        '''Currently, goal state is set in Task itself, this is only valid for internal rewards!!'''
        reward = 0
        print "Environment:getRewardFromEnvironment: reward:", reward
        return reward
    
 #   def ExecuteAction(self, action, possibleActions = None):
 #       self.prevState = self.EnvironmentMatrix[self.prevState][action]
 #       print "SimpleEnvironment: Agent is going to state: ", self.prevState
        
    def generateActions(self):    
        possibleActions = []
         
        #combine primitive and extended actions
        for index, action in enumerate(self.EnvironmentMatrix[self.getCurrentState()]):
            possibleActions.append(Action.Action(index, action))    
                             
        print "RepresentationEnvironment: possibleActions: ", possibleActions
        #return indexActions, reachableStates
        return possibleActions


        
    def restart(self):
        self.prevState = 0
        
        
if __name__ == '__main__':
    #highest 
    myEnvironment = SimpleEnvironment()
    environmRepMyAgent = RepresentationEnvironment.RepresentationEnvironment(NUMBER_OF_ACTIONS, NUMBER_OF_STATES)
    environmRepMyAgent.setEnvironment(myEnvironment)
    
    
    mySimpleAgentLaser = Agent.Task()
    mySimpleAgentLaser.setEnvironment(environmRepMyAgent)
    mySimpleAgentLaser.setRepresentationOfEnvironment(environmRepMyAgent) 
    mySimpleAgentLaser.setGoalState(GOAL_STATE)
        
#     # two actions
#     actions = []
#     environmRepAction = RepresentationEnvironment.RepresentationEnvironment(NUMBER_OF_SIMPLE_ACTIONS, NUMBER_OF_STATES)
#     environmRepAction.setEnvironment(myEnvironment)
# #    actions.append(Agent.Task())
# #    actions[0].setEnvironment(myEnvironment)
# #    actions[0].setRepresentationOfEnvironment(environmRepAction)
# #    actions[0].setStartCondition(0) 
# #    actions[0].setGoalState(3)
#         
# #    actions.append(Agent.Task())
# #    actions[1].setEnvironment(myEnvironment)
# #    actions[1].setRepresentationOfEnvironment(myEnvironment) 
# #    actions[1].setGoalState(1)
#     
#     environmRepMyAgent.setAdditionalActions(actions) 
        
    i = 0
    minDeltaV = 0.1
    while i <3000:
        print"minDeltaV:", mySimpleAgentLaser._RL.getDeltaV()
        if  mySimpleAgentLaser.goalReached:
            mySimpleAgentLaser.reset()
            myEnvironment.restart()
            i += 1
            print "i: ", i
            if  minDeltaV > max(mySimpleAgentLaser._RL.getDeltaV()):
                break
            
        mySimpleAgentLaser.Update()

            
            

            
