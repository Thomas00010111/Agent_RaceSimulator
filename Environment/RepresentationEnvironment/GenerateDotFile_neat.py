'''
Created on Jun 18, 2013

@author: mrfish


Kommentar fuer mich:

Schreiben von GraphVic File und geenerieren der State Darastellung auseinandergezogen.
Noch nicht getestet!!

Es kam zum Abbruch der Komunikation bei Afrug der Stategenerierung ("neato"). Weiss nicht warum, wahrscheinlich timeout.
Denke es ist besser das Schreiben des Vic Files und generieren der graphischen Darstellung auseinander zu ziehen
und dann bei Bedarf demn Graphjen zu generieren.

Muss noch getestet werden!!  

'''

import os
import pickle

import Colour


StatesPerRow = 7   # number of lines

def getPosForState(stateRepresentation):
    xpos = stateRepresentation/StatesPerRow * 100
    ypos = stateRepresentation%StatesPerRow * 100
    return str(xpos)+","+str(ypos)

def drawStateDiagram(extendedMatrix, rl, path):
    generateGraphvicFile(extendedMatrix, rl, path)
    generateGraph(path)
    

def generateGraphvicFile(extendedMatrix, rl, path):
    graphvicFile = open(path + "graph.tmp", 'wb', 0)
    noOfStates = extendedMatrix.getNumberOfStates()
    myColors = Colour.Colour(noOfStates)
    graphvic = []
    graphvic.append("digraph G {")
    graphvic.append("fixedsize=true; \nratio=fill; \noverlap=false; \nsize=\"100,100\";")
    graphvic.append("node [fontsize=80, style=rounded,width=4, height=4];")
    
    for n in range(0,noOfStates):
        graphvic.append(str(n) + " [style=filled, fillcolor=\"" + myColors.getColourForState(n) + "\", pos=\"" + getPosForState(n) + "\"];")
         
    #graph = pydot.Dot(graph_type='digraph', size="100,100", ratio="fill", overlap="false", fixedsize="true")
#        node = pydot.Node("node", fontsize="80", style="rounded", width="5", height="5")
#        graph.add_node(node)

    for item in graphvic:
        graphvicFile.write("%s\n" % item)
    
    for stateRepresentation, n in enumerate(extendedMatrix.transitionMatrices):
        print "stateRepresentation: ", stateRepresentation, "     n: ", n._probabilityMatrix
    
        for action, row in enumerate(n.getProbabilityMatrixAsList()):
            #print "action: ", action, "     row: ", row
            for nextState, probability in enumerate(row):
                #print "nextState: ", nextState, "    probability:", probability                    
                if probability > 0.0:            
                        arrowWidth = str(probability*10.0)
                        if rl.getRewardedTransitions(stateRepresentation, nextState) > 0:
                            graphicFileRow = str(stateRepresentation) + " -> " + str(nextState) + " [  penwidth=\"" + arrowWidth + "\" , label=\"***" + str(action) + "/" + str("%.2f" % probability) + "***\", ranksep=\"3.0\", nodesep=\"2.0\", color=\"" + myColors.getColourForState(stateRepresentation) + "\"]"                      
                        else:    
                            graphicFileRow = str(stateRepresentation) + " -> " + str(nextState) + " [  penwidth=\"" + arrowWidth + "\" , label=\"" + str(action) + "/" + str("%.2f" % probability) + "\", ranksep=\"3.0\", nodesep=\"2.0\", color=\"" + myColors.getColourForState(stateRepresentation) + "\"]"
                        print graphicFileRow 
                        graphvicFile.write("%s\n" % graphicFileRow)
                    
                    #graphvic.append(graphicFileRow)
                    #edge = pydot.Edge(str(stateRepresentation), str(nextState), label=(str(action) + "/" + str("%.2f" % probability)), ranksep="3.0", nodesep="2.0", color="green" )
                    #graph.add_edge(edge)
    graphvicFile.write("}")
    #calling graph.write_png('graph.png') gives an exception
    #graph.write('graph.tmp', format="raw")
    #graphvic.append("}")
#        graphvicFile = open("graph.tmp", 'wb')
#        for item in graphvic:
#            graphvicFile.write("%s\n" % item)
    graphvicFile.close()
    #It seems that calling the command line function here gives exception:
    #'NoneType' object has no attribute 'Edge'
    #filename = "transition_graph.png"

#     pathTmp = path + "graph.tmp"
#     outputFile = " -o" + path + "transition_graph.png"
#     outputFile = pathTmp + outputFile
#     #print "Please wait, generating ",  outputFile
#     #os.system("neato -n2 -Tpng %s" % outputFile)
#     print "Graph saved in ", path, " transition_graph.png" 
    
def generateGraph(path):
    pathTmp = path + "graph.tmp"
    outputFile = " -o" + path + "transition_graph.png"
    outputFile = pathTmp + outputFile
    print "Please wait, generating ",  outputFile
    os.system("neato -n2 -Tpng %s" % outputFile)   
    print "Graph saved in ", path, " transition_graph.png" 
    

def test():
    path = "test2/simpleAgent"
    #ex = ExtendedDiscreteTransitionMatrix.ExtendedDiscreteTransitionMatrix(74,8,fileName=path, loadFromFile=True)
    f_probabilityMatrix = open(path + "_probabilityMatrix", 'r')
    ex = pickle.load(f_probabilityMatrix)
    f_probabilityMatrix.close()
        
    f_RL = open(path + "_RL", 'r')
    rl = pickle.load(f_RL)
    generateGraphvicFile(ex, rl, path)

    
if __name__ == '__main__':
    path = "test2/simpleAgent"
    generateGraph(path)

    
    