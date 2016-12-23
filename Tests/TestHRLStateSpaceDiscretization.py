'''
Created on Jun 29, 2013

@author: mrfish
'''
import math
import numpy
import unittest

import Environment.RepresentationEnvironment.SOM.StateSpaceDiscretization as StateSpaceDiscretization


class TestHRLStateSpaceDiscretization(unittest.TestCase):


    def setUp(self):
        # 2D
        self.NumberOfStates = 16
        square = math.sqrt(self.NumberOfStates)
        if(square-int(square)):
            AssertionError
            
        self.SSD = StateSpaceDiscretization.StateSpaceDiscetization(self.NumberOfStates)
        
        #3D
        self.NumberOfStates_3D = 5
        self.SSD_3D = StateSpaceDiscretization.StateSpaceDiscetization(5, grow=True)
        
    def test_initalSetUp(self):
        self.assertEqual(len(self.SSD.gng.graph.nodes), self.NumberOfStates)
        
    def test_checkLabels(self):
        for n,node in enumerate(self.SSD.gng.graph.nodes):
            self.assertEqual(node.data.label,n)
    
    
    def test_addingNode(self):
        position = numpy.array([0.5,0.5])
        self.SSD.addNode(position)
        node = self.SSD.getNearestNode(position)
        self.assertEqual(node.data.label,self.NumberOfStates)
        pass
    
    
    def test_addingSeveralNodes(self):
        p = numpy.linspace(0.1,1.1,20)
        index = self.NumberOfStates
        for p1 in p:
            for p2 in p:
                position = numpy.array([p1,p2])
                self.SSD.addNode(numpy.array(position))
                node = self.SSD.getNearestNode(position)
                self.assertEqual(node.data.label,index)
                index+=1
                
    def test_generateLabels(self):
        x = numpy.load(open("sensors_test.pkl", 'r'))
        STEP = 1
        for i in range(0,x.shape[0],STEP): 
            self.SSD_3D.train(x[i:i+STEP])
            print "i: ", i, "   nodes: ", len (self.SSD_3D.gng.graph.nodes)

        self.SSD_3D.generateLabels()
        for nodeIdTest, nodeId in enumerate(self.SSD_3D.gng.graph.nodes):
            self.assertEqual(nodeId.label,nodeIdTest)
            
        self.assertGreaterEqual(self.NumberOfStates_3D, len(self.SSD_3D.gng.graph.nodes))
        
        self.assertEqual(self.SSD_3D.gng.graph.nodes[-1].label, len(self.SSD_3D.gng.graph.nodes)-1) 
        
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    