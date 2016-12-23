'''
Created on Nov 28, 2012

@author: mrfish

Uses: Java Eistuete mit Dreirad. Es werden alle drei Koordinaten in einen State uebersetzt.
Ohne SOM.

'''
from PyQt4 import QtCore
import PyQt4
import atexit
import datetime
import numpy
import sys
import time

import Agent.JavaMainAgent as Agent
import Environment.IEnvironment
import Environment.RealEnvironment.JavaSomEnvironment as JavaEnvironment
import Environment.RepresentationEnvironment.RepresentationEnvironment_ContinuousMsgFromJavaServer as RepresentationEnvironment 
import Environment.RepresentationEnvironment.SOM.Gui as Gui
import Environment.RepresentationEnvironment.SOM.Gui2D as Gui2D
import Misc.MessageParserJavaEnv as MsgParser2D
import Misc.MessageParserJavaEnvLaser2D as MsgParser
#import Misc.MessageParserJavaEnv3D as MsgParser
#import Misc.MessageParserJavaEnvLaser4D as MsgParser
import Environment.RepresentationEnvironment.AdaptEnvironment as AdaptEnvironment

import PyQt4.Qwt5 as Qwt
import matplotlib.pyplot as plt  
import pickle
import cProfile
import kdtree

#import Agent.MainAgent as Agent
#import Misc.MessageParserJavaEnvLaser4D as MsgParser
#import mayavi.mlab
#sys.stdout = open('output_environment.txt', 'w')
#NUMBER_OF_ACTIONS = 4 * 2       #n,s,e,w and 2 speeds
NUMBER_OF_ACTIONS = 4        #n,s,e,w


#NUMBER_OF_SIMPLE_ACTIONS = 4
SIZEofSTATE = 20
SIZExy = 200
STATESORIENTATION = 10
NUMBEROFSTATESONEDIRECTION = SIZExy/SIZEofSTATE
NUMBER_OF_STATES_JAVA_WORLD = SIZEofSTATE * SIZEofSTATE * STATESORIENTATION
UPDATEDRAWINGSTEPS = 7
#NUMBER_OF_STATES = NUMBER_OF_STATES_JAVA_WORLD

DIMENSION = MsgParser.Dimension

#ACTION_TIME_COUNTER = 1000
ACTION_TIMEOUT_COUNTER = 5000

NUMBER_OF_ACTIONS_HL = 4    #left, right, up, down
DIMENSION_HL = MsgParser2D.Dimension
GOAL_STATE_HL = 23
levels_HL = 4
#NUMBER_OF_STATES_HL = 2**(levels_HL+1)    # actually -1, removed for extra state i.e. terminal state


#Actually the number of states in the kd-tree is  2**(levels+1)-1
# but we want an extra state
levels = 7
NUMBER_OF_STATES = 2**(levels+1)    # actually -1, removed for extra state i.e. terminal state


FileNameProbMatrices = "Probab1l1tyMatr1x3D"

class JavaEnvironmentEistuete(JavaEnvironment.JavaSomEnvironment, QtCore.QThread):
    def __init__(self, numberOfStates, parent=None):
        QtCore.QThread.__init__(self,parent)
        JavaEnvironment.JavaSomEnvironment.__init__(self, numberOfStates)
        self.sensorData = numpy.array([0, 0])
        #self.stateSpaceDiscetization = StateSpaceDiscretization.StateSpaceDiscetization(numberOfStates)
#        self.msgId = 0
        self.goalReachedFlag = False
        self.startInGoalStateCounter = 0
        self.tempDriver = None
        self.activeTask = 0
        self.taskTimeOutCounter = 0
        self.avgGoalReachedCounterTask1=0
        self.avgGoalReachedCounterTask2=0
        self.setToStartCounter=0
        self.crossedStatesCounter = 0
        self.crossedStatesbetweenStartAndGoalCounter=0
        self.statesStartToGoal = []
        
    def onexit(self):
        if self.tempDriver:
            self.tempDriver.onShutdown()
