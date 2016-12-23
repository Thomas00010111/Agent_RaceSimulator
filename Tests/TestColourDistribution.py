'''
Created on Jan 27, 2013

@author: mrfish
'''

import numpy
import numpy.testing
import unittest

import Environment.RepresentationEnvironment.Colour as Colour


class TestColour(unittest.TestCase):
    
#
    def setUp(self):
        numberOfStates=5
        self.myColour=Colour.Colour(numberOfStates)
   
    def test_getColourForState(self):
        state=3
        self.myColour.getColourForState(state)
           
    if __name__ == '__main__':
        unittest.main()