import cProfile
import re



import Environment.RepresentationEnvironment.RepresentationEnvironment_ContinuousMsgFromJavaServer as RepresentationEnvironment 

NUMBER_OF_ACTIONS = 4        #n,s,e,w
DIMENSION = ( 16,16, 16, 16*2 )

def main():
    environmRepMyAgent1 = RepresentationEnvironment.RepresentationEnvironment_ContinuousMsgFromJavaServer(NUMBER_OF_ACTIONS, DIMENSION, None)
    print "End"

cProfile.run("main()",  'myrestats')        