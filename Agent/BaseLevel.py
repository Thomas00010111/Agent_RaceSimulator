'''
Created on Nov 24, 2012

@author: mrfish
'''
import RL.QRL as RL
import numpy
import pickle

class BaseLevel():
    def __init__(self, name = None):
        self._RL = None
        self.name = name
        
    def getNumberOfStates(self):
        return self._RL.getNumberOfStates()
    
    def setNumberOfStates(self, numberOfStates, numberOfActions):
        assert False, "use self.createRL(numberOfStates, numberOfActions)"
    
    def createRL(self, numberOfStates, numberOfActions):
        self._RL = RL.RL(numberOfStates, numberOfActions) 
        
    def createRLFromFile(self, filename):
        self._RL = pickle.load(open(filename + ".pkl", 'rb'))
        
    def dumpRL(self, filename):
        '''save whole RL object'''
        pickle.dump(self._RL, open(filename + ".pkl", 'wb'))        
        
    def saveVvalues(self):
        filename = "V_" + self.name + ".pkl"
        numpy.save(open( filename, "wb" ), self.rl.getVStates())
        #pickle.dump(self.rl.getVStates(), open( filename, "wb" ))
        
    def log(self, text, filename, mode):
        f = open(filename, mode)
        f.write(str(text)+'\n')
        f.close()
     
    @property   
    def rl(self):
        return self._RL
    