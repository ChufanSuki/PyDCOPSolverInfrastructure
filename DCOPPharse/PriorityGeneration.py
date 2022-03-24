from ScoringHeuristic import *
from TreeGenerator import *
from PriorityView import *

class PriorityGeneration:
    orderingView = None
    priorityBegin = None
    rootElectionHeuristic = None
    NextNodeHeuristics = None

    def __init__(self,neighbourNodes):
        PriorityGeneration.orderingView = PriorityView(neighbourNodes)
        PriorityGeneration.priorityBegin = 1

    def generate(self):
        iteratedCount = 0
        PriorityGeneration.orderingView.maxPriority = PriorityGeneration.rootElectionHeuristic.getScores()
        curNodeId = PriorityGeneration.orderingView.maxPriority
        PriorityGeneration.orderingView.nodeIterated[curNodeId] = True
        PriorityGeneration.orderingView.priority[curNodeId] = PriorityGeneration.priorityBegin
        PriorityGeneration.priorityBegin = PriorityGeneration.priorityBegin + 1
        iteratedCount = iteratedCount + 1
        totalCount = len(PriorityGeneration.orderingView.neighbourNodes)

        #优先级生成
        while iteratedCount<totalCount:
            nextNodeId = PriorityGeneration.NextNodeHeuristics.getScores_three(PriorityGeneration.orderingView)
            PriorityGeneration.orderingView.nodeIterated[nextNodeId] = True
            PriorityGeneration.orderingView.priority[nextNodeId] = PriorityGeneration.priorityBegin
            PriorityGeneration.priorityBegin = PriorityGeneration.priorityBegin + 1

            if iteratedCount == totalCount - 1:
                PriorityGeneration.orderingView.minPriority = nextNodeId
            iteratedCount = iteratedCount + 1

        #结点高优先级结点与低优先级结点
        for nodeId in PriorityGeneration.orderingView.neighbourNodes.keys():
            neighbours = PriorityGeneration.orderingView.neighbourNodes[nodeId]

            for Node in neighbours:
                if PriorityGeneration.orderingView.priority[nodeId] > PriorityGeneration.orderingView.priority[Node]:
                    PriorityGeneration.orderingView.highNodes[nodeId].append(Node)
                else:
                    PriorityGeneration.orderingView.lowNodes[nodeId].append(Node)


    def generate_tree(self,treeGenerator):
        PriorityGeneration.orderingView.maxPriority = treeGenerator.getRoot()
        curNodeId = PriorityGeneration.orderingView.maxPriority
        lis = Queue()
        lis.put(curNodeId)
        while lis.empty == False:
            curNodeId = lis.get()
            PriorityGeneration.orderingView.priority[curNodeId] = treeGenerator.getLevels()[curNodeId]+1
            low = treeGenerator.getAllChildren()[curNodeId]
            high = treeGenerator.getAllParents()[curNodeId]

            for i in range(0,len(low)):
                PriorityGeneration.orderingView.lowNodes[curNodeId].append(low[i])

            for i in range(0,len(high)): 
                PriorityGeneration.orderingView.highNodes[curNodeId].append(high[i])

            for child in treeGenerator.getChildren()[curNodeId]:
                lis.put(child)
            if lis.empty and len(treeGenerator.getChildren()[curNodeId]) == 0:
                PriorityGeneration.orderingView.minPriority = curNodeId


    def setRootHeuristics(self,rootHeuristic):
        PriorityGeneration.rootElectionHeuristic = rootHeuristic

    def setNextNodeHeuristics(self,nextNodeHeuristics):
        PriorityGeneration.NextNodeHeuristics = nextNodeHeuristics

    def getHighNodes(self):
        return PriorityGeneration.orderingView.highNodes

    def getLowNodes(self):
        return PriorityGeneration.orderingView.lowNodes

    def getPriorities(self):
        return PriorityGeneration.orderingView.priority

    def getMaxPriority(self):
        return PriorityGeneration.orderingView.maxPriority

    def getMinPriority(self):
        return PriorityGeneration.orderingView.minPriority

    def getAllNodes(self):
        return PriorityGeneration.orderingView.allNodes


        