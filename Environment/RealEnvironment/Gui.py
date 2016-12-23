'''
Created on Feb 11, 2013

@author: mrfish
'''
from PyQt4 import QtCore
import PyQt4
from PyQt4.QtCore import *
import random, sys

import Environment.RepresentationEnvironment.SOM.MyGrowingNeuralGasNode as MyGrowingNeuralGasNode 
import PyQt4.Qwt5 as Qwt
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl


class PlottingDataMonitor3D(PyQt4.QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(PlottingDataMonitor3D, self).__init__(parent)
        self.setGeometry( QtCore.QRect(200, 200 , 500, 300 ))
        self.color = [1.0, 0.1, 1.0, 0.5]
        self.lastNodePos = np.array([0.5, 0.2, 0.1])
        self.colors = np.array(([self.color]*len(self.lastNodePos)))
        self.view = gl.GLViewWidget()
        
        # first number colors seem to be color, fourth intensity
        white = (1.0, 1.0, 1.0, 1.0)
        pink = (1.0, 0.1, 1.0, 0.5)
        lightRed = (1.0, 0.1, 0.1, 0.5)
        
        
        sensorDataFloat= np.load(open("sensors.pkl", 'r'))
  
        #train
        nodes = np.zeros((5, 3))
        gng = MyGrowingNeuralGasNode.MyGrowingNeuralGasNode(start_poss = nodes, max_nodes=5)
        
        gng.train(sensorDataFloat[:,0:3])
        gng.stop_training()

        x_nodePos = [node.data.pos[0] for node in gng.graph.nodes]
        y_nodePos = [node.data.pos[1] for node in gng.graph.nodes]
        z_nodePos = [node.data.pos[2] for node in gng.graph.nodes]
        
        newNodePos = np.concatenate(([x_nodePos],[y_nodePos],[z_nodePos]),axis=0).T
        self.acc3D_sensor = gl.GLScatterPlotItem(pos = sensorDataFloat[:,0:3], color = lightRed, size = 5.0)
        self.acc3D_nodePos = gl.GLScatterPlotItem(pos = newNodePos, color = pink, size = 50.0)

        #coordinate axes
        ones = np.linspace(0, 1.0, 1000)
        zeros = np.zeros((np.size(ones)))
        axis1 = gl.GLScatterPlotItem(pos=np.concatenate(([ones],[zeros],[zeros]),axis=0).T, color = white, size = 2.0)
        axis2 = gl.GLScatterPlotItem(pos=np.concatenate(([zeros],[ones],[zeros]),axis=0).T, color = white, size = 2.0)
        axis3 = gl.GLScatterPlotItem(pos=np.concatenate(([zeros],[zeros],[ones]),axis=0).T, color = white, size = 2.0)
        
        self.view.addItem(self.acc3D_sensor)
        self.view.addItem(self.acc3D_nodePos)
        self.view.addItem(axis1)
        self.view.addItem(axis2)
        self.view.addItem(axis3)

        
        self.setCentralWidget(self.view)
        

if __name__ == "__main__":
    app = PyQt4.QtGui.QApplication(sys.argv)
    form = PlottingDataMonitor3D()
    form.show()
    sys.exit(app.exec_())
