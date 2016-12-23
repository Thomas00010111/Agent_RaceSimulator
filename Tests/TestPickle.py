import pickle
import Agent.BaseLevel as BaseLevel
import unittest

class A():
       def __init__(self):
           pass
           
       def init(self, var1, var2):
           self.var1 = var1
           self.var2 = var2
           
       def save(self, filename):
           pickle.dump(self, open(filename, 'wb'))
       
       def load(self, filename):
           return pickle.load(open(filename, 'rb'))
       
#https://stackoverflow.com/questions/2709800/how-to-pickle-yourself
class C():
    def __init__(self, var1, var2):
        self.var1 = var1
        self.var2 = var2
        
    def save(self, filename):
        pickle.dump(self, open(filename, 'wb'))
    
    @classmethod
    def load(cls, filename):
        return pickle.load(open(filename, 'rb'))

class TestPickleUnpickle(unittest.TestCase):
        
    def testSimplePickleA(self):
        filename = "NameA.pkl"
        aVariable = 1.0
        aString = "testA" 
        a = A()
        a.init(aVariable, aString)
        a.save(filename)
        
        a_unpickled = pickle.load(open(filename, 'rb'))
        
        self.assertEqual(aString,a_unpickled.var2, "not equal")
        self.assertEqual(aVariable,a_unpickled.var1, "not equal")
        
    def testSimplePickleC(self):
        filename = "NameC.pkl"
        aVariable = 11.0
        aString = "testC" 
           
        c=C(aVariable, aString)
        c.save("NameC.pkl")
        c.var1 = 12
        
        c_unpickled=C.load("NameC.pkl")
         
        self.assertEqual(aString,c_unpickled.var2, "not equal")
        self.assertEqual(aVariable,c_unpickled.var1, "not equal")   
        
        
        
class TestPickleUnpickleBaseLevel(unittest.TestCase):
        
    def testPickleUnpickle(self):
        filename = "NameBaseLevel.pkl"
        aString = "testBaseLevel"
        numberOfStates = 12345
        numberOfActions = 3
         
        b = BaseLevel.BaseLevel(aString)
        b.createRL(numberOfStates, numberOfActions)
        b.dumpRL(filename)
        
        b_unpickled = BaseLevel.BaseLevel(aString)
        b_unpickled.createRLFromFile(filename)
        
        self.assertEqual(b_unpickled.getNumberOfStates(),numberOfStates, "not equal")
        self.assertEqual(aString,b_unpickled.name, "not equal")
        
        
if __name__ == '__main__':
    unittest.main()
    
    
    
    
        
        
        
        
        