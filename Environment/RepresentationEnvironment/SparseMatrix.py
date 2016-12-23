'''
Created on Nov 18, 2012

@author: mrfish
'''

import numpy
import scipy.sparse as sparse 

class SparseMatrix:
     
    def __init__(self, dimension, filename=None, loadId=None, dtype=numpy.float):
        self.noOfActions=dimension[0]
        self.noOfStates = dimension[1]
        #self.mtx = sparse.dok_matrix((self.noOfActions, self.noOfStates), dtype=dtype)    #slow
        self.mtx = sparse.csr_matrix((self.noOfActions, self.noOfStates), dtype=dtype)
                
                
    def __str__(self):
        return str(self.mtx.todense())
    
    def __getitem__(self, i ):
        if not type(i) == tuple:
            temp = numpy.array(self.mtx[i].todense())[0]
            return temp
        else:
            return numpy.array(self.mtx[i[0],i[1]])
    
    def __setitem__(self,i, value):
        if not type(i) == tuple:
            self.mtx[i]=value
        else:
            self.mtx[i[0],i[1]]=value 

    def __len__(self):
        return len(self.mtx.todense())
    
    @property
    def shape(self):
        return self.mtx.shape
    
    def getClassName(self):
        return self.__class__.__name__
    
    def fill(self, dummy):
        '''only for compatibility with numpy'''
        pass
            
    def dot(self, matrix):
        return self.mtx.dot(matrix)
    
                      
                      
if __name__== "__main__":
    size1 = 5
    size2 = 3
    i = 2
    mtx1 = numpy.zeros(( size1,size2), dtype = float)
    mtx1[i][i]=5
    print "mtx1: ", mtx1
    print "mtx1 row: ", mtx1[i]
    print "len: ", len(mtx1)
    
    mtx2 = sparse.dok_matrix(( size1,size2), dtype=numpy.float64)
    mtx2[i, i] = 5
    print "mtx2: ", mtx2.todense() 
    print "mtx2 row: ", mtx2[i].todense()
    print "mtx2 elem: ", mtx1[i,i]
    print "len: ", len(mtx2)
    
    mtx3 = SparseMatrix( size1,size2)
    mtx3[i,i]=5
    print "mtx3: ", mtx3
    print "mtx3 row: ", mtx3[i]
    print "mtx3 elem: ", mtx3[i,i]
    print "len: ", len(mtx3)
    