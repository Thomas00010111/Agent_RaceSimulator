import random
import numpy
import mdptoolbox
import SimpleDiscreteRobotEnvironment.BaseLevel_QRL as BaseLevel
from __builtin__ import False

REWARD = 1
crashTerminalState = 99

IndexTerminalState = 100
MaxNumberOfDetailedStates = 100 + 1 # plus terminal state


class CombinedAgent(BaseLevel.BaseLevel):
    def __init__(self, environment, agents, filename=None, sparse=False):
        numberOfStates = MaxNumberOfDetailedStates
        BaseLevel.BaseLevel.__init__(self, len(agents), numberOfStates, None, sparse)
        self.agents = agents
        self.environment = environment
        self.probRandomState = 1.0
        self.goalReached = False
        self.crashed = False
        self.opponentPassed = False
        self.crashedIntoOpponent = False
       
        for agent in self.agents:
            agent.sensorModule.environment = self.environment
            agent.sensorModule.environment.resetRacePosition() 
            
        self.mappingCommonStateToState = []
        
        self.prevCommonState = None
        
        self.enhancedStates=[]
        for i in range(0, len(self.agents)):
            self.enhancedStates.append(set())
        
        self.active_tasks_idx = None
#        self.active_tasks_steps = 0
        
    
    def reset(self):
        self.goalReached = False
        self.crashed = False
        self.opponentPassed = False
        self.crashedIntoOpponent = False
        self.active_tasks_idx = None
#        self.active_tasks_steps = 0
        
    def getCommonStateId(self):
        commonStateId = ""
        for a,eh in zip(self.agents, self.enhancedStates):
            eh.add(a.sensorModule.getCurrentState())
            commonStateId = commonStateId + str(a.sensorModule.getCurrentState())
         
        if not commonStateId in self.mappingCommonStateToState:
                self.mappingCommonStateToState.append(commonStateId)
                
        return self.mappingCommonStateToState.index(commonStateId)
    
    def Update(self, msg_in):
        [t.representationOfEnv.update(msg_in) for t in self.agentsactiveTask]
        
        
    def Step(self):
        print "--------------------------------------------"
        
#         for agent in self.agents:
#             agent.environment.environment = self.environment 
#         
#         bestActionValues = []
#         value_total = numpy.zeros((4,1))
        
        # 0 is racetrack
        print "Before: ", self.agents[0].sensorModule.printEnvironment()
        
#         for idx, ag in enumerate(self.agents):
#             print idx, ": actionValue: ", ag.getPossibleActionValues(ag.environment.getCurrentState())
#             print idx, ": best action: ", ag.getPossibleActionValues(ag.environment.getCurrentState()).argmax()
#         actionValues0 = self.agents[0].getPossibleActionValues(self.agents[0].environment.getCurrentState())
#         actionValues1 = self.agents[1].getPossibleActionValues(self.agents[1].environment.getCurrentState())
#         print "actionValues0: ", actionValues0
#         print "actionValues1: ", actionValues1
        
#         max_action0 = actionValues0.argmax()
#         max_action1 = actionValues1.argmax()
#         maxValue0 = actionValues0.max()
#         maxValue1 = actionValues1.max()

        #if self.active_tasks_idx is not None and self.active_tasks_steps == 3:
        if self.active_tasks_idx is not None and self.agents[self.active_tasks_idx].sensorModule.isGoalReachedAgent:            
            commonStateId = self.getCommonStateId()
            max_action_0 = self.agents[0].getPossibleActionValues(self.agents[0].sensorModule.getCurrentState()).argmax()
            reward = self.agents[0].getPossibleActionValues(self.agents[0].sensorModule.getCurrentState())[max_action_0]
            print "Ended Task, self.prevTaskStartState: ", self.prevTaskStartState, "   self.active_tasks_idx: ", self.active_tasks_idx, "    commonStateId: ", commonStateId, "     reward: ", reward             
            
            self._RL.Update(self.prevTaskStartState, self.active_tasks_idx, commonStateId, reward)
            
            self.agents[self.active_tasks_idx].sensorModule.environment.resetRacePosition()
