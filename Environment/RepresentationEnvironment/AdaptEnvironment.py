import numpy
import Environment.RepresentationEnvironment.SOM.MyGrowingNeuralGasNode as MyGrowingNeuralGasNode
import csv
import Environment.RepresentationEnvironment.StateInformation as StateInformation

MaxNumberSoms = 1000
MinActionExec = 200

class AdaptEnvironment():
    def __init__(self, agent=None, dimensionLaser=None):
        self._splitted = False
        self.representationEnvironment = agent.mySimpleAgent.representationOfEnvironment
        self._rl = agent.mySimpleAgent.rl
        self.prevLaser = None
        self.prevState = None
        self.prevPrevLaser = None
        self.prevPrevPrevLaser = None
        # self._probabilityMatrix = representationEnvironment._probabilityMatrix

        # numberOfSoms = self.representationEnvironment.numberOfStates * self.representationEnvironment.getNumberOfActions()
        numberOfSoms = MaxNumberSoms * self.representationEnvironment.getNumberOfActions()

        self.gng = []
        for i in range(numberOfSoms):
            self.gng.append(MyGrowingNeuralGasNode.MyGrowingNeuralGasNode(start_poss=numpy.array([[0.0], [0.1]]), eps_n=0.01, max_nodes=2))

        # print "self.gng: i:",i
        csv_logfile = open('logfile_som_position.csv', 'wb')
        self.csv_writer = csv.writer(csv_logfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.csv_writer.writerow(['State', 'Action', 'index', 'Pos0', 'Pos1', 'Distance', 'q'])

        self.stateInformation = []
        for i in range(numberOfSoms):
            self.stateInformation.append(StateInformation.StateInformation(self._rl, dimensionLaser))

    @property
    def splitted(self):
        return self._splitted

    def Update(self, previousSensorData, prevAction):
        self._splitted = False
        # self._Refine(currentState)
        # self._RefineDeltaV(currentState)
        #        self._RefineDeltaQ(currentState)
        self._VariableSplit(previousSensorData, prevAction)

    def _trainSom(self, state, action, sensorData):
        if self._rl.updateQ is None:
            return 0.0
        assert state < MaxNumberSoms, "More states than SOMs"
        index = state + MaxNumberSoms * action
        q = numpy.array([[self._rl.updateQ]])
        self.gng[index].train(q)

        (n0, n1), (dist0, dist1) = self.gng[index]._get_nearest_nodes(sensorData)
        assert dist0 <= dist1, "Assumption was wrong!! dist0 > dist1"

        print "node position: "
        print [node.data.pos for node in self.gng[index].graph.nodes]

        somDistance = abs(self.gng[index].graph.nodes[0].data.pos - self.gng[index].graph.nodes[1].data.pos)
        print "distance: ", somDistance
        self.csv_writer.writerow([state, action, index, float(self.gng[index].graph.nodes[0].data.pos),
                                  float(self.gng[index].graph.nodes[1].data.pos), float(somDistance), float(q)])
        return n0, somDistance


    def _VariableSplit(self, previousSensorData, prevAction):
        """
        The server does not execute an action if it leads to a crash. Thus laser readings before the action the will lead
        to a crash and after it are the same.
        """
        currentLaser = self.representationEnvironment.messageParser.getSensorData()
        previousState = self.representationEnvironment.getPreviousState()
        currentState = self.representationEnvironment.getCurrentState()

        if previousState is None:
            return
        if currentState is None:
            return
        if prevAction is None:
            return

        self.prevLaser = previousSensorData

        if self.prevLaser is not None:
            actionExecuted = self.stateInformation[previousState].actionCount(prevAction)
            actionReliable = (actionExecuted > MinActionExec)

            # if self.prevState != currentState and actionReliable and (self._rl.Q_variance[currentState]>0.2).any():
            node, somDistance = self._trainSom(previousState, prevAction, previousSensorData)

            self.stateInformation[previousState].Update(prevAction, node.data.label, previousSensorData)
            print "prev state: ", previousState, "    actionExecuted: ", actionExecuted, "      somDistance: ", somDistance
            if (somDistance > 0.6) and actionReliable:
#                print "prev state: ", previousState, "    actionExecuted: ", actionExecuted, "      somDistance: ", somDistance
                avg,  split_axis = self.stateInformation[previousState].getSplitPointAndAxis(prevAction)
                # n = self.representationEnvironment.stateSpaceDiscetization.getNode(currentState).split2(self.prevLaser, axis=split_axis, sel_axis = (lambda axis: axis))\
                n = self.representationEnvironment.stateSpaceDiscetization.split(avg, axis=split_axis, sel_axis=(lambda axis: axis))
                print "_VariableSplit 1: split_axis: ", split_axis
                self._rl.setQvalues(n.left.label, self._rl.getQvalues(previousState))
                self._rl.setQvalues(n.right.label, self._rl.getQvalues(previousState))
                self._splitted = True
            #                assert False, "DEBUG: SOM SPLIT"

            #             if self.prevState == currentState and self.representationEnvironment.reward:
            #                 deltaLaser = abs(currentLaser-self.prevPrevLaser)
            #                 split_axis = numpy.argmax(deltaLaser)
            #                 print "_VariableSplit 2: split_axis: currentLaser: ", currentLaser, "     self.prevPrevLaser:", self.prevPrevLaser, "   split_axis: ", split_axis
            #
            #                 # leaf does not have data, [-1] is leaf, [-2] is node before leaf
            #                 n = self.representationEnvironment.stateSpaceDiscetization.getPathToLeaf(currentLaser)[-2]
            # #               print "n: ", n
            #
            #                 if abs(n.data[split_axis] - self.prevPrevLaser[split_axis]) > 0.05:
            #                     #n.split2(self.prevPrevLaser, axis=split_axis, sel_axis = (lambda axis: axis))
            #                     n = self.representationEnvironment.stateSpaceDiscetization.split(self.prevPrevLaser, axis=split_axis, sel_axis = (lambda axis: axis))
            #                     print "_VariableSplit 2: split_axis: ", split_axis, "  n.left.label= ",n.left.label," = ", self._rl.getQvalues(currentState), "     n.right.label: ", n.right.label, " = ", self._rl.getQvalues(currentState)
            #                     self._rl.setQvalues(n.left.label, self._rl.getQvalues(currentState))
            #                     self._rl.setQvalues(n.right.label, self._rl.getQvalues(currentState))
            #                     self._splitted = True
            # self.prevPrevLaser = self.prevLaser
            # self.prevLaser = currentLaser

    def _RefineDeltaQ(self, currentState):
        '''Split based on delta V.
            Check Reliability!!!! '''
        assert self._rl is not None, "AdaptEnvironment: No RL module given"
        MinActionExec = 100
        actionReliable = (self._rl.Q_reliable[currentState] > MinActionExec).all()

        if actionReliable and (self._rl.Q_variance[currentState] > 0.2).any():
            leftState, rightState = self.representationEnvironment.stateSpaceDiscetization.getNode(currentState).split()
            self._rl.setQvalues(leftState, self._rl.getQvalues(currentState))
            self._rl.setQvalues(rightState, self._rl.getQvalues(currentState))

            self._splitted = True
            print "splitted current state: ", currentState

    def _Refine(self, currentState):
        ''' Split state based on assumption that every state should have an action with a probability greater than 0.95'''
        ''' Check Reliability!!!! '''
        for a in range(0, self.representationEnvironment._numberOfActions):
            print "self._probabilityMatrix[int(currentState)].getRowprobabilityMatrix(a): ", self._probabilityMatrix[
                int(currentState)].getRowprobabilityMatrix(a)
            if self._probabilityMatrix[int(currentState)].isReliable(a):
                if not (self._probabilityMatrix[int(currentState)].getRowprobabilityMatrix(a) >= 0.95).any():
                    self.leftState, self.rightState = self.representationEnvironment.stateSpaceDiscetization.getNode(
                        currentState).split()
                    self._splitted = True
                    print "splitted current state: ", currentState
                    # currentState = self._stateSpaceDiscetization.getState(self.messageParser.getSensorData())

    def _RefineDeltaV(self, currentState):
        '''Split based on delta V.
            Check Reliability!!!! '''
        assert self._rl is not None, "AdaptEnvironment: No RL module given"
        MinActionExec = 100
        actionReliable = [self._probabilityMatrix[currentState].isReliable(a, MinActionExec) for a in
                          range(0, self.representationEnvironment._numberOfActions)]

        if sum(actionReliable) == self.representationEnvironment._numberOfActions:
            if self._rl.getDeltaV(currentState) > 0.2:
                leftState, rightState = self.representationEnvironment.stateSpaceDiscetization.getNode(
                    currentState).split()
                self._rl.setV(leftState, self._rl.getV(currentState))
                self._rl.setV(rightState, self._rl.getV(currentState))

                self._splitted = True
                print "splitted current state: ", currentState

# if not (self._probabilityMatrix[int(currentState)].getRowprobabilityMatrix(a) >= 0.95).any():
#                 self.leftState, self.rightState = self.representationEnvironment.stateSpaceDiscetization.getNode(currentState).split()
#                 self._splitted = True
#                 print "splitted current state: ", currentState
#                 #currentState = self._stateSpaceDiscetization.getState(self.messageParser.getSensorData())
