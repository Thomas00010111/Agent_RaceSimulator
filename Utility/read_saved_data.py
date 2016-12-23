'''
Created on Feb 11, 2013

@author: mrfish
'''
import Tkinter, tkFileDialog
import numpy
import pickle



root = Tkinter.Tk()
root.withdraw()

initialDirectory="/home/mrfish/Dropbox/Workspace/Agent_MyRaceSimulator/Environment/RealEnvironment"
file_path = tkFileDialog.askopenfilename(initialdir=initialDirectory, filetypes = [('numpy files', '.pkl')])       
        
        
V = pickle.load(open( file_path, 'rb' ))        
        
for n in V:
    print n        
        
print min( [n[4] for n in V] )

# V = numpy.load(open( file_path, 'rb' ))
 
# for n in V[:,[0,4]]:
#     if n[0] > 0.0:
#         print n
#  
# print min( [n for n in V[:,4] if n > 0.0] )
        








# print "number of V values: ", len(V)
# 
# NumberStates = math.sqrt(len(V))
# decimal, intPart = math.modf(NumberStates)
# if decimal == 0.0:
#     NumberStates = int(NumberStates)
# else:
#     print "ERROR: cannot reshape states, not n x n"
#     sys.exit()
#     
# vReashaped = numpy.reshape(V, (NumberStates, NumberStates))
# 
# x, y, z = [], [], []
# 
# for vi1, vline in enumerate(vReashaped):
#     print vline
#     for vi2, v in enumerate(vline):
#         x.append(vi1)
#         y.append(vi2)
#         z.append(v)
#         
# mayavi.mlab.barchart(x, y, z)
# 
# # plot axes
# mayavi.mlab.axes()
# mayavi.mlab.xlabel('x')
# mayavi.mlab.ylabel('y')
# mayavi.mlab.zlabel('V')
# mayavi.mlab.outline()
# mayavi.mlab.colorbar()
# mayavi.mlab.show()

