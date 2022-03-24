
from Problem import *
from xml.etree import ElementTree as ET
from ParserGeneral import *
from TreeGenerator import * 
from DFSgeneration import *
from MostConnectedHeuristic import *
from PriorityGeneration import *
from graphviz import Graph,Digraph


class ProblemParser:
    PRESENTATION="presentation"
    FORMAT="format"
    TYPE="type"

    FORMAT_DISCHOCO="XDisCSP 1.0"
    FORMAT_FRODO="XCSP 2.1_FRODO"

    TYPE_DCOP="DCOP"
    TYPE_GRAPH_COLORING="DisCSP"

    def __init__(self,xmlPath,treeGeneratorType):
        self.xmlPath = xmlPath
        self.treeGeneratorType = treeGeneratorType
        self.problemBenchmark = None
        self.problemFormat = None
        self.problemType = None
        self.treeGeneratorType = None
        self.root = None
        self.graph = None


    def parse(self):
        problem = Problem()
        
        tree = ET.parse(self.xmlPath)
        root = tree.getroot()
        if self.parsePresentation(root.find('presentation')) == False:
            print("parsePresentation()=false")
            return None

        parser = None
        parser = ParserGeneral(root, 'DCOP')
        if parser != None:
            parser.parseContent(problem)    #解析problem里面的内容
            self.generateCommunicationStructure(problem)   #生成DFS通信结构
            return problem
        else:
            return None


    def generateCommunicationStructure(self,problem):
        treeGenerator = None
        #采取DFS伪树通信结构
        treeGenerator = DFSgeneration(problem.neighbourAgents)
        # print(treeGenerator.dfsview.neighbourCounts)
        # print("\n")
        DFSgeneration.setRootHeuristics(MostConnectedHeuristic(problem))
        DFSgeneration.setNextNodeHeuristics(MostConnectedHeuristic(problem))
        treeGenerator.generate() #生成DFS通信结构


        problem.agentLevels=treeGenerator.getLevels()

        for level in problem.agentLevels.values():
            if problem.treeDepth<(level+1):
               problem.treeDepth=level+1
        problem.pseudoHeight=treeGenerator.getHeight()
        problem.parentAgents=treeGenerator.getParents()
        problem.childAgents=treeGenerator.getChildren()
        problem.allParentAgents=treeGenerator.getAllParents()    #这里的allParaent表示的是该给点的所有父节点
        problem.allChildrenAgents=treeGenerator.getAllChildren()   #这里的allChildren表示的是该给点的所有子节点
        # print('------')
        # print(problem.parentAgents)
        # print(problem.allParentAgents)
        # print('-----')


        




    def parsePresentation(self,element):
        if element == None:
            return False

        else:
            return True

def graph(problem):
    dot = Graph('G',strict = True,filename='C:\\Users\\Klaus\\Desktop\\DCOP\\Graph\\process.gv',format='png')
    #print(problem.VariableRelation.keys())
    for i in problem.VariableRelation.keys():
        
            j = problem.VariableRelation[i]
            test = j.split(' ')
            #print(i)
            #print(test)
            dot.edge(test[0],test[1],str(i))
    return dot

def DFSgraph(problem):
    dot = Graph('G',strict = True,filename='C:\\Users\\Klaus\\Desktop\\DCOP\\Graph\\DFS.gv',format='png')
    # print(problem.parentAgents)
    # print(problem.neighbourAgents)
    data = []
    for i in problem.parentAgents.keys():
        j = problem.parentAgents[i]
        if j == -1:
            continue
        dot.edge(str(j),str(i),_attributes={'color':'red'})   #_attributes={'color'='red'}
        data.append((i,j))
        data.append((j,i))
    for i in problem.neighbourAgents.keys():
        k = problem.neighbourAgents[i]
        for j in k:
            if (i,j) not in data and (j,i) not in data:
                dot.edge(str(j),str(i),_attributes={'style':'dashed'})
                data.append((i,j))
                data.append((j,i))
    return dot



if __name__ == '__main__':
    parser=ProblemParser('C:\\Users\\Klaus\\Desktop\\DCOP\\problem\\1_5_50\\RandomDCOP_5_3_1.xml', "DFS")
    problem=parser.parse()
    print(problem.neighbourAgents)
    print(problem.agentDomains)
    print(problem.VariableRelation)
    print(problem.costs)
    print('\n'*5)
    print('对{}问题的关键信息解析如下：'.format('RandomDCOP_5_3_1.xml'))
    print('Agent:{}'.format(problem.agentNames))
    print('domians:{}'.format(problem.domains))
    print('agentDomains:{}'.format(problem.agentDomains))
    print('VariableRelation:{}'.format(problem.VariableRelation))
    print('neighbourAgents:{}'.format(problem.neighbourAgents))
    print('parentAgents:{}'.format(problem.parentAgents))
    print('childAgents:{}'.format(problem.childAgents))
    print('allParentAgents:{}'.format(problem.allParentAgents))
    print('allChildrenAgents:{}'.format(problem.allChildrenAgents))
    print('costs:{}'.format(problem.costs))
    print('\n'*5)
    print(problem.childAgents)
    # g = graph(problem)
    # g.view('C:\\Users\\Klaus\\Desktop\\DCOP\\Graph\\process.gv')
    # h = DFSgraph(problem)
    # h.view('C:\\Users\\Klaus\\Desktop\\DCOP\\Graph\\DFS.gv')
   
    
    #### PriorityGeneration 
       


    

