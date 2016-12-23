'''
Created on Nov 28, 2012

@author: mrfish

Uses: Java Eistuete mit Dreirad. Es werden alle drei Koordinaten in einen State uebersetzt.
Ohne SOM.


Workarounds/Hacks:
The server does not execute an action if it leads to a crash. Thus laser readings before the action the will lead to a crash and after
it are the same. Effects _VariableSplit.

'''
from PyQt4 import QtCore
import atexit
import datetime
import numpy
import time

import Agent.JavaMainAgent as Agent
import Environment.IEnvironment
import Environment.RealEnvironment.JavaSomEnvironment as JavaEnvironment
import Environment.RepresentationEnvironment.RepresentationEnvironment_ContinuousMsgFromJavaServer as RepresentationEnvironment 
import Environment.RepresentationEnvironment.SOM.Gui as Gui
import Environment.RepresentationEnvironment.SOM.Gui2D as Gui2D
#import Misc.MessageParserJavaEnvLaser2D as MsgParser
import Misc.MessageParserJavaEnvLaser5D as MsgParser

import Environment.RepresentationEnvironment.AdaptEnvironment as AdaptEnvironment

import PyQt4.Qwt5 as Qwt
import matplotlib.pyplot as plt
import pickle
import dill # extends pickle

import cProfile
import sys

#import Agent.MainAgent as Agent
#import Misc.MessageParserJavaEnvLaser4D as MsgParser
#import mayavi.mlab
#sys.stdout = open('output_environment.txt', 'w')
#NUMBER_OF_ACTIONS = 4 * 2       #n,s,e,w and 2 speeds
NUMBER_OF_ACTIONS = 4        #n,s,e,w


#NUMBER_OF_SIMPLE_ACTIONS = 4
#SIZEofSTATE = 20
#SIZExy = 200
#STATESORIENTATION = 10
#NUMBEROFSTATESONEDIRECTION = SIZExy/SIZEofSTATE
#NUMBER_OF_STATES_JAVA_WORLD = SIZEofSTATE * SIZEofSTATE * STATESORIENTATION
#UPDATEDRAWINGSTEPS = 7
#NUMBER_OF_STATES = NUMBER_OF_STATES_JAVA_WORLD

#DIMENSION = MsgParser.Dimension


FileNameRL_Opponent = "rl_opponent"
FileNameStateSpaceRep_Opponent = "StateSpaceRep_opponent"
FileNameTaskGoalStates_Opponent = "Task_goalStates_opponent"

FileNameRL_RaceTrack = "rl_racetrack"
FileNameStateSpaceRep_RaceTrack = "StateSpaceRep_racetrack"
FileNameTaskGoalStates_RaceTrack = "Task_goalStates_racetrack"

if True:
    FileNameRL = FileNameRL_Opponent
    FileNameStateSpaceRep = FileNameStateSpaceRep_Opponent
    FileNameTaskGoalStates = FileNameTaskGoalStates_Opponent
else:
    FileNameRL = FileNameRL_RaceTrack
    FileNameStateSpaceRep = FileNameStateSpaceRep_RaceTrack
    FileNameTaskGoalStates = FileNameTaskGoalStates_RaceTrack
    
#ACTION_TIMEOUT_COUNTER = 5000
#NUMBER_OF_STATES_HL = 2**(levels_HL+1)    # actually -1, removed for extra state i.e. terminal state


#Actually the number of states in the kd-tree is  2**(levels+1)-1
# but we want an extra state

#levels = 7
levels = 2

NumberOfStates = 10000
PositiveTerminalState = NumberOfStates + 1   # index 10000
NegativeTerminalState = NumberOfStates + 2   # index 10001
MaxNumberQStates = NegativeTerminalState

# levels = 6
# NUMBER_OF_STATES = 2**(levels+1+1)    # actually -1, removed for extra state i.e. terminal state
# MaxNumberQStates = NUMBER_OF_STATES + 1 + 1

FileNameProbMatrices = "Probab1l1tyMatr1x3D"

