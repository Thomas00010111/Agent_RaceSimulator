"""
A script to calculate the projection of 3D world coordinates to
2D display coordinates (pixel coordinates) for a given scene.
The 2D pixel locations of objects in the image plane are related to their
3D world coordinates by a series of linear transformations. The specific
transformations fall under the group known as projective transformations.
This set includes pure projectivities, affine transformations,
perspective transformations, and euclidean transformations. In the case
of mlab (and most other computer visualization software), we deal with
only the perspective and euclidean cases. An overview of Projective space
can be found here: http://en.wikipedia.org/wiki/Projective_space and a
thorough treatment of projective geometry can be had in the book
"Multiple View Geometry in Computer Vision" by Richard Hartley.
The essential thing to know for this example is that points in 3-space
are related to points in 2-space through a series of multiplications of
4x4 matrices which are the perspective and euclidean transformations. The
4x4 matrices predicate the use of length 4 vectors to represent points.
This representation is known as homogeneous coordinates, and while they
appear foriegn at first, they truly simplify all the mathematics
involved. In short, homogeneous coordinates are your friend, and you
should read about them here:
http://en.wikipedia.org/wiki/Homogeneous_coordinates
In the normal pinhole camera model (the ideal real world model), 3D world
points are related to 2D image points by the matrix termed the
'essential' matrix which is a combination of a perspective transformation
and a euclidean transformation. The perspective transformation is defined
by the camera intrinsics (focal length, imaging sensor offset, etc...)
and the euclidean transformation is defined by the cameras position and
orientation. In computer graphics, things are not so simple. This is
because computer graphics have the benefit of being able to do things
which are not possible in the real world: adding clipping planes, offset
projection centers, arbitrary distortions, etc... Thus, a slightly
different model is used.
What follows is the camera/view model for OpenGL and thus, VTK. I can not
guarantee that other packages follow this model.
There are 4 different transformations that are applied 3D world
coordinates to map them to 2D pixel coordinates. They are: the model
transform, the view transform, the perspective transform, and the
viewport or display transform.
In OpenGL the first two transformations are concatenated to yield the
modelview transform (called simply the view transform in VTK). The
modelview transformation applies arbitrary scaling and distortions to the
model (if they are specified) and transforms them so that the orientation
is the equivalent of looking down the negative Z axis. Imagine its as if
you relocate your camera to look down the negative Z axis, and then move
everything in the world so that you see it now as you did before you
moved the camera. The resulting coordinates are termed "eye" coordinates
in OpenGL (I don't know that they have a name in VTK).
The perspective transformation applies the camera perspective to the eye
coordinates. This transform is what makes objects in the foreground look
bigger than equivalent objects in the background. In the pinhole camera
model, this transform is determined uniquely by the focal length of the
camera and its position in 3-space. In Vtk/OpenGL it is determined by the
frustum. A frustum is simply a pyramid with the top lopped off. The top
of the pyramid (a point) is the camera location, the base of the pyramid
is a plane (the far clipping plane) defined as normal to principle camera
ray at distance termed the far clipping distance, the top of the frustum
(where it's lopped off) is the near clipping plane, with a definition
similar to that of the far clipping plane. The sides of the frustum are
determined by the aspect ratio of the camera (width/height) and its
field-of-view. Any points not lying within the frustum are not mapped to
the screen (as they would lie outside the viewable area). The
perpspective transformation has the effect of scaling everything within
the frustum to fit within a cube defined in the range (-1,1)(-1,1)(-1,1)
as represented by homogeneous coordinates. The last phrase there is
important, the first 3 coordinates will not, in general, be within the
unity range until we divide through by the last coordinate (See the
wikipedia on homogeneous coordinates if this is confusing). The resulting
coordinates are termed (appropriately enough) normalized view
coordinates.
The last transformation (the viewport transformation) takes us from
normalized view coordinates to display coordinates. At this point, you
may be asking yourself 'why not just go directly to display coordinates,
why need normalized view coordinates at all?', the answer is that we may
want to embed more than one view in a particular window, there will
therefore be different transformations to take each view to an
appropriate position an size in the window. The normalized view
coordinates provide a nice common ground so-to-speak. At any rate, the
viewport transformation simply scales and translates the X and Y
coordinates of the normalized view coordinates to the appropriate pixel
coordinates. We don't use the Z value in our example because we don't
care about it. It is used for other various things however.
That's all there is to it, pretty simple right? Right. Here is an overview:
Given a set of 3D world coordinates:
 - Apply the modelview transformation (view transform in VTK) to get eye
   coordinates
 - Apply the perspective transformation to get normalized view coordinates
 - Apply the viewport transformation to get display coordinates
VTK provides a nice method to retrieve a 4x4 matrix that combines the
first two operations. As far as I can tell, VTK does not export a method
to retrieve the 4x4 matrix representing the viewport transformation, so
we are on our there to create one (no worries though, its not hard, as
you will see).
Now that the prelimenaries are out of the way, lets get started.
"""

