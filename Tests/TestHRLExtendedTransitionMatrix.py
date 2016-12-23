'''
Created on Jan 27, 2013

@author: mrfish
'''

import numpy.testing
import unittest

import Environment.RepresentationEnvironment.ExtendedDiscreteTransitionMatrix as ExtendedDiscreteTransitionMatrix


class TestHRLExtendedTransitionMatrix(unittest.TestCase):
    
#
    def setUp(self):
        self.NumberOfActions = 3
        self.NumberOfStates = 5
        self.matrix = ExtendedDiscreteTransitionMatrix.ExtendedDiscreteTransitionMatrix( self.NumberOfActions, self.NumberOfStates)

    def test_inti(self):
        self.assertEqual(len(self.matrix.transitionMatrices),  self.NumberOfStates)  
     
    def test_CalcBestAction(self):
        currentState = 2
        self.VValues = numpy.array([1.2,  3.7,  1.3, -7.4,  2.3 ])
        self.matrix[currentState].CalcBestAction(self.VValues)
        #??????????????????????? hier fehlt was
   
    def test_reset(self):
        [tm._probabilityMatrix.fill(1.23) for tm in self.matrix.transitionMatrices]
        [tm._transitionMatrix.fill(1.23) for tm in self.matrix.transitionMatrices]
        self.matrix.reset()
        zeroMatrix = numpy.zeros(shape=(self.NumberOfActions,self.NumberOfStates))
        [numpy.testing.assert_array_equal(tm._probabilityMatrix, zeroMatrix) for tm in self.matrix.transitionMatrices]
        [numpy.testing.assert_array_equal(tm._transitionMatrix, zeroMatrix) for tm in self.matrix.transitionMatrices]
   
    
#    def test_drawStateDiagram(self):
#        self.matrix.drawStateDiagram()   

    def test_dumpToFile(self):
        matrixName = "testExtendedTransitionMatrix"
        self.matrix.dumpToFile(matrixName)
        self.loadedMatrix = ExtendedDiscreteTransitionMatrix.ExtendedDiscreteTransitionMatrix(0,0)
        self.loadedMatrix.loadFromFile(matrixName)
        self.assertNotEqual(self.matrix, self.loadedMatrix)
        self.assertEqual(len(self.matrix.transitionMatrices),len(self.loadedMatrix.transitionMatrices))
        numpy.testing.assert_array_equal([tm._probabilityMatrix for tm in self.matrix.transitionMatrices], [tm._probabilityMatrix for tm in self.loadedMatrix.transitionMatrices])
        numpy.testing.assert_array_equal([tm._transitionMatrix for tm in self.matrix.transitionMatrices], [tm._transitionMatrix for tm in self.loadedMatrix.transitionMatrices])
    
    def test_exists(self):
        print self.matrix.exists("NonExistingFilename")
        self.assertFalse(self.matrix.exists("NonExistingFilename"), "File name should not exist")
        

        
    if __name__ == '__main__':
        unittest.main()