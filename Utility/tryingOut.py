import itertools
#from mayavi import mlab
#from mayavi.plugins.app import Mayavi
import numpy 
import kdtree
import matplotlib.pyplot as plt


    
rangeCarPosX = numpy.linspace( 10, 190,40)
#rangeCarPosX = [150]
print "rangeCarPosX: ", rangeCarPosX
    
#rangeCarPosY = [CarPosY]
rangeCarPosY = numpy.linspace( 10, 190,40)
print "rangeCarPosY: ", rangeCarPosY

print numpy.array([[x[1],x[0]] for x in itertools.product(rangeCarPosX, rangeCarPosY, repeat=1)])


# sequence = ["".join(seq) for seq in itertools.product("01", repeat=3)]
# print sequence
# points_temp= numpy.array([list(s) for s in sequence])
# points_new = numpy.array([map(float, f) for f in points_temp])
# points = numpy.array([[0.0, 0.0,  0.0],[0.0 ,  0.0, 1.0], [ 0.0, 1.0, 0.0], [ 0.0, 1.0, 1.0], [1.0, 0.0,  0.0], [1.0, 0.0,  1.0], [1.0, 1.0,  0.0], [1.0, 1.0,  1.0]])
#  
# print points_new
# print points



# a = list(['001','011'])
# print a
# b = [list(s) for s in a]
# results = [map(int, f) for f in b]
# print results
#c=[float(f) for f in b ]








# def fkt():
#     return [1,2,3]
# 
# 
# print 2*fkt()
# plt.plot([2,2,2],fkt(),'ro')
# 
# plt.show()


# years = {
#     2006: ['A', 'B', 'C', 'D', 'E'],
#     2007: ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'],
#     2008: ['E', 'F', 'G'],
# }
# print years[2006]
# 
# for i in years[2006]:
#     print i





# n = 8.0
# range0=numpy.linspace( 0 + 1/n, 1-1/n,n-1,True )
# rangex=numpy.array([0.5, 0.25, 0.75, ])
# rangey=numpy.array([0.5, 0.5, 0.5,])
# nodes = numpy.array([x for x in itertools.product(range0, range0, repeat=1)])
# print (nodes)
# 
# list_nodes = []
# for nod in nodes:
#     list_nodes.append(nod)
# 
# tree = kdtree.create(list_nodes)
# 
# 
# kdtree.visualize(tree)
# kdtree.plot2D(tree)

# a = 5
# b = numpy.array([a,a])
# print b
# print b.shape

# currentState = numpy.array([2045, 1533, 1532, 1404, 1340, 1339, 1323, 1322, 1321, 1319])
# goalState = numpy.array([1534, 1405])
# 
# indexGoalState = [index for index,s in enumerate(currentState) if s in goalState]
# if indexGoalState:
#     print "goal" 

# for i in [index for index,d in enumerate(a!=b) if d]:
#     print i





# list = []
# list.append([4, 2, 3, "abcd"])
# list.append([5, 2, 3, "gbcd"])
# 
# print list[1]
# 
# data = numpy.zeros((3,5))
# data[1][1]=1
# data1=numpy.array([1,2,3])
# print data
# print data1








# V = numpy.array([10,15,12,13, 14, 15])
# currentState = numpy.array([1,2,3])
# 
# temp = numpy.zeros((currentState.size, 2))
# for i in range(0,currentState.size):
#     temp[i] = [currentState[i] , V[currentState[i]]]  
# print max(temp, key=lambda x: x[1])







# x = [1, 2, 3, 4, 5, 6]
# y = [0, 0, 0, 0, 0, 0]
# z = y
# 
# s = [.5, .6, .7, .8, .9, 1]
# 
# 
# pts = mlab.points3d(x, y, z, s)
# mlab.show()
# DimensionData=3
# upper=15
# dimension=(15,15,15)
# nodes1 = numpy.array([x for x in itertools.product(range(upper), repeat=DimensionData)])
# nodes2 = numpy.array([x for x in itertools.product(range(dimension[0]), range(dimension[1]), range(dimension[2]), repeat=1)])
# 
# print nodes1
# print nodes2
# print "length:", len(nodes1)
# print "length:", len(nodes2)
# 
# print max(dimension)





# dimension=(3,3,2)
# print dimension[0]
# #g0 = numpy.array([x for x in itertools.product([0,1,2],[0,1,2], repeat=1)])
# g1 = numpy.array([x for x in itertools.product([0,1,2],[0,1,2], [0,1],repeat=1)])
# 
# for i in range(0,len(g1[0])): 
#     print g1[:,i]

#g2 = numpy.array([x for x in itertools.product([0,1],g1,repeat=1)])
# print "g: ", g1
# print "length:", len(g1)

# upper = 4
# #nD
# n=2 
# e = numpy.array([x for x in itertools.product(range(upper), repeat=n)])
# e = e/float(upper-1)
# print "e: ", e
# 
# f = numpy.array([x for x in itertools.product(range(upper), range(upper),repeat=2)])
# print "f: ", f
# 
# g = numpy.array([x for x in itertools.product([0,1], [2,3,4],repeat=2)])
# print "g: ", g

# #3D
# upper = 3
# f1=itertools.product(range(upper), range(upper))
# print "f:"
# for f in f1:
#     print f
# 
# 
# for i in f1:
#     a = itertools.product([i], range(upper))
#     for t in a:
#         print t

# print "g:"    
# for g in itertools.product(x for x in f1, range(upper)):
#     print g
    
#print f1 * range(upper)


# e = numpy.array([x for x in itertools.product(f, range(upper))])
# e = e/float(upper-1)
# print e

   
# b = numpy.array([x for x in permutations(range(upper),2)])
# print "b:", b
# b = b/float(upper-1)
# print b
# for c in itertools.combinations_with_replacement(range(upper),2):
#     print c
# 
# print
# print
# print"d:"    
# for d in itertools.permutations(range(upper),2):
#     print d
