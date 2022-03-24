from Problem import *
from DFSview import *
from ScoringHeuristic import ScoringHeuristic
from PriorityView import *


#主要是为了获取问题本身结点之间的约束关系

class MostConnectedHeuristic(ScoringHeuristic):
    def __init__(self,problem):  
        super().__init__()
        self.problem = problem


    def getScores(self):
        maxNeighbourCount = -1
        maxNeighbourCountNodeId = -1
        #
		#寻找邻居结点最多的结点ID
		#
        for nodeId in self.problem.neighbourAgents.keys():
            temp = len(self.problem.neighbourAgents[nodeId])
            if temp >= maxNeighbourCount:
                maxNeighbourCount = temp
                maxNeighbourCountNodeId = nodeId
        return maxNeighbourCountNodeId

    '''
    下一个结点的选择是以连接边最多的为准
    '''
    def getScores_two(self,nodeId,dfsview):  #返回没有被遍历以及邻居节点最多的点
        neighbours = dfsview.neighbourNodes[nodeId]
        # print(dfsview.neighbourNodes)
        # print(dfsview.neighbourCounts)
        # print("-----")
        counts = dfsview.neighbourCounts[nodeId]   #与nodeId相连的节点的邻居个数
        for i in range(0,len(counts)):
            if dfsview.nodeIterated[neighbours[i]] == True:   #查看该节点是否被遍历过,被遍历的置于-1
                counts[i] = -1

        maxIndex = counts.index(max(counts))
        if counts[maxIndex] == -1:
            return -1
        else:
            return neighbours[maxIndex]

    def getScores_three(self,orderingView):
        maxNeighbourCount=-1
        maxNeighbourCountNodeId=-1
        # /*
		#  * 寻找邻居结点最多的结点ID
		#  */
        for nodeId in self.problem.neighbourAgents.keys():
            temp = len(self.problem.neighbourAgents[nodeId])
            if orderingView.nodeIterated[nodeId] == True:
                continue
            if temp >= maxNeighbourCount:
                maxNeighbourCount=temp
                maxNeighbourCountNodeId=nodeId

        return maxNeighbourCountNodeId




    