#             self.tempDriver.representationOfEnv.probabilityMatrix.displayProbabilityMatrix(1)
#             self.tempDriver.representationOfEnv.probabilityMatrix.displayProbabilityMatrix(3)
#             self.tempDriver.representationOfEnv.probabilityMatrix.displayProbabilityMatrix(5)
#             self.tempDriver.representationOfEnv.probabilityMatrix.displayProbabilityMatrix(1081)
#             self.tempDriver.representationOfEnv.probabilityMatrix.displayProbabilityMatrix(1082)
#             self.tempDriver.representationOfEnv.probabilityMatrix.displayProbabilityMatrix(1096)
#             self.tempDriver.representationOfEnv.probabilityMatrix.displayProbabilityMatrix(1097)
        print "ON EXIT"
     
    def setToStart(self):
        super(JavaEnvironmentEistuete,self).setToStart()
        self.activeTask = 0   
        self.taskTimeOutCounter = 0
        self.setToStartCounter+=1
        self.crossedStatesCounter = 0
        self.statesStartToGoal = []
        
        # Function should be in Representaion of Environment
    def Update(self):
        
        plt.ion()
        #fig, ax1 = plt.subplots()
        fig= plt.figure()
        ax1 = fig.add_subplot(111)
        ax2=ax1.twinx()
        plt.draw()
        
        exiting = False
        
        myEnvironment = self #JavaSomEnvironment()
        
        # tasks
        lowLevelTasks = []
        for t in range(NUMBER_OF_ACTIONS_HL):
            #environmRepMyAgent1 = RepresentationEnvironment.RepresentationEnvironment_ContinuousMsgFromJavaServer(NUMBER_OF_ACTIONS, DIMENSION, MsgParser.MessageParserJavaEnv(), number_of_states=2048)
            environmRepMyAgent1 = RepresentationEnvironment.RepresentationEnvironment_ContinuousMsgFromJavaServer(NUMBER_OF_ACTIONS, DIMENSION, MsgParser.MessageParserJavaEnv(), number_of_states = levels)
            environmRepMyAgent1.setEnvironment(myEnvironment)
            agent = Agent.MainAgent(environmRepMyAgent1) 
            agent.mySimpleAgent.goalState =[NUMBER_OF_STATES-1]
            lowLevelTasks.append(agent)
            
        
        activeTask = lowLevelTasks[0]
        
        assert activeTask.representationOfEnv._stateSpaceDiscetization.getNode(NUMBER_OF_STATES-1) is None, "Terminal state must not be present in kd-tree"
        assert activeTask.representationOfEnv._stateSpaceDiscetization.getNode(NUMBER_OF_STATES-2).label == NUMBER_OF_STATES-2, "Terminal state must not be present in kd-tree"
        assert activeTask.representationOfEnv._stateSpaceDiscetization.getNode(0).label == 0, "0 has to be valid state in kd-treee"
        
        
        environmRepMyAgentHL = RepresentationEnvironment.RepresentationEnvironment_ContinuousMsgFromJavaServer(NUMBER_OF_ACTIONS_HL, DIMENSION_HL, MsgParser2D.MessageParserJavaEnv(), number_of_states =levels_HL)
        environmRepMyAgentHL.setEnvironment(myEnvironment)
        HighLevelTask = Agent.MainAgent(environmRepMyAgentHL)
        HighLevelTask.mySimpleAgent.goalState =[GOAL_STATE_HL]
        HighLevelTask.representationOfEnv._stateSpaceDiscetization.update2DPlot(path_savefig="hl_kdtree-discetization_") 
        
        
        adaptEnvironment = AdaptEnvironment.AdaptEnvironment(environmRepMyAgent1, activeTask.mySimpleAgent.rl, MsgParser.Dimension)
                                           
        #driver.mySimpleAgent.goalState =[2415, 2416, 2417, 2418 , 2419 , 2420, 2421, 2422 ,2423 ,2424 ,2425 ,2426 ,2427 ,2428 ,2429] 
        #draw nodes
#         nodes = driver.representationOfEnv.stateSpaceDiscetization.getNodePositions()
#         graph = DisplayNodePositionsAndV.Scatterplot4D(nodes)    
        
 
        self.deleteLogFiles(['i.txt', 'deltaV.txt', 'StepsVsGoal_Task1.txt', 'StepsVsGoal_Task2.txt'])

        myEnvironment.connect()
        myEnvironment.Send("RESTAR")
        myEnvironment.TryReceive()
        myEnvironment.setToStart()

        executedActionCounter = 0
        task1_goalReached = 0
        task1_activateCounter = 0
        hl_goal_reached_counter = 0
        
        measureTimeCounter = 0
        startTime = datetime.datetime.now()
        
        NoOfloglines=1000000
        #data = numpy.zeros((NoOfloglines,5))
        data = []
        
        actionHistogram = numpy.zeros(NUMBER_OF_ACTIONS)
        ratioSetToStartVsGoalReached1 = 0 
        
        #currentDateAndTime = str(datetime.datetime.now()).replace(".", ":") #plt.savefig interprets . as file extension
        #plt.savefig("statediscretization_" + currentDateAndTime)
        
        
        for task in lowLevelTasks:            
            task.representationOfEnv._stateSpaceDiscetization.update2DPlot()
            task.representationOfEnv._stateSpaceDiscetization.update2DPlot(path_savefig="kdtree-discetization_")
            
        HighLevelTask.representationOfEnv._stateSpaceDiscetization.update2DPlot()
        
        while True:
            print "------------ Java Environment --------------------------------"
            measureTimeCounter+=1
            msg_in = self.TryReceive()
            
            #assert self.msgId == self.packageID, "Messages out of sync: %r != %r " % (self.msgId, self.packageID)  
