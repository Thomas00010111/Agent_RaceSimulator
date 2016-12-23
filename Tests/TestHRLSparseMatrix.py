'''
Created on Jan 27, 2013

@author: mrfish
'''

import numpy
import numpy.testing
import unittest
import scipy.sparse as sparse 

import Environment.RepresentationEnvironment.SparseMatrix as SparseMatrix


class TestHRLProbabilityTransitionMatrix(unittest.TestCase):
    ''' The interface to the Sparse Matrix should be similar to the earlier used matrix for which numpy arrays were used.
        Unfortunately addressing an element like matrix[i][j] is not possible with this wrapper'''
#
    def setUp(self):
        self.NumberOfStates = 5
        self.NumberOfActions = 3
        
        self.matrix_numpy = numpy.zeros(( self.NumberOfActions,self.NumberOfStates), dtype = float)
        self.matrix_sparse = SparseMatrix.SparseMatrix(( self.NumberOfActions,self.NumberOfStates), dtype = float)
        
        
    # test initialization of matrix (not predefined function of the test framework)
    def test_init(self):
        self.assertEqual(len(self.matrix_numpy), len(self.matrix_sparse))
        self.assertEqual(len(self.matrix_numpy[1]), len(self.matrix_sparse[1]))
        self.assertEqual(self.matrix_numpy.shape, self.matrix_sparse.shape)
    
    def test_getElement(self):
        index1 = 2
        index2 = 3
        value = 123.0
        self.matrix_numpy[index1][index2] = value
        self.matrix_sparse[index1,index2] = value
        self.assertEqual(self.matrix_numpy[index1][index2], self.matrix_sparse[index1, index2])
        
    def test_getRow(self):
        index1 = 2
        self.matrix_numpy[index1]
        self.matrix_sparse[index1]
        numpy.testing.assert_array_equal(self.matrix_numpy[index1], self.matrix_sparse[index1])
        
    def test_dot(self):
        matrix_numpy1 = numpy.array([[0.1, 0.3,  0.9, 0.0,  0.0 ],
                                    [ 0.5, 0.7,  0.0, 0.0, 0.01 ]], dtype = float)
        
        matrix_numpy2 = numpy.array([[0.1, 0.3],
                                     [0.9, 0.0],
                                     [0.0, 0.5],
                                     [0.7, 0.0],
                                     [0.0, 0.01]], dtype = float)
        
        matrix_result_numpy = numpy.dot(matrix_numpy1, matrix_numpy2)
        
        matrix_sparse_temp = sparse.dok_matrix([[0.1, 0.3,  0.9, 0.0,  0.0 ],
                                                [ 0.5, 0.7,  0.0, 0.0, 0.01 ]], dtype = float)
        matrix_sparse = SparseMatrix.SparseMatrix(( self.NumberOfActions,self.NumberOfStates), dtype = float)
        matrix_sparse.mtx = matrix_sparse_temp
        
        matrix_result_sparse = matrix_sparse.dot(matrix_numpy2)

        numpy.testing.assert_array_equal(matrix_result_numpy, matrix_result_sparse) 
        
        
#     i = 2
#     mtx1 = numpy.zeros(( size1,size2), dtype = float)
#     mtx1[i][i]=5
#     print "mtx1: ", mtx1
#     print "mtx1 row: ", mtx1[i]
#     print "len: ", len(mtx1)
#     
#     mtx2 = sparse.dok_matrix(( size1,size2), dtype=numpy.float64)
#     mtx2[i, i] = 5
#     print "mtx2: ", mtx2.todense() 
#     print "mtx2 row: ", mtx2[i].todense()
#     print "mtx2 elem: ", mtx1[i,i]
#     print "len: ", len(mtx2)
#     
#     mtx3 = SparseMatrix( size1,size2)
#     mtx3[i,i]=5
#     print "mtx3: ", mtx3
#     print "mtx3 row: ", mtx3[i]
#     print "mtx3 elem: ", mtx3[i,i]
#     print "len: ", len(mtx3)

        
        
    if __name__ == '__main__':
        unittest.main()