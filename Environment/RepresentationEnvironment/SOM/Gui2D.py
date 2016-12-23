'''
Created on Feb 11, 2013

@author: mrfish
'''
from PyQt4 import QtCore
import PyQt4
import numpy
from pyqtgraph.Qt import QtGui, QtCore
import sys

import Environment.RepresentationEnvironment.Colour as Colour
import PyQt4.Qwt5 as Qwt
import numpy as np
import pyqtgraph as pg


class PlottingDataMonitor2D(PyQt4.QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(PlottingDataMonitor2D, self).__init__(parent)
              
        #self.setGeometry( QtCore.QRect(200, 200 , 500, 300 ))

        self.color = (255, 0, 0)

        # Why [0.5, 0.2]?? 
        self.lastNodePos = np.array([[0.5, 0.2]])

        # to draw areas of nodes
        self.sensorValues = [numpy.array([0,0])]
        self.nodeIds =  [numpy.array([0])]
        #self.nodePosAndV = [[[]]]
        self.nodePosAndV = None
        
        win = pg.GraphicsWindow(title = "2D Graphics Window")
        #win.addViewBox()
        win.resize(700,500)
        self.p3 = win.addPlot(title = "Scatterplot")
        #p3.plot(np.random.normal(size=100), pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')
        self.p3.plot(self.lastNodePos, pen=None, symbolBrush=(255,0,0), symbolPen=None, symbol = "o")
        self.p3.showGrid(x=True, y=True)
        self.p3.enableAutoRange('xy', False)
        self.p3.setXRange(-0.1,+1.1)
        self.p3.setYRange(-0.1,+1.1)
        
        self.setCentralWidget(win)
        self.toolbar = QtGui.QToolBar()
        self.toolbar.setFixedHeight(100)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolbar)
        self.setCheckBox(self.toolbar)
        self.connect(self.checkBoxShowVValues, QtCore.SIGNAL("stateChanged(int)"), self.drawVValuesEvent)

        
#        self.view = gl.GLViewWidget()
#
#        ax = gl.GLAxisItem(size = PyQt4.QtGui.QVector3D(1.0,1.0,1.0))
#        #ax.setSize(1.0,1.0,1.0)
#        self.view.addItem(ax)
#        
#        gi = gl.GLGridItem(size = PyQt4.QtGui.QVector3D(1.0,1.0,1.0))
#        self.view.addItem(gi)
#        
#        self.acc3D_sp = gl.GLScatterPlotItem(pos = self.lastNodePos, color = (1.0, 0.1, 1.0, 0.5), size = 5.0)
#        self.view.addItem(self.acc3D_sp)
#        
#        self.setCentralWidget(self.view)

    def drawVValuesEvent(self):
        self._plotTextItem(self.nodePosAndV)

    def setCheckBox(self, parent):
        self.checkBoxShowVValues = QtGui.QCheckBox("Show V-Values", parent=parent)
        self.checkBoxShowVValues.adjustSize()
        self.checkBoxShowVValues.setChecked(True)
        

#https://stackoverflow.com/questions/16844693/pyqtgraph-chaco-guiqwt-fast-scrolling-timetrace-demo
#     def set_spinbox(self, parent):
#         self.spinb = QtGui.QDoubleSpinBox(parent=parent)
#         self.spinb.setDecimals(3)
#         self.spinb.setRange(0.001, 3600.)
#         self.spinb.setSuffix(" s")
#         self.spinb.setValue(1)   # set the initial width
#         #self.spinb.valueChanged.connect(self.xwidth_changed)
#         #parent.addWidget(self.spinb)

    def _plotNodes(self, nodePos):
        self.p3.plot(self.lastNodePos, pen=None, symbolPen=None).setData(nodePos, symbolBrush=self.color, symbol = "d")
    
    def _plotTextItem(self, nodePosAndV):
        for posV in nodePosAndV:
            #print "_plotTextItem: pos: ", posV[0], "   Number_V:", posV[1], "   Number: ", posV[2], "   V:", posV[3]
            #NumberV = str(posV[2][0]) + "_" + str(posV[3][1])
            NumberV = str(posV[1][0])
            text = pg.TextItem(NumberV,  color=( 0, 200, 0), anchor=(0.0,0.0), border='w', fill=(0, 0, 255, 100))
            text.setPos(posV[0][0],posV[0][1] )
            self.p3.addItem(text)
    
    def _plotCurrentPos(self, currentPos):
        colorPoint = (0,255,0)
        points = np.vstack([currentPos])  
        self.p3.plot(points, pen=None, symbolPen=None).setData(points, symbolBrush=colorPoint)

        
    def replotEvent(self, nodePosAndV, currentPos):
        self.nodePosAndV = nodePosAndV
        self.p3.clear()
        self._drawPointsEvent(self.sensorValues, self.nodeIds)       
        self._plotNodes(numpy.array([nodeV[0] for nodeV in nodePosAndV]))
        self._plotCurrentPos(currentPos)
        if self.checkBoxShowVValues.checkState():
            self._plotTextItem(nodePosAndV)
    
        
    def updatePointsEvent(self, sensorValues, nodeIds):
        self.sensorValues = sensorValues
        self.nodeIds = nodeIds
        #numpy.savetxt("sensorValues.txt", self.sensorValues, fmt='%.2e') 
        #numpy.savetxt("nodeIds.txt", self.nodeIds, fmt='%.2e')
        #numpy.savetxt("nodeIds.txt", self.nodeIds)

    
        
    def _drawPointsEvent(self, sensorValues, nodeIds):
        #WE GET AN ERROR HERE!!!
        #IT SEEMS SOMETHING IN FUNCTION PLOT IS CHANGED!!!
        # "symbolBrush=" DOES NOT ACCEPT THE LIST ANYMORE!!! 
        colorPoint = (0,255,0)
        
        colors = []
        myColors = Colour.Colour(max(nodeIds)+1)
        for p in nodeIds:
            colors.append(myColors.getColourForState(p))
            #colors.append(colorPoint)
        points = numpy.array(sensorValues)
        #self.p3.plot(self.lastNodePos, pen=None, symbolPen=None).setData(points, symbolBrush=colors)
        self.p3.plot(self.lastNodePos, pen=None, symbolPen=None).setData(points, symbolBrush=colorPoint)
    
        
    def addPointEvent(self, pointPos):
        colorPoint = (0,255,0)
        # add new point and color of point
        points = np.vstack([self.lastNodePos, [pointPos]])
        colors = list(self.colorsList)
        colors.append(colorPoint)   
        self.p3.clear()
        self.p3.plot(self.lastNodePos, pen=None, symbolPen=None).setData(points, symbolBrush=colors)
#        self.p3.setData(points, symbolBrush=colors)
        
    def replotNodesAndValuesEvent(self, nodePosAndV):
        #self.p3.clear()
        self.updatePointsEvent(self.sensorValues, self.nodeIds)
        self._plotNodes(numpy.array([nodeV[0] for nodeV in nodePosAndV]))
        self._plotTextItem(nodePosAndV)
        
                
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv).instance()
    form = PlottingDataMonitor2D()
    form.show()
    sys.exit(app.exec_())
    


