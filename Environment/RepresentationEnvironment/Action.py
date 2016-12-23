

class Action():
    def __init__(self, startCondition, action, targetStates=[]):
        self.extended = False
        self.action = None
        self.targetStates = None
        self.setAction(action)
        self.targetStates = targetStates
    
    def setAction(self, action):
        self.action = action
#         if isinstance(action, Agent.Task.Task):
#             self.extended = True
    
#     def isExtendenAction(self):
#         return self.extended
    
    def getGoalState(self):
        return self.targetStates
    

        
    