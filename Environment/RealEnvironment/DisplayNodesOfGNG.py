'''
Created on Feb 11, 2013

@author: mrfish
'''
import Tkinter, tkFileDialog
import mayavi.mlab
import numpy 


root = Tkinter.Tk()
root.withdraw()

initialDirectory="/home/mrfish/MrFish/Source Code/Workspace/HierarchicalRL_ContinuousActionAndEnv/Environment/RealEnvironment"
file_path = tkFileDialog.askopenfilename(initialdir=initialDirectory, filetypes = [('numpy files', '.pkl')])

white = (1, 1, 1)
black = (0, 0, 0)
red = (1, 0, 0)        
        
x= numpy.load(open(file_path, 'r'))

print x

mayavi.mlab.points3d(x[:,0], x[:,1], x[:,2], transparent=True, opacity=0.3)
mayavi.mlab.points3d(x[:,0], x[:,1], x[:,2], scale_factor=.01, color=black)
mayavi.mlab.axes()
mayavi.mlab.xlabel('x - axis')
mayavi.mlab.ylabel('y - axis')
mayavi.mlab.zlabel('z - axis')
mayavi.mlab.outline()
mayavi.mlab.colorbar()
mayavi.mlab.show()
        
