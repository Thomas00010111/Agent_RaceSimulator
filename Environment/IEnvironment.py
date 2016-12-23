'''
Created on Nov 18, 2012

@author: mrfish
'''

class IEnvironment(object):
    
    def __init__(self):
        pass
    
    def getNumberOfStates(self):
        raise NotImplementedError( "Should have implemented this" )
      
    def getReachableStates(self, currentNState):
        raise NotImplementedError( "Method removed" )
    
    def getCurrentState(self):
        raise NotImplementedError( "Should have implemented this" )
      
    def GotoRandomState(self, currentNState):
        raise NotImplementedError( "Should have implemented this" )
          
    def updateTransition(self, prevState, action, currentState):
        raise NotImplementedError( "Should have implemented this" )
            
    def executeAction(self, action):
        raise NotImplementedError( "Method removed" )
    
    def setAdditionalActions(self, actions):
        raise NotImplementedError( "Should have implemented this" )
    
    def ExecuteAction(self, stateRepresentation):
        raise NotImplementedError( "Should have implemented this" )
    
    def generateActions(self):
        raise NotImplementedError( "Should have implemented this" )
    
#     def getRewardFromEnvironment(self):
#         raise NotImplementedError( "Should have implemented this. Environment has to provide reward" )
#     