class JavaEnvironmentEistuete(JavaEnvironment.JavaSomEnvironment, QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)
        JavaEnvironment.JavaSomEnvironment.__init__(self)
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
        self.previousSensorData = None
        
        # Function should be in Representaion of Environment
    def Update(self):
        self.previousSensorData = None
        self.previousActionId = None
        showSomInStates=[3, 4, 10, 11]
        
        plt.ion()
        #fig, ax1 = plt.subplots()
        fig= plt.figure(1)
        fig3 = plt.figure(3)
        ax3 = fig3.add_subplot(len(showSomInStates),1, 1)
        ax1 = fig.add_subplot(111)
        ax_variance = fig.add_subplot(111)
        ax2 = ax1.twinx()
#        plt.figure(1)
#        ax1.plot(1, 5, "or")
#        ax2.plot(  1, 0.5,"+b")
        plt.draw()
        
        exiting = False
        
        myEnvironment = self #JavaSomEnvironment()
        
        myMessageParser = MsgParser.MessageParserJavaEnv()
        myMessageParser.setSensorType(MsgParser.OpponentSensor)
#        myMessageParser.setSensorType(MsgParser.DistanceSensor)
        
        #environmRepMyAgent1 = RepresentationEnvironment.RepresentationEnvironment_ContinuousMsgFromJavaServer(NUMBER_OF_ACTIONS, DIMENSION, MsgParser.MessageParserJavaEnv(), number_of_states=2048)
        environmRepMyAgent1 = RepresentationEnvironment.RepresentationEnvironment_ContinuousMsgFromJavaServer(NUMBER_OF_ACTIONS, myMessageParser.Dimension, myMessageParser, levels = MaxNumberQStates)
        environmRepMyAgent1.stateSpaceDiscetization.createRepresentation(myMessageParser.Dimension, levels )
#        environmRepMyAgent1.stateSpaceDiscetization.saveRepresentationTofile(FileNameStateSpaceRep)
#        environmRepMyAgent1.stateSpaceDiscetization.createRepresentationFromFile(FileNameStateSpaceRep)
        
        environmRepMyAgent1.setEnvironment(myEnvironment)
        agent = Agent.MainAgent(environmRepMyAgent1)
        #agent.mySimpleAgent.createRL(environmRepMyAgent1.getNumberOfStates(), environmRepMyAgent1.getNumberOfActions())
        agent.mySimpleAgent.createRL(MaxNumberQStates, environmRepMyAgent1.getNumberOfActions())
#        agent.mySimpleAgent.dumpRL(FileNameRL)
#        agent.mySimpleAgent.createRLFromFile(FileNameRL)

        agent.mySimpleAgent.goalState = [MaxNumberQStates -1, MaxNumberQStates-2]
        
        #HighLevelTask.representationOfEnv._stateSpaceDiscetization.update2DPlot(path_savefig="hl_kdtree-discetization_") 
        
        #adaptEnvironment = AdaptEnvironment.AdaptEnvironment(environmRepMyAgent1, agent.mySimpleAgent.rl)
        adaptEnvironment = AdaptEnvironment.AdaptEnvironment(agent, MsgParser.Dimension_OpponentSensor)
                                           
        self.deleteLogFiles(['i.txt', 'deltaV.txt', 'StepsVsGoal_Task1.txt', 'StepsVsGoal_Task2.txt'])

        myEnvironment.connect()
        myEnvironment.Send("RESTAR")
        myEnvironment.TryReceive()
        myEnvironment.setToStart()

        executedActionCounter = 0
        task1_goalReached = 0
        task1_activateCounter = 0
        
        measureTimeCounter = 0
        startTime = datetime.datetime.now()
        
        NoOfloglines=1000000
        #data = numpy.zeros((NoOfloglines,5))
#        data = []
        
        visitedStates = {}
        actionHistogram = numpy.zeros(NUMBER_OF_ACTIONS)
        
            