# Author: S. Chris Colbert <sccolbert@gmail.com>
# Copyright (c) 2009, S. Chris Colbert
# License: BSD Style

from __future__ import print_function

# this import is here because we need to ensure that matplotlib uses the
# wx backend and having regular code outside the main block is PyTaboo.
# It needs to be imported first, so that matplotlib can impose the
# version of Wx it requires.
import matplotlib
matplotlib.use('WXAgg')
import pylab as pl


import numpy as np
from mayavi import mlab
from mayavi.core.ui.mayavi_scene import MayaviScene

def get_world_to_view_matrix(mlab_scene):
    """returns the 4x4 matrix that is a concatenation of the modelview transform and
    perspective transform. Takes as input an mlab scene object."""

    if not isinstance(mlab_scene, MayaviScene):
        raise TypeError('argument must be an instance of MayaviScene')


    # The VTK method needs the aspect ratio and near and far clipping planes
    # in order to return the proper transform. So we query the current scene
    # object to get the parameters we need.
    scene_size = tuple(mlab_scene.get_size())
    clip_range = mlab_scene.camera.clipping_range
    aspect_ratio = float(scene_size[0])/float(scene_size[1])

    # this actually just gets a vtk matrix object, we can't really do anything with it yet
    vtk_comb_trans_mat = mlab_scene.camera.get_composite_projection_transform_matrix(
                                aspect_ratio, clip_range[0], clip_range[1])

     # get the vtk mat as a numpy array
    np_comb_trans_mat = vtk_comb_trans_mat.to_array()

    return np_comb_trans_mat


def get_view_to_display_matrix(mlab_scene):
    """ this function returns a 4x4 matrix that will convert normalized
        view coordinates to display coordinates. It's assumed that the view should
        take up the entire window and that the origin of the window is in the
        upper left corner"""

    if not (isinstance(mlab_scene, MayaviScene)):
        raise TypeError('argument must be an instance of MayaviScene')

    # this gets the client size of the window
    x, y = tuple(mlab_scene.get_size())

    # normalized view coordinates have the origin in the middle of the space
    # so we need to scale by width and height of the display window and shift
    # by half width and half height. The matrix accomplishes that.
    view_to_disp_mat = np.array([[x/2.0,      0.,   0.,   x/2.0],
                                 [   0.,  -y/2.0,   0.,   y/2.0],
                                 [   0.,      0.,   1.,      0.],
                                 [   0.,      0.,   0.,      1.]])

    return view_to_disp_mat


def apply_transform_to_points(points, trans_mat):
    """a function that applies a 4x4 transformation matrix to an of
        homogeneous points. The array of points should have shape Nx4"""

    if not trans_mat.shape == (4, 4):
        raise ValueError('transform matrix must be 4x4')

    if not points.shape[1] == 4:
        raise ValueError('point array must have shape Nx4')

    return np.dot(trans_mat, points.T).T


if __name__ == '__main__':
    f = mlab.figure()

    N = 4

    # create a few points in 3-space
    X = np.random.random_integers(-3, 3, N)
    Y = np.random.random_integers(-3, 3, N)
    Z = np.random.random_integers(-3, 3, N)

    # plot the points with mlab
    pts = mlab.points3d(X, Y, Z)

    # now were going to create a single N x 4 array of our points
    # adding a fourth column of ones expresses the world points in
    # homogenous coordinates
    W = np.ones(X.shape)
    hmgns_world_coords = np.column_stack((X, Y, Z, W))

    # applying the first transform will give us 'unnormalized' view
    # coordinates we also have to get the transform matrix for the
    # current scene view
    comb_trans_mat = get_world_to_view_matrix(f.scene)
    view_coords = \
            apply_transform_to_points(hmgns_world_coords, comb_trans_mat)

    # to get normalized view coordinates, we divide through by the fourth
    # element
    norm_view_coords = view_coords / (view_coords[:, 3].reshape(-1, 1))

    # the last step is to transform from normalized view coordinates to
    # display coordinates.
    view_to_disp_mat = get_view_to_display_matrix(f.scene)
    disp_coords = apply_transform_to_points(norm_view_coords, view_to_disp_mat)

    # at this point disp_coords is an Nx4 array of homogenous coordinates
    # where X and Y are the pixel coordinates of the X and Y 3D world
    # coordinates, so lets take a screenshot of mlab view and open it
    # with matplotlib so we can check the accuracy
    img = mlab.screenshot()
    pl.imshow(img)

    for i in range(N):
        print('Point %d:  (x, y) ' % i, disp_coords[:, 0:2][i])
        pl.plot([disp_coords[:, 0][i]], [disp_coords[:, 1][i]], 'ro')

    pl.show()

    # you should check that the printed coordinates correspond to the
    # proper points on the screen

    mlab.show()


