#            self.active_tasks_steps = 0
            self.active_tasks_idx = None 
            
        # if a task is active, continue the task
        if self.active_tasks_idx is not None:    
            print "continuing active Task: ", self.active_tasks_idx
            #post the best action group
            task_proposed_action = self.agents[self.active_tasks_idx].getPossibleActionValues(self.agents[self.active_tasks_idx].sensorModule.getCurrentState()).argmax()
            max_action = task_proposed_action
#            self.active_tasks_steps += 1
        else:
            min_actions = numpy.array([ag.getPossibleActionValues(ag.sensorModule.getCurrentState()).argmin() for ag in self.agents[1:3]])
            min_actions_value = numpy.array([ self.agents[1].getPossibleActionValues(self.agents[1].sensorModule.getCurrentState())[min_actions[0]], self.agents[1].getPossibleActionValues(self.agents[2].sensorModule.getCurrentState())[min_actions[1]] ])
            max_actions = numpy.array([ag.getPossibleActionValues(ag.sensorModule.getCurrentState()).argmax() for ag in self.agents[1:3]])
            max_actions_value = numpy.array([ self.agents[1].getPossibleActionValues(self.agents[1].sensorModule.getCurrentState())[max_actions[0]], self.agents[1].getPossibleActionValues(self.agents[2].sensorModule.getCurrentState())[max_actions[1]] ])
            
            print "tasks min action: ", min_actions, "    values: ", min_actions_value
            print "tasks max action: ", max_actions
            
            max_action_0 = self.agents[0].getPossibleActionValues(self.agents[0].sensorModule.getCurrentState()).argmax()
            max_action_0_value = self.agents[0].getPossibleActionValues(self.agents[0].sensorModule.getCurrentState())[max_action_0]
            print "max_action_0: ", max_action_0
            
            tasksRunable = self.agents[1].sensorModule.isOpponentVisible and  self.agents[2].sensorModule.isOpponentVisible
            if max_action_0 in min_actions and (min_actions_value < 1.0).all() and tasksRunable:
                # Check if this state is already known
                commonStateId = self.getCommonStateId()           
                if commonStateId in self.mappingCommonStateToState:
                    #select max task
                    self.active_tasks_idx, value = self.getBestNextAction(commonStateId)
                    self.probRandomState -= 0.005
                    if self.active_tasks_idx == -1 or random.uniform(0,1) < self.probRandomState:
                        self.active_tasks_idx = random.randint(1,2)
                        print "Combined Agent: RandomAction: ", self.active_tasks_idx, "     self.probRandomState: ", self.probRandomState
                        
                        
                else:
                    #save state and select random task
                    self.mappingCommonStateToState.append(commonStateId)
                    self.active_tasks_idx = random.randint(1,2)
                    
                print "active Task: ", self.active_tasks_idx     
                task_proposed_action = self.agents[self.active_tasks_idx].getPossibleActionValues(self.agents[self.active_tasks_idx].sensorModule.getCurrentState()).argmax()
                self.agents[self.active_tasks_idx].sensorModule.environment.resetRacePosition()
                max_action = task_proposed_action
                self.prevTaskStartState = commonStateId
#                 # now block this action
#                 actions_0 = self.agents[0].getPossibleActionValues(self.agents[0].environment.getCurrentState())
#                 idx_max_action = actions_0.argmax()
#     #            actions_0[idx_max_action] = -1            
#                 print "values in state: ", self.agents[0].environment.getCurrentState(), "  ", self.agents[0]._RL.Q[self.agents[0].environment.getCurrentState()]
#                 self.agents[0]._RL.Q[self.agents[0].environment.getCurrentState()][max_action_0] = 1.0
#                 max_action = actions_0.argmax()
            
