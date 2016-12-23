'''
Created on Jun 29, 2013

@author: mrfish
'''
import random
import subprocess
import unittest

import Environment.RealEnvironment.JavaEnvironmentEistuete as JavaEnvironmentEistuete


class TestHRLStateSpaceDiscretization(unittest.TestCase):

# Autmatisches starten des Servers klappt nicht... 
# Muss zweimal gestartet werden, wahrscheinlich um erst eine Exception im Server zu provozieren
    def setUp(self):
        self.environment = JavaEnvironmentEistuete.JavaEnvironmentEistuete()
#        subprocess.call(["cd", "~/MrFish"])
#        subprocess.call(["java EnvironmentServerUDP &"])
#         cd ~/MrFish/Source\ Code/Workspace/EnvironmentServer/branches/bin
#        cd /MrFish/Source Code/Workspace/EnvironmentServer/branches/bin$ java EnvironmentServerUDP &

    # If connection procedure and action sending is out in two differnt functions
    # test fails    
    def test_connect(self):
        self.environment.connect()
        self.environment.Send("RESTAR")
        self.environment.TryReceive()
        self.environment.restart()
    
        for msgId_test in range(1,10000):
            self.environment.TryReceive()
            #self.assertEqual(msgId_test, float(self.environment.msgId),"msgId not correct, received msgId has to be used for next sent message")
            
            if random.randint(0,3)==1:
                self.environment.restart()   
            else: 
                myAction = "ACTION:" + str(random.randint(0,4))
                self.environment.Send(myAction)
        
        
        
        
    
    