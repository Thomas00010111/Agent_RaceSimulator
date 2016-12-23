'''
Created on Feb 11, 2013

@author: mrfish
'''
import Tkinter, tkFileDialog
import numpy

import Environment.RepresentationEnvironment.SOM.Scatterplot4D as Scatterplot4D 
import Environment.RepresentationEnvironment.SOM.StateSpaceDiscretization as StateSpaceDiscretization


root = Tkinter.Tk()
root.withdraw()
 
initialDirectory="/home/mrfish/MrFish/Source Code/Workspace/Agent_MyRaceSimulator/Environment/RealEnvironment"
file_path_states = tkFileDialog.askopenfilename(initialdir=initialDirectory, filetypes = [('States (numpy file)', '.pkl')])       
nodes = numpy.load(open( file_path_states, 'rb' ))
print "number of states: ", len(nodes)
 
file_path_v = tkFileDialog.askopenfilename(initialdir=initialDirectory, filetypes = [('V (numpy file)', '.pkl')])
V = numpy.load(open( file_path_v, 'rb' ))
 
print "number of V values: ", len(V)


#draw nodes
scalars = V.reshape(1,V.shape[0])[0]
print "scalars:", scalars 
graph = Scatterplot4D .Scatterplot4D(nodes, scalars)
graph.show()




        
