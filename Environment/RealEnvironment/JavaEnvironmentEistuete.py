'''
Created on Nov 28, 2012

@author: mrfish

Uses: Java Eistuete mit Dreirad. Es werden alle drei Koordinaten in einen State uebersetzt.
Ohne SOM.

'''
#import Environment.RepresentationEnvironment.Action as Action
import datetime
from socket import *

import Environment.IEnvironment


SERVER_IP = "127.0.0.1"
SERVER_PORT = 4444

# Maximal size of file read from socket
BUFSIZE = 2048

FileNameProbMatrices = "Probab1l1tyMatr1x3D"

class JavaEnvironmentEistuete(Environment.IEnvironment.IEnvironment):
    def __init__(self):
        self.prevState = 0
        self.socket = None
        self.msgId = 0
#        assert (len(self.environmentActions)== numberOfActions),"Number of Actions not equal Number of environment Actions" 
        self.connect()
        
    
    def connect(self):    
        try:
            self.socket = socket(AF_INET, SOCK_DGRAM)
            self.socket.settimeout(2)   #timeout of 1s
        except:
            print "No connection to server"
            self.socket.close()
            sys.exit()
            
    def Send(self, stringToSend):
        try:
            msgstr = str(self.msgId) +";" + stringToSend +";"
            sent = self.socket.sendto(msgstr, (SERVER_IP, SERVER_PORT))
            print "sent: ", sent, "  msgstr: ", msgstr 
        except IOError as e:
            print "Error during send, I/O error({0}): {1}".format(e.errno, e.strerror)
            self.socket.close()
            sys.exit()  
        return sent  

            
    def TryReceive(self):
        msg_in = ""
        try:
            msg_in = self.socket.recv(BUFSIZE)
            recTime = datetime.datetime.now()
            print "[",recTime,"] received:", msg_in
        except IOError as e:
            print "Error during receive, I/O error({0}): {1}".format(e.errno, e.strerror)
            #self.socket.close()
            return None
        self.msgId = msg_in.split(";",2)[0]
        print "msgId = ", self.msgId
        msg = msg_in.split(";",2)[1]
        return msg.split(":") 
        
    def restart(self):
        self.Send("CARRAM")
        
    def setToStart(self):
        self.Send("RACRES")
        
    def getCurrentPos(self):
        self.Send("CURPOS")
    
    def getRewardFromEnvironment(self):
        reward = float(self.TrySendReceive("CURPOS")[3])
        print "Environment:getRewardFromEnvironment: reward:", reward
        return reward
        
        
    def log(self, text, filename,mode):
        f = open(filename, mode)
        f.write(str(text)+'\n')
        f.close()
        
    def addDateToCurrentLogFiles(self, files):
        [os.rename(f, str(datetime.datetime.now()) + '_' + f) for f in files]
    
    def deleteLogFiles(self, files):
        for f in files:
            try:
                os.remove(f) 
            except:
                print "file not found: ", f
        
    
    
    
    
      
            

            
