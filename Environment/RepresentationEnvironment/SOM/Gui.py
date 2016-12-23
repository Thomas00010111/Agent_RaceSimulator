'''
Created on Feb 11, 2013

@author: mrfish
'''
from PyQt4 import QtCore
import PyQt4
import sys

import Environment.RepresentationEnvironment.SOM.Gui2D as Gui2D
import PyQt4.Qwt5 as Qwt


#import Environment.RealEnvironment.JavaSomEnvironment as JavaEnvironment
#import SimplePreMountainCarAgentJava.client  
#sys.stdout = open("myLog.txt", "w")      
class Form(PyQt4.QtGui.QMainWindow):
    def __init__(self, model, gui, parent=None):
        super(Form, self).__init__(parent)       
        self.connect(model, QtCore.SIGNAL("addPointEvent(PyQt_PyObject)"), self.addPointEvent )
        self.connect(model, QtCore.SIGNAL("replotNodesAndValuesEvent(PyQt_PyObject)"), self.replotNodesAndValuesEvent )
        self.connect(model, QtCore.SIGNAL("replotEvent(PyQt_PyObject, PyQt_PyObject)"), self.replotEvent )
        self.connect(model, QtCore.SIGNAL("updatePointsEvent(PyQt_PyObject, PyQt_PyObject)"), self.updatePointsEvent )
        self.gui = gui

        
    def addPointEvent(self, pointPos):
        self.gui.addPointEvent(pointPos)
        
    def replotNodesAndValuesEvent(self, nodePosAndV):
        self.gui.replotNodesAndValuesEvent(nodePosAndV)
    
    def replotEvent(self, nodePosAndV, currentPos):
        self.gui.replotEvent(nodePosAndV, currentPos)
        
    def updatePointsEvent(self, coordinate, NodeId):
        self.gui.updatePointsEvent(coordinate, NodeId)
        
    def show(self):
        self.gui.show()
        
        
def main():
    app = PyQt4.QtGui.QApplication(sys.argv)
    myclient = JavaEnvironment.JavaSomEnvironment()
    gui = Gui2D.PlottingDataMonitor2D()
    form = Form(myclient, gui)
    form.show()
    myclient.start()
    sys.exit(app.exec_())
     
 
if __name__ == "__main__":
    main()
