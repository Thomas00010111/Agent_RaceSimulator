'''
Created on Jun 29, 2013

@author: mrfish
'''
import unittest
import pickle
import numpy

import RL.QRL as QRL


class TestHRLRl(unittest.TestCase):


    def setUp(self):
        self.NumberOfStates = 5
        self.NumberOfActions = 3
        self.RL = QRL.RL(self.NumberOfStates, self.NumberOfActions )
        
    def test_save(self):
        self.RL.save("test_filename")
        
        postfix_added_by_save = "_Q_log"
        filename = "test_filename" + postfix_added_by_save
        testRlClass = pickle.load(open(filename + ".pkl", 'rb'))
        numpy.testing.assert_array_equal(testRlClass.Q, numpy.ones((self.NumberOfStates, self.NumberOfActions)))
        
        q = numpy.load(open(filename + ".npy", 'rb'))
        numpy.testing.assert_array_equal(q, numpy.ones((self.NumberOfStates, self.NumberOfActions)))
        



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()