import mayavi.mlab
import numpy


class Scatterplot4D:
    def __init__(self, nodes, scalars=None):
        if scalars==None:
            scalars = numpy.zeros(nodes.shape[0])
        self.graph=mayavi.mlab.points3d(nodes[:,0], nodes[:,1], nodes[:,2], scalars,transparent=True, scale_factor=0.05, opacity=0.3)
        
        # plot axes
        mayavi.mlab.axes()
        mayavi.mlab.xlabel('X')
        mayavi.mlab.ylabel('Y')
        mayavi.mlab.zlabel('theta')
        mayavi.mlab.outline() 
        mayavi.mlab.colorbar()
       
    
    def update(self, nodes, scalars):
        self.graph.mlab_source.scalars=scalars
        self.graph.mlab_source.set(points=nodes)
        
    def show(self):
        mayavi.mlab.show()