'''
Created on Jun 16, 2013

@author: mrfish
'''

import math
import numpy


class Colour():
    def __init__(self, numberOfStates):
        self.colours = []
        for i in range(0, numberOfStates):
            self.colours.append(self.spectrum(i/(numberOfStates-1.0)))
        
    def spectrum(self, w):
        if w>1:
            w=1
        if w<0:
            w=0
        
        w = w*(645-380) + 380
        if (w >= 380 and w < 440):
            R = -(w - 440.) / (440. - 350.)
            G = 0.0
            B = 1.0

        elif (w >= 440 and w < 490):
            R = 0.0
            G = (w - 440.) / (490. - 440.)
            B = 1.0
        
        elif (w >= 490 and w < 510):
            R = 0.0
            G = 1.0
            B = (510-w) / (510. - 490.)
        
        elif (w >= 510 and w < 580):
            R = (w - 510.) / (580. - 510.)
            G = 1.0
            B = 0.0
            
        elif (w >= 580 and w < 645):
            R = 1.0
            G = -(w - 645.) / (645. - 580.)
            B = 0.0
        
        elif (w >= 645 and w <= 780):
            R = 1.0
            G = 0.0
            B = 0.0
        
        else:
            R = 0.0
            G = 0.0
            B = 0.0
        
        R = int(R * 255.0)
        G = int(G * 255.0)
        B = int(B * 255.0)
        return [R,G,B] 

        
 #   def __init__self, noOfStates::
 #       angles = numpy.linspace0, 2*math.pi, noOfStates:
 #       Y=0.5
 #       self.colourList=[]
 #       
 #       for angle in angles:
 #           U=math.cosangle:
 #           V=math.sinangle:
 #           
 #           R=Y+V/0.88
 #           G=Y-0.38*U-0.58*V
 #           B=Y+U/0.49
 #           
 #           self.colourList.append[R,G,B]:
 
    def _convertToRGB(self, RGB):
        # "#0x" + str(bytearray(RGB)).encode('hex')
        return "#" + str(bytearray(RGB)).encode('hex')    
            
            
    def getColourForState(self,stateRepresentation):
        return self._convertToRGB(self.colours[stateRepresentation])


if __name__ == '__main__':
    numberOfStates = 5
    myColour = Colour(numberOfStates)
    print myColour.colours
    color = myColour.getColourForState(3)
    print color