#             driver0.representationOfEnv.update(msg_in)
            print "msg_in: ", msg_in
            
            # Update high level task
            HighLevelTask.representationOfEnv.update(msg_in)
            
            #High level task chooses new action or continues current action
            [state_hl,action_hl,actionId_hl] = HighLevelTask.Update(msg_in)
            if state_hl == "goalreached":
                #reward higher level
                print "HL Goal Reached"
                hl_goal_reached_counter+=1
                activeTask.representationOfEnv.rewardTask()
                plt.figure(fig.number)
                ax1.plot(executedActionCounter, hl_goal_reached_counter, 'ro')
                #ax1.plot(executedActionCounter, self.crossedStatesbetweenStartAndGoalCounter, 'bo')
                ax2.plot(executedActionCounter, HighLevelTask.mySimpleAgent.probRandomState,'r+')
#                print "activeTask.mySimpleAgent.rl.getVariance()", activeTask.mySimpleAgent.rl.getVariance()
#                ax2.plot([executedActionCounter, executedActionCounter, executedActionCounter], activeTask.mySimpleAgent.rl.getVariance(),'b+')
                #ax2.plot(executedActionCounter, activeTask.representationOfEnv.probRandomState,'r*')
                #ax2.plot(executedActionCounter, ratioSetToStartVsGoalReached1,'r*')
                plt.draw()
                currentDateAndTime = str(datetime.datetime.now()).replace(".", ":") #plt.path_savefig interprets . as file extension
                plt.savefig("hl_goal_reached_" + currentDateAndTime)
                
                myEnvironment.setToStart()
                time.sleep(0.5)
                continue
            
            elif actionId_hl is not None:
                activeTask = lowLevelTasks[actionId_hl]

            #activeTask.representationOfEnv.update(msg_in, goalLocations[0])
            activeTask.representationOfEnv.update(msg_in)
            
            if  activeTask.representationOfEnv.nextStateReached():
                self.statesStartToGoal.append(activeTask.representationOfEnv.getCurrentState())
#                adaptEnvironment.Update()
                self.crossedStatesCounter+=1
            
            [state,action,actionId] = activeTask.Update(msg_in)
            
#             if  activeTask.representationOfEnv.nextStateReached() and activeTask.mySimpleAgent.probRandomState > 0.5:
#                 adaptEnvironment.Update()           
            
            self.taskTimeOutCounter+=1
            task1_activateCounter+=1    
            
            if self.taskTimeOutCounter > ACTION_TIMEOUT_COUNTER:
                print "activeTask timed out"
                activeTask.reset()
                myEnvironment.setToStart()
            
            elif state == "crashed":
                activeTask.reset()
                myEnvironment.setToStart()
                
#             elif state == "rewarded":
#                 numberLineCrossed+=1
#                 deltaTicks = driver.representationOfEnv.environmentState.carState.getTicks()- prevEnvironmentTicks
#                 ax1.plot(numberLineCrossed, deltaTicks, 'o')
#                 ax2.plot(numberLineCrossed, driver.mySimpleAgent.probRandomState,'+')
#                 plt.draw()
#                 prevEnvironmentTicks=driver.representationOfEnv.environmentState.carState.getTicks()
#                 myEnvironment.setToStart()

            elif state == "goalreached":
                print "JavaEnvironmentEistuete: goalreached"
                task1_goalReached+=1
                self.avgGoalReachedCounterTask1+=1
                
                print "States crossed: ",self.crossedStatesCounter
#                data[executedActionCounter][4]= self.crossedStatesCounter 
                self.crossedStatesbetweenStartAndGoalCounter = self.crossedStatesCounter 

#                 data[executedActionCounter][0]= task1_goalReached
#                 data[executedActionCounter][2]= activeTask.mySimpleAgent.probRandomState
                self.statesStartToGoal.append(activeTask.representationOfEnv.getCurrentState())
                print "self.statesStartToGoal: ", self.statesStartToGoal
                
                data.append([task1_goalReached,0, activeTask.mySimpleAgent.probRandomState,0,self.crossedStatesCounter, self.statesStartToGoal])
                myEnvironment.getCurrentPos()
#                myEnvironment.setToStart() 
                
                # Do not reset, send something
                #self.Send("CURPOS")
            