#             elif max_actions[0]==max_actions[1] and max_actions_value[0]>1.0 and self.agents[0].getPossibleActionValues(self.agents[0].environment.getCurrentState())[max_actions[0]] > 1.0:
#                 max_action = max_actions[0]
            
            else:
                max_action = max_action_0
            

        
        maxValue = self.agents[0].getPossibleActionValues(self.agents[0].sensorModule.getCurrentState()).max()
        self.environment.executeAction(max_action)     
            
        print "max_action: ", max_action, "    maxValue: ", maxValue    
        print "Action Executed: ", self.agents[0].sensorModule.printEnvironment()
        

        #if currentNState == self.environment.GoalState:
        if self.environment.isGoalReached:
            self.goalReached = True
        
        if self.environment.crashedInWall():
            if self.active_tasks_idx is not None:
                reward = -5
                commonStateId = IndexTerminalState
#                commonStateId = self.getCommonStateId()
                print "Ended Task, self.prevTaskStartState: ", self.prevTaskStartState, "   self.active_tasks_idx: ", self.active_tasks_idx, "    commonStateId: ", commonStateId, "     reward: ", reward
                self._RL.Update(self.prevTaskStartState, self.active_tasks_idx, commonStateId, reward)
            self.crashed = True
         
        if self.environment.crashedIntoOpponent:
            assert False, "No crashes into opponents may happen"
            if self.active_tasks_idx is not None:          
                commonStateId = self.getCommonStateId()
                reward = -5
                print "Ended Task, self.prevTaskStartState: ", self.prevTaskStartState, "   self.active_tasks_idx: ", self.active_tasks_idx, "    commonStateId: ", commonStateId, "     reward: ", reward             
                self._RL.Update(self.prevTaskStartState, self.active_tasks_idx, commonStateId, reward)

            print "Crashed into opponent: currentState =", self.agents[0].sensorModule.getCurrentState(), "    ", self.agents[1].sensorModule.getCurrentState()
            self.crashedIntoOpponent = True   
            
            
            

#             commonStateId = str(self.agents[0].environment.getCurrentState()) + str(self.agents[1].environment.getCurrentState())
#              
#             if not commonStateId in self.mappingCommonStateToState:
#                 self.mappingCommonStateToState.append(commonStateId)
#                  
#             commonState = self.mappingCommonStateToState.index(commonStateId)
#             
#             assert commonState == self.getCommonStateId(), "test: must be equal "

#             R =  self.agents[0].rewardMatrix
#             R[ self.agents[1].environment.getCurrentState(), max_action1] = 5
#                         
#             P = self.agents[0]._probabilityMatrix.toASS()
#             print P
#             vi = mdptoolbox.mdp.ValueIteration(P, R, 0.9, epsilon=0.01)
#             #vi.setVerbose()
#             vi.run()
#             
#             newValues = self.agents[0].getPossibleActionValues(self.agents[0].environment.getCurrentState(), vi.V)
#             print "newValues: ", newValues
#             max_action = newValues.argmax()
#             maxValue = newValues.max()
#         else:
#             max_action = max_action0
#             maxValue = maxValue0
#         print "max_action: ", max_action, "   maxValue: ", maxValue
        
#         for agentIdx, agent in enumerate(self.agents):           
#             currentNState = agent.environment.getCurrentState()            
#             value = agent.getPossibleActionValues(currentNState, agent._RL.getVStates())
# #            bestActionValues.append((action, value, agentIdx))
#             
#             print "Step: agentIdx: ", agentIdx, "     currentState: ", currentNState, "     value: ", value
#             
#             value_total = value_total + value
#         
# #        max_action, maxValue, agentId = max(bestActionValues,key=lambda item:item[1])
#         max_action = value_total.argmax()
#         maxValue = value_total.max()
#         print "    max_action: ", max_action, "    currentNState: ", currentNState, "    maxValue: ", maxValue
        
#         self.environment.executeAction(max_action)     
        
#        prevNState = currentNState
        
#         for agentIdx, agent in enumerate(self.agents):
#             print "Action executed - Step: agentIdx: ", agentIdx, "     currentState: ", agent.environment.getCurrentState()