#        agent.representationOfEnv._stateSpaceDiscetization.update2DPlot()
#        agent.representationOfEnv._stateSpaceDiscetization.update2DPlot(path_savefig="kdtree-discetization_")

            
        activeTask = agent
        split_counter = 0        
        
        while True:
            print "------------ Java Environment --------------------------------"
            measureTimeCounter+=1
            msg_in = self.TryReceive()
            
            #assert self.msgId == self.packageID, "Messages out of sync: %r != %r " % (self.msgId, self.packageID)  
#             driver0.representationOfEnv.update(msg_in)
            print "msg_in: ", msg_in


            #activeTask.representationOfEnv.update(msg_in, goalLocations[0])
            activeTask.representationOfEnv.update(msg_in)            
            currentState = int(activeTask.representationOfEnv.getCurrentState())
            for a in range(NUMBER_OF_ACTIONS):
                visitedStates[str(currentState)+"-"+ str(a)]=activeTask.mySimpleAgent.rl.getDeltaNormalized(currentState,a)
            print visitedStates
            
#            adaptEnvironment.Update()
            split_counter += adaptEnvironment.splitted
            
            [state,action,actionId] = activeTask.Update(msg_in)

            # Why do I need the explicite check if state == "goalreached"??? nextStateReached() seems to set to false somewhere
            if (activeTask.representationOfEnv.nextStateReached() or state == "goalreached" or state == "crashed") and activeTask.mySimpleAgent.probRandomState > 0.4:
                adaptEnvironment.Update(self.previousSensorData, self.previousActionId) #moved here

            self.previousSensorData = activeTask.representationOfEnv.messageParser.getSensorData()
            
            self.taskTimeOutCounter+=1
            task1_activateCounter+=1
            
            if state == "crashed":
                activeTask.reset()
                myEnvironment.setToStart()

            elif state == "goalreached":               
                task1_goalReached+=1
                self.avgGoalReachedCounterTask1+=1
                
                print "JavaEnvironmentEistuete: goalreached, task1_goalReached: ", task1_goalReached, "     executedActionCounter: ", executedActionCounter
                
                print "States crossed: ",self.crossedStatesCounter
                self.crossedStatesbetweenStartAndGoalCounter = self.crossedStatesCounter 
                self.statesStartToGoal.append(activeTask.representationOfEnv.getCurrentState())
                print "self.statesStartToGoal: ", self.statesStartToGoal
#                 plt.figure(1)
#                 ax1.plot(executedActionCounter, task1_goalReached, "or")
#                 ax2.plot(executedActionCounter, activeTask.mySimpleAgent.probRandomState,"+b")

#                 currentDateAndTime = str(datetime.datetime.now()).replace(".", ":") #plt.path_savefig interprets . as file extension
#                 plt.savefig("goal_reached_" + currentDateAndTime)
                activeTask.reset()
                myEnvironment.setToStart()
#                time.sleep(0.5)
#                assert False, "REMOVE ONLY FOR DEBUGGING !!"
                #DEDUG
                continue
                
#                 data.append([task1_goalReached,0, activeTask.mySimpleAgent.probRandomState,0,self.crossedStatesCounter, self.statesStartToGoal])
#                 myEnvironment.getCurrentPos()
#                 myEnvironment.setToStart() 
                
            elif state == "action":
                executedActionCounter+=1
                activeTask.representationOfEnv.t+=1
                self.previousActionId = actionId
                self.Send(action)
                
            print "Updated driver"

            if (activeTask.mySimpleAgent.probRandomState <= activeTask.mySimpleAgent.minRandomState): # or (executedActionCounter == (NoOfloglines-1)):
                print "actionHistogram: ", actionHistogram
#                currentDateAndTime = str(datetime.datetime.now()).replace(".", ":") #plt.savefig interprets . as file extension
#                plt.savefig("steps2goal_" + currentDateAndTime)
                #numpy.save(open("data_" + currentDateAndTime + ".pkl", "wb" ), data)
    #            pickle.dump(data, open("data_" + currentDateAndTime + ".pkl", "wb" ))
                path = "../../../../../LogFiles/ExteNUMBER_OF_STATESndedTransitionMatrices/matrix"