#             elif state == "CROSSED_GOAL_WRONG_DIRECTION":
#                 print "CROSSED_GOAL_WRONG_DIRECTION"
#                 myEnvironment.setToStart()
                
            elif state == "action":
                executedActionCounter+=1
                activeTask.representationOfEnv.t+=1

                self.Send(action)
                
            print "Updated driver"
               
            
            # this if seems to be the end 
            if (activeTask.mySimpleAgent.probRandomState <= activeTask.mySimpleAgent.minRandomState) or (executedActionCounter == (NoOfloglines-1)):
                print "actionHistogram: ", actionHistogram
                currentDateAndTime = str(datetime.datetime.now()).replace(".", ":") #plt.savefig interprets . as file extension
                plt.savefig("steps2goal_" + currentDateAndTime)
                #numpy.save(open("data_" + currentDateAndTime + ".pkl", "wb" ), data)
                pickle.dump(data, open("data_" + currentDateAndTime + ".pkl", "wb" ))
                path = "../../../../../LogFiles/ExtendedTransitionMatrices/matrix"
                activeTask.representationOfEnv.probabilityMatrix.dumpToFile(path)
                activeTask.mySimpleAgent.rl.save("rl")
                #driver.representationOfEnv.generateGraphvicFile(driver.mySimpleAgent.rl, "")
#                 self.saveVvalues()
#                 self.representationOfEnv._stateSpaceDiscetization.saveNodes("states")   
                exiting = True
            
#             if measureTimeCounter == 100000:
#                 fileplt=plt,name = "deltaTime_100000runs_" + str(datetime.datetime.now()).replace(".", ":") + ".txt"
#                 deltaTime =  datetime.datetime.now() - startTime
#                 timeFile = open(filename, "w")
#                 text = "measureTimeCounter: " + str(measureTimeCounter) + "\n" + "deltaTime: "+ str(deltaTime) 
#                 timeFile.write(text)
#                 timeFile.close()
                
            if self.setToStartCounter == 500 or exiting:
                print "Updating plots"
                ratioSetToStartVsGoalReached1 = float(self.avgGoalReachedCounterTask1)/float(self.setToStartCounter)
                self.avgGoalReachedCounterTask1=0
                self.setToStartCounter = 0
                
#                 plt.figure(fig.number)
#                 ax1.plot(executedActionCounter, task1_goalReached, 'ro')
#                 #ax1.plot(executedActionCounter, self.crossedStatesbetweenStartAndGoalCounter, 'bo')
#                 ax2.plot(executedActionCounter, activeTask.mySimpleAgent.probRandomState,'r+')
#                 print "activeTask.mySimpleAgent.rl.getVariance()", activeTask.mySimpleAgent.rl.getVariance()
#                 ax2.plot([executedActionCounter, executedActionCounter, executedActionCounter], activeTask.mySimpleAgent.rl.getVariance(),'b+')
#                 #ax2.plot(executedActionCounter, activeTask.representationOfEnv.probRandomState,'r*')
#                 #ax2.plot(executedActionCounter, ratioSetToStartVsGoalReached1,'r*')
#                 plt.draw()
#                 currentDateAndTime = str(datetime.datetime.now()).replace(".", ":") #plt.path_savefig interprets . as file extension
#                 plt.savefig("goal_reached_" + currentDateAndTime)
                
                for task in lowLevelTasks:
 #                   task.representationOfEnv._stateSpaceDiscetization.update2DPlot(path_savefig="kdtree-discetization_")                      
                    task.representationOfEnv._stateSpaceDiscetization.plotQ2D(Values=task.mySimpleAgent.rl.getQValues(), plot="Q", path_savefig="q-values_")                
                   
                HighLevelTask.representationOfEnv._stateSpaceDiscetization.plotQ2D(Values=HighLevelTask.mySimpleAgent.rl.getQValues(), plot="Q", path_savefig="hl_q-values_")                
                
                if exiting:
                    #kdtree.plotV2D(activeTask.representationOfEnv._stateSpaceDiscetization.tree, V=activeTask.mySimpleAgent.rl.getVStates(), path_savefig="v-values_")
                    #kdtree.plotV2D(activeTask.representationOfEnv._stateSpaceDiscetization.tree, V=numpy.random.rand(len(activeTask.mySimpleAgent.rl.getVStates()),1)*20.0, path_savefig="v-values_")                    
                    break
        
    def run(self):
        self.Update()
         
    
def start3D():
    myclient = JavaEnvironmentEistuete(NUMBER_OF_STATES)
    atexit.register(myclient.onexit)
    myclient.run()    
    
        
def start2D():
#     myclient = JavaEnvironmentEistuete()
#     myclient.mystart()
    
    #app = PyQt4.QtGui.QApplication(sys.argv)
    myclient = JavaEnvironmentEistuete(NUMBER_OF_STATES)
    atexit.register(myclient.onexit)
    #gui= Gui2D.PlottingDataMonitor2D()
    #form = Gui.Form(myclient, gui)
    #form.show()
    #myclient.start()
    myclient.run()
    
    #sys.exit(app.exec_())
          
if __name__ == '__main__':
    #start2D()
    cProfile.run("start2D()",  'myrestats')                       

            
