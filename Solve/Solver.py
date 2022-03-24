import sys
sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\DCOPPharse\\')
sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\CycleQueue\\')


from DCOPPharse import *
from graphviz import Graph,Digraph

from CycleQueue import *

import threading

# class Solver:

#     def __init__(self):
#         self.results = []
#         self.resultsRepeated = []
#         self.algorithmType = ''
        
# from dcopplatform import *










if __name__ == '__main__':
    parser=DCOPPharse.ProblemParser('C:/Users/Klaus/Desktop/毕业设计/DCOPSolverOld-master/DCOPSolver/problems/10_3/RandomDCOP_10_10_1.xml', "DFS")
    problem=parser.parse()
    # print(problem.agentNames)
    # print(problem.agentDomains)
    # print(problem.VariableRelation)
    # print(problem.costs)
    
    # g = graph(problem)
    # g.view('C:/Users/Klaus/Desktop/DCOP/Graph/process.gv')
    h = DFSgraph(problem)
    h.view('C:/Users/Klaus/Desktop/DCOP/Graph/DFS.gv')
    agentManagerCycle = AgentManagerCycle(problem,'DPOP',1000,0.4)
    msgMailer = MessageMailerCycle(agentManagerCycle,'DPOP')
    msgMailer.startProcess()
    msgMailer.initWait()   #为避免出现Agent线程开始而Mailer未初始化完成而出现错误
    agentManagerCycle.startAgents(msgMailer)
    msgMailer.join()
    print(msgMailer.re)