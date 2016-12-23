'''
Created on Jun 29, 2013

@author: mrfish
'''
import unittest

import RL.RL as RL


class TestHRLRl(unittest.TestCase):


    def setUp(self):
        self.NumberOfStates = 5
        self.RL = RL.RL(self.NumberOfStates)
        
    def test_getRewardedTransitions(self):
        fromState = 3
        toState = 3
        self.assertEqual(self.RL.getRewardedTransitions(fromState, toState), 0)
        
    def test_Update_prevValueGetsReduced(self):
        prev=1
        current = 2
        
        #set prev and current to 1
        self.RL.setV(prev, 1)
        self.RL.setV(current, 1)
        
        oldValue=self.RL.getV(prev)
        self.RL.Update(prev, current, 0) #no reward
        ValueDelta = self.RL.getDeltaV()[prev]
        self.assertGreater(oldValue, self.RL.getV(1), "V-value did not change after update")
        self.assertGreater(ValueDelta, 0, "Delta of V-value did not change after update")
        
    def test_UpdateGoalState_valueHasToChange(self):    
        goalState=self.NumberOfStates-1
        vValueVirtualState = 1
        reward = 1
        
        oldValue=self.RL.getV(goalState)    
        self.RL.UpdateGoalState(goalState, vValueVirtualState, reward)
        self.assertGreater(self.RL.getV(goalState), oldValue, "V-value of goal state did not increase after update")




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    