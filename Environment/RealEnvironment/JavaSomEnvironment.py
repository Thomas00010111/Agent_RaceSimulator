'''
Created on Nov 28, 2012

@author: mrfish

Uses: Java environment mit punkt, es werden nur zwei Koordinaten der Java Umgebung
durch eine SOM diskretisiert.


'''

from PyQt4 import QtCore
import PyQt4
import numpy
import random

import Environment.IEnvironment
import Environment.RealEnvironment.JavaEnvironmentEistuete as JavaEnvironment
import PyQt4.Qwt5 as Qwt


#import Environment.RealEnvironment.JavaEnvironmentEistuete as JavaEnvironment 
#NUMBER_OF_ACTIONS = 4
NUMBER_OF_SIMPLE_ACTIONS = 4

FileNameProbMatrices = "Probab1l1tyMatr1x"


class JavaSomEnvironment(JavaEnvironment.JavaEnvironmentEistuete, QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self,parent)
        JavaEnvironment.JavaEnvironmentEistuete.__init__(self)
        self.sensorData = numpy.array([0, 0])
    
    def GotoRandomState(self, currentNState):
        ''' returns a random state that can be reached'''
        index = random.randint(0, NUMBER_OF_SIMPLE_ACTIONS-1)
        return index, self.EnvironmentMatrix[self.prevState][index]
    
         
        
        

            
            

            