#                activeTask.representationOfEnv.probabilityMatrix.dumpToFile(path)
                activeTask.mySimpleAgent.rl.save("rl")
 
                exiting = True
                
            if (executedActionCounter%1000) == 0 or exiting:
                print "Updating plots"
#                ratioSetToStartVsGoalReached1 = float(self.avgGoalReachedCounterTask1)/float(self.setToStartCounter)
                self.avgGoalReachedCounterTask1=0
                self.setToStartCounter = 0

                str_prob = str(activeTask.mySimpleAgent.reduceProbabilityBy).replace(".", "p")   
                str_highest_state_id = str(activeTask.representationOfEnv.stateSpaceDiscetization.highestStateId)           
                currentDateAndTime = str(datetime.datetime.now()).replace(".", ":") + "_" + str_prob +"_"+ str_highest_state_id #plt.path_savefig interprets . as file extension


                plt.figure(1)
                ax1.plot(executedActionCounter, task1_goalReached, "or")
                ax2.plot(executedActionCounter, activeTask.mySimpleAgent.probRandomState,"+b")
                plt.savefig("goal_reached_" + currentDateAndTime)
                
                q_var = []
                plt.figure(2)
                plt.cla()
                my_xticks = visitedStates.keys()
                for k in my_xticks:
                    q_var.append(visitedStates[k])
                plt.xticks(range(len(my_xticks)), my_xticks, rotation=90)
                plt.plot(q_var, "bo")
                [min_var, mean, max_var] = activeTask.mySimpleAgent.rl.getVariance()
                plt.plot([0, len(my_xticks)], [mean, mean])
                plt.draw()
#                currentDateAndTime = str(datetime.datetime.now()).replace(".", ":") #plt.path_savefig interprets . as file extension
                plt.savefig("delta_q_var_" + currentDateAndTime)  
                     
                activeTask.representationOfEnv._stateSpaceDiscetization.plotQ2D(Values = activeTask.mySimpleAgent.rl.getQValues(), plot="Q", path_savefig="q-values_")                
#                currentDateAndTime = str(datetime.datetime.now()).replace(".", ":") #plt.path_savefig interprets . as file extension
#                plt.savefig("hl_goal_reached_" + currentDateAndTime)                   
                environmRepMyAgent1.stateSpaceDiscetization.saveRepresentationTofile(FileNameStateSpaceRep)
                agent.mySimpleAgent.dumpRL(FileNameRL)
                agent.mySimpleAgent.dumpGoalStates(FileNameTaskGoalStates)

                plt.figure(3)
                plt.clf()
                for i,state in enumerate(showSomInStates):
                    plt.subplot(len(showSomInStates), 1, i+1)
                    for a in range(0, NUMBER_OF_ACTIONS):
                        index = state + AdaptEnvironment.MaxNumberSoms * a
                        pos_nodes = numpy.array([node.data.pos for node in  adaptEnvironment.gng[index].graph.nodes])
                        b = numpy.ones(pos_nodes.flatten().shape) * a/10.0
                        plt.plot(pos_nodes, b, linewidth=10)
                    plt.xlabel(str(state))
                    plt.ylabel(str(state))
                #plt.draw()
                plt.figure(3).canvas.draw()
                print "split_counter: ", split_counter

                
                if exiting:
                    #kdtree.plotV2D(activeTask.representationOfEnv._stateSpaceDiscetization.tree, V=activeTask.mySimpleAgent.rl.getVStates(), path_savefig="v-values_")
                    #kdtree.plotV2D(activeTask.representationOfEnv._stateSpaceDiscetization.tree, V=numpy.random.rand(len(activeTask.mySimpleAgent.rl.getVStates()),1)*20.0, path_savefig="v-values_")                    
                    print "exiting"
                    break
        
    def run(self):
        self.Update()
         
    
def start3D():
    myclient = JavaEnvironmentEistuete()
    atexit.register(myclient.onexit)
    myclient.run()    
    
        
def start2D():
#     myclient = JavaEnvironmentEistuete()
#     myclient.mystart()
    
    #app = PyQt4.QtGui.QApplication(sys.argv)
    myclient = JavaEnvironmentEistuete()
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

            
