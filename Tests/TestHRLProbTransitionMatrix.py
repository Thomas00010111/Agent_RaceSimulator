'''
Created on Jan 27, 2013

@author: mrfish
'''

import numpy
import numpy.testing
import unittest

import Environment.RepresentationEnvironment.ProbTransitionMatrix as ProbTransitionMatrix


class TestHRLProbabilityTransitionMatrix(unittest.TestCase):
    
#
    def setUp(self):
        self.NumberOfStates = 5
        self.NumberOfActions = 5
        self.matrix = ProbTransitionMatrix.ProbTransitionMatrix( self.NumberOfActions, self.NumberOfStates)
        self.matrix._probabilityMatrix = numpy.array([[0.1, 0.0,  0.9, 0.0,  0.0 ],
                                            [ 0.0, 0.0,  0.0, 0.0, 0.0 ],
                                            [ 0.2, 0.7,  0.0, 0.1, 0.0 ],
                                            [ 0.0, 0.0,  0.0, 0.0, 0.0 ],
                                            [ 0.0, 0.0,  0.0, 0.0, 0.0 ]], dtype = float)
    
    # test initialization of matrix (not predefined function of the test framework)
    def test_init(self):
        NumberOfActions = 3
        NumberOfStates = 8
        matrix = ProbTransitionMatrix.ProbTransitionMatrix(NumberOfActions, NumberOfStates)
        self.assertEqual(len(matrix._probabilityMatrix), 3)
        self.assertEqual(len(matrix._probabilityMatrix[0]), 8)
        self.assertEqual(matrix._probabilityMatrix.shape, (3,8))
        self.assertEqual(matrix._transitionMatrix.shape, (3,8)) 
        
            
    
    def test_CalcBestAction(self):
        VValues = numpy.array([1.2,  3.7,  1.3, -7.4,  2.3 ])
        bestAction = self.matrix.CalcBestAction(VValues)
        self.assertEqual(bestAction,2)
         
   
    def test_updateProbability(self):
        self.matrix.updateProbability(1, 3)
        self.matrix.updateProbability(1, 3)
        numpy.testing.assert_array_equal(self.matrix._transitionMatrix[1], numpy.array([0,  0,  0, 2,  0 ]))
        numpy.testing.assert_array_equal(self.matrix._probabilityMatrix[1], numpy.array([0.0,  0.0,  0.0, 1.0,  0.0 ]))
        self.assertEqual(self.matrix.getProbability(1, 3), 1)
        
        self.matrix.updateProbability(1, 2)
        self.matrix.updateProbability(1, 2)                                                                                
        numpy.testing.assert_array_equal(self.matrix._transitionMatrix[1], numpy.array([0,  0,  2, 2,  0 ]))
        numpy.testing.assert_array_equal(self.matrix._probabilityMatrix[1], numpy.array([0.0,  0.0,  0.5, 0.5,  0.0 ]))
        self.assertEqual(self.matrix.getProbability(1, 2), 0.5)
        
        
    def test_getProbability(self):
        self.matrix.updateProbability(1, 3)
        self.matrix.updateProbability(1, 3)
        self.assertEqual(self.matrix.getProbability(1, 3), 1)
        
        self.matrix.updateProbability(1, 2)
        self.matrix.updateProbability(1, 2)                                                                                
        self.assertEqual(self.matrix.getProbability(1, 2), 0.5)


    def test_getSumActionCalled(self):
        self.matrix.updateProbability(1, 2)
        self.matrix.updateProbability(1, 3)
        self.matrix.updateProbability(1, 4)
        self.matrix.updateProbability(3, 4)
        self.assertEqual(self.matrix.getSumActionCalled(1),3)
        self.assertEqual(self.matrix.getSumActionCalled(3),1)
        
    def test_getActionsToReachState(self):
        self.matrix.reset()
        targetState = 2
        otherState = 1
        self.matrix.updateProbability(1, targetState)
        self.matrix.updateProbability(1, otherState)
        self.matrix.updateProbability(2, targetState)
        result = self.matrix.getActionsToReachState(targetState)
        self.assertEqual(result, [[0,0.0], [1,0.5], [2,1.0], [3,0.0], [4,0.0]])
        
    def test_getReachableStates(self):
        self.matrix.reset()
        targetState = 2
        otherState = 1
        self.matrix.updateProbability(1, targetState)
        self.matrix.updateProbability(1, otherState)
        self.matrix.updateProbability(2, targetState)
        self.matrix.updateProbability(2, targetState)
        result = self.matrix.getReachableStates()
        #state 0 is reached using action 0 with a probability of 0.0 ...
        #which actually means state 0 is not reachable
        self.assertEqual(result, [[0,[0,0.0]], [1,[1,0.5]], [2,[2,1.0]], [3,[0,0.0]], [4,[0,0.0]]])
        
    def test_getRowprobabilityMatrix(self):
        ''' gets the probability of reaching states''' 
        action = 2
        self.assertEqual( (self.matrix._probabilityMatrix[action] > 0.6).any(), True)
        numpy.testing.assert_array_equal(self.matrix.getRowprobabilityMatrix(action), self.matrix._probabilityMatrix[action]) 
        
        
    def test_reset(self):     
        self.matrix.reset()
        zeroMatrix = numpy.zeros(shape=(self.NumberOfActions,self.NumberOfStates))
        numpy.testing.assert_array_equal(self.matrix._transitionMatrix, zeroMatrix)
        
        
    if __name__ == '__main__':
        unittest.main()