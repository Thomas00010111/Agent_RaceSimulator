import numpy

import Environment.RepresentationEnvironment.ExtendedDiscreteTransitionMatrix as ExtendedDiscreteTransitionMatrix


State = 100
path = "../../../../../LogFiles/ExtendedTransitionMatrices"
extendedMatrix = ExtendedDiscreteTransitionMatrix.ExtendedDiscreteTransitionMatrix(8,12*12*12*2, "matrix", path)
extendedMatrix.displayProbabilityMatrix(State)

# extendedMatrix = ExtendedDiscreteTransitionMatrix.ExtendedDiscreteTransitionMatrix(8,12*12*12*2, "matrix", "ExtendedTransitionMatrices", loadAll=True)
# for tm in extendedMatrix.transitionMatrices:
#     print tm.getReachableStates()
    
    #     [1680, 1656, 1632, 1682, 1658, 1704, 1710, 1686, 1662, 1660,1684]
#     itemindex1 = numpy.where( tm.getReachableStates()==1682 )
#     itemindex2 = numpy.where( tm.getReachableStates()==1658 )
#     itemindex3 = numpy.where( tm.getReachableStates()==1704 )
#     
# print itemindex1
# print itemindex2
# print itemindex3