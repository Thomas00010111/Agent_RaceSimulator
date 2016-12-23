import Agent.TaskCont_ContinuousMsgFromJavaServer as Agent

#MaxNumberQStates = 10000

class MainAgent(object):    # has to be derived from object, otherwise @property does not work 
    def __init__(self, representationEnvironment):
        print "MainAgent init"
        self.mySimpleAgent = Agent.Task("JavaMainAgent")
        
        self.mySimpleAgent.setRepresentationOfEnvironment(representationEnvironment) 
#        self.mySimpleAgent.initRL()
#        self.mySimpleAgent.initRL(NumberQStates = MaxNumberQStates)
        
#        representationEnvironment.rl = self.mySimpleAgent.rl

#        self.mySimpleAgent.reduceProbabilityBy = 0.000008   # reduce with every primitive action
#        self.mySimpleAgent.reduceProbabilityBy = 0.00001   # 5d delta very small, but several hours running time    
#        self.mySimpleAgent.reduceProbabilityBy = 0.00001    #2D
#        self.mySimpleAgent.reduceProbabilityBy = 0.000007   #2D adapt Env
#        self.mySimpleAgent.reduceProbabilityBy = 0.000001   #3D adapt Env
        self.mySimpleAgent.reduceProbabilityBy = 0.000008
        self.mySimpleAgent.minRandomState = 0.05
        
        
    @property
    def representationOfEnv(self):
        return self.mySimpleAgent.representationOfEnvironment
    
    @representationOfEnv.setter
    def representationOfEnv(self, value,  NumberQStates = None):
        self.mySimpleAgent.setRepresentationOfEnvironment(value, NumberQStates)    
    
    def onShutdown(self):
        self.mySimpleAgent.rl.writeLogfile("VLog_Agent")
        
    def reset(self):
        self.mySimpleAgent.reset()
        self.representationOfEnv.reset()
        
        
    def Update(self, msg_in):
        print "MainAgent: Updated driver"
        # Call Agent to set action
        self.mySimpleAgent.Update()
        state, myActionStr, actionId = None, None, None
        
        if self.representationOfEnv.crashed:
            self.reset()
            self.representationOfEnv.crashed = False
            state = "crashed"
            print "MainAgent: ", state 
            #prevEnvironmentTicks=0
            
        elif self.mySimpleAgent.getGoalReached():           
            self.reset()
            self.representationOfEnv.goalReached= False
            state = "goalreached"
            print "MainAgent: ", state 
            
        elif self.representationOfEnv._rewarded:           
            self.reset()
            self.representationOfEnv._rewarded = False
            state = "rewarded"
            print "MainAgent: ", state 
            
#         elif self.mySimpleAgent.getGoalReached():           
#             self.reset()
#             self.representationOfEnv.goalReached= False
#             state = "goalreached"
#             print "MainAgent: ", state 
        
        # CROSSED should happen later, but still in one of the goal states
#             elif self.mySimpleAgent.goalReached or msg_in[6] == "CROSSED":
#                 if msg_in[6] == "CROSSED":
#                     self.mySimpleAgent.goalState.append(self.representationOfEnv.getPreviousDifferentState()) 
#                 print "goal State reached"
#                 numberLineCrossed+=1
#                 ax1.plot(numberLineCrossed, prevEnvironmentTicks, 'o')
#                 ax2.plot(numberLineCrossed, self.mySimpleAgent.probRandomState,'+')
#                 plt.draw()
#                 prevEnvironmentTicks=0
#                  
#                 self.mySimpleAgent.reset()
#                 self.representationOfEnv.reset()
#                 myEnvironment.setToStart()
        
#         elif msg_in[6] == "CROSSED_GOAL_WRONG_DIRECTION":
#             print "CROSSED_GOAL_WRONG_DIRECTION"
#             self.reset()
#             state="CROSSED_GOAL_WRONG_DIRECTION"
            
        else:
            speed = 4.0
            if self.representationOfEnv.action >= 4: 
                speed = 4.0

            action = self.representationOfEnv.action % 4
            myActionStr = "ACTION:" + str(action) + ":" + str(speed)
            actionId = action
            state="action"
            
                
#             #send signals to update GUI
#             if (updateCounter%2000 == 0):
#                 # Use this event to update 2D GUI which shows node and car positions     
#                 #self.emit(QtCore.SIGNAL("replotEvent(PyQt_PyObject, PyQt_PyObject)"), self.representationOfEnv.Combine(self.mySimpleAgent._RL.getVStates(),self.mySimpleAgent._RL, self.representationOfEnv.stateSpaceDiscetization.gng.graph.nodes), self.representationOfEnv.sensorData.getSensorData())
#                 v = self.mySimpleAgent._RL.getVStates()
#                 scalars = v.reshape(1,v.shape[0])[0]
#                 graph.update(nodes, scalars)
#                 time.sleep(0.4)       
             
#             if (updateCounter%2000 == 0):   
#                   
#                 logStr= str(updateCounter) + ";" + str(self.mySimpleAgent.accumReward) + ";" + str(self.mySimpleAgent.probRandomState)
#                 filename = "StepsVsGoal_" + str(self.mySimpleAgent.name) + ".txt"
#                 self.log(logStr, filename, 'ab')
#                                   
#                 time.sleep(0.5)
        
        return state, myActionStr, actionId
    
    def saveVvalues(self):
        self.mySimpleAgent.saveVvalues()

        
        
        
        