# import numpy as np
# from mayavi.mlab import plot3d, draw, show, figure
# from mayavi import mlab
# import time
#   
# # Produce some nice data.
# n_mer, n_long = 6, 11
# pi = np.pi
# dphi = pi/1000.0
# phi = np.arange(0.0, 2*pi + 0.5*dphi, dphi, 'd')
# mu = phi*n_mer
# x = np.cos(mu)*(1+np.cos(n_long*mu/n_mer)*0.5)
# y = np.sin(mu)*(1+np.cos(n_long*mu/n_mer)*0.5)
# z = np.sin(n_long*mu/n_mer)*0.5
#   
# # View it.
# fig = figure(1)
# l = plot3d(x, y, z, np.sin(mu), tube_radius=0.025, colormap='Spectral')
#   
# mlab.view(90, 0)
# 
# # Now animate the data.
# ms = l.mlab_source
# 
# i = 0
# 
# def picker_callback(picker_obj):
#     global i
#     print i
#     x = np.cos(mu)*(1+np.cos(n_long*mu/n_mer +np.pi*(i+1)/5.)*0.5)
#     scalars = np.sin(mu + np.pi*(i+1)/5)
#     ms.reset(x=x, scalars=scalars)
#     time.sleep(0.5)
#     i+=1
#     
# fig.on_mouse_pick(picker_callback)
# show()

# from mayavi import mlab
# from numpy import array, cos, sin, cos
# 
# x_coord = array([0.0, 1.0, 0.0, -1.0])
# y_coord = array([1.0, 0.0, -1.0, 0.0])
# z_coord = array([0.2, -0.2, 0.2, -0.2])
# 
# plt = mlab.points3d(x_coord, y_coord, z_coord)
# 
# msplt = plt.mlab_source
# @mlab.animate(delay=100)
# def anim():
#     angle = 0.0
#     while True:
#         x_coord = array([sin(angle), cos(angle), -sin(angle), -cos(angle)])
#         y_coord = array([cos(angle), -sin(angle), -cos(angle), sin(angle)])
#         msplt.set(x=x_coord, y=y_coord)
#         yield
#         angle += 0.1
# 
# anim()
# mlab.show()


# """ Example showing how to pick data on a surface, going all the way back
# to the index in the numpy arrays.
# In this example, two views of the same data are shown. One with the data
# on a sphere, the other with the data flat.
# We use the 'on_mouse_pick' method of the scene to register a callback on
# clicking on the sphere. The callback is called with a picker object as
# andan argument. We use the point_id of the point that has been picked,
# andand  go back to the 2D index on the data matrix to find its position.
# """
# 
# ################################################################################
# # Create some data
# import numpy as np
# pi  = np.pi
# cos = np.cos
# sin = np.sin
#  
# phi, theta = np.mgrid[0:pi:180j,0:2*pi:180j]
# m0 = 4; m1 = 3; m2 = 2; m3 = 3; m4 = 1; m5 = 2; m6 = 2; m7 = 4;
# s = sin(m0*phi)**m1 + cos(m2*phi)**m3 + sin(m4*theta)**m5 + cos(m6*theta)**m7
# x = sin(phi)*cos(theta)
# y = cos(phi)
# z = sin(phi)*sin(theta)
#  
# ################################################################################
# # Plot the data
# from mayavi import mlab
#  
# # A first plot in 3D
# fig = mlab.figure(1)
# mlab.clf()
# mesh = mlab.mesh(x, y, z, scalars=s)
# cursor3d = mlab.points3d(0., 0., 0., mode='axes',
#                                 color=(0, 0, 0),
#                                 scale_factor=0.5)
# mlab.title('Click on the ball')
#  
# # A second plot, flat
# fig2d = mlab.figure(2)
# mlab.clf()
# im = mlab.imshow(s)
# cursor = mlab.points3d(0, 0, 0, mode='2dthick_cross',
#                                 color=(0, 0, 0),
#                                 scale_factor=10)
# mlab.view(90, 0)
#  
# ################################################################################
# # Some logic to select 'mesh' and the data index when picking.
  
# def picker_callback(picker_obj):
#     picked = picker_obj.actors
#     if mesh.actor.actor._vtk_obj in [o._vtk_obj for o in picked]:
#         # m.mlab_source.points is the points array underlying the vtk
#         # dataset. GetPointId return the index in this array.
#         x_, y_ = np.lib.index_tricks.unravel_index(picker_obj.point_id,
#                                                                 s.shape)
#         print("Data indices: %i, %i" % (x_, y_))
#         n_x, n_y = s.shape
#         cursor.mlab_source.reset(x=x_ - n_x/2.,
#                                y=y_ - n_y/2.)
#         cursor3d.mlab_source.reset(x=x[x_, y_],
#                                  y=y[x_, y_],
#                                  z=z[x_, y_])
#   
# fig.on_mouse_pick(picker_callback)
#   
# mlab.show()