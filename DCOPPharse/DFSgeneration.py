from TreeGenerator import *
from DFSview import * 
from ScoringHeuristic import *

class DFSgeneration(TreeGenerator):


    #/** The heuristic used to choose the root */
    rootElectionHeuristic = None
    #/** The heuristic used to choose the next node */
    NextNodeHeuristics = None
    dfsview = None

    # 
	#  neighbourNodes 	表示结点的邻接存储关系
	#  为根结点选择策略
	# 
	#   
	#  
    def __init__(self,neighbourNodes):
        super().__init__(neighbourNodes)
        DFSgeneration.dfsview = DFSview(neighbourNodes)



    ##DFS产生算法
    def generate(self):
        iteratedCount = 0
        curLevel = 0
        DFSgeneration.dfsview.rootId = DFSgeneration.rootElectionHeuristic.getScores()   #寻找邻居节点最多的节点
        DFSgeneration.rootId = DFSgeneration.dfsview.rootId    #根节点
        curNodeId = DFSgeneration.dfsview.rootId
        DFSgeneration.dfsview.nodeIterated[curNodeId] = True   #记录当前点是否被遍历过
        iteratedCount = iteratedCount + 1    #记录遍历点的个数
        DFSgeneration.dfsview.parentNode[curNodeId] = -1    #-1表示当前点是根节点
        DFSgeneration.dfsview.nodeLevel[curNodeId] = curLevel    #记录该点的等级，也就是层次（树高）

        totalCount = len(DFSgeneration.dfsview.neighbourNodes)   #总的点的个数
        while iteratedCount < totalCount:    #判断是否遍历完所有的点
            nextNodeId = DFSgeneration.NextNodeHeuristics.getScores_two(curNodeId, self.dfsview); #下一个结点的选择是以连接边最多的为准
            if nextNodeId == -1:    #选择的下一个节点是已经被遍历过的
                curLevel = curLevel - 1    #层级数减一回到上一层
                #回溯
                curNodeId = DFSgeneration.dfsview.parentNode[curNodeId]
            else:
                curLevel = curLevel + 1   #层数加一
                DFSgeneration.dfsview.childrenNodes[curNodeId].append(nextNodeId)  #记录当前选择的孩子，并加入childrenNodes字典
                DFSgeneration.dfsview.parentNode[nextNodeId] = curNodeId   #加入parentNode字典

                DFSgeneration.dfsview.nodeIterated[nextNodeId] = True
                DFSgeneration.dfsview.nodeLevel[nextNodeId] = curLevel
                iteratedCount = iteratedCount + 1
                curNodeId = nextNodeId
        # print(DFSgeneration.dfsview.parentNode)
        # print(DFSgeneration.dfsview.childrenNodes)
        self.calAllChildrenAndParentNodes()  #记录正对于伪树来说一个节点的所有父母
        self.calHeight()     #计算伪树的高度
        #print(self.allChildren)
        
        # print(self.allChildren)
        # print(self.allParents)
        
        


    """
    选择根结点策略
    """
    @staticmethod
    def setRootHeuristics(rootHeuristic):
        DFSgeneration.rootElectionHeuristic = rootHeuristic

    """
    选择叶子结点策略
    """
    @staticmethod
    def setNextNodeHeuristics(nextNodeHeuristics):
        DFSgeneration.NextNodeHeuristics = nextNodeHeuristics

    def getChildren(self):
        return DFSgeneration.dfsview.childrenNodes

    def getParents(self):
        return DFSgeneration.dfsview.parentNode

    def calHeight(self):
        curNodeId = DFSgeneration.dfsview.rootId
        link = True
        while link == True and curNodeId != -1:
            if len(DFSgeneration.dfsview.childrenNodes[curNodeId]) > 1:
                link = False
            else:
                DFSgeneration.dfsview.pseduHeight = DFSgeneration.dfsview.pseduHeight + 1
                g = (i for i in DFSgeneration.dfsview.childrenNodes[curNodeId])
                if len(DFSgeneration.dfsview.childrenNodes[curNodeId]) == 1:
                    curNodeId = next(g)
                if len(DFSgeneration.dfsview.childrenNodes[curNodeId]) == 0:
                    break

        self.height = self.dfsview.pseduHeight


    def getLevels(self):
        return DFSgeneration.dfsview.nodeLevel

    def calAllChildrenAndParentNodes(self):
        for nodeId in DFSgeneration.dfsview.neighbourNodes.keys():
            neighbours = DFSgeneration.dfsview.neighbourNodes[nodeId]
            children = DFSgeneration.dfsview.childrenNodes[nodeId]
            parent = DFSgeneration.dfsview.parentNode[nodeId]
            level = DFSgeneration.dfsview.nodeLevel[nodeId]
            if parent == -1:
                #根节点
                allChildrenList = []
                for i in range(0,len(neighbours)):
                    allChildrenList.append(neighbours[i])

                self.allParents[nodeId] = []
                self.allChildren[nodeId] = allChildrenList
            elif len(children) == 0:
                #叶节点
                allParentList = []
                for i in range(0,len(neighbours)):
                    allParentList.append(neighbours[i])
                self.allParents[nodeId] = allParentList
                self.allChildren[nodeId] = [] 
            else:
                #中间节点
                allParentList = []
                allChildrenList = []
                for i in range(0,len(neighbours)):
                    if neighbours[i] == parent:
                        allParentList.append(neighbours[i])
                    elif neighbours[i] in children:
                        allChildrenList.append(neighbours[i])
                    else:
                        if level < DFSgeneration.dfsview.nodeLevel[neighbours[i]]:
                            #在本节点之下
                            allChildrenList.append(neighbours[i])
                        else:
                            #在本节点之上
                            allParentList.append(neighbours[i])
                self.allParents[nodeId] = allParentList
                self.allChildren[nodeId] = allChildrenList
            # print('---------')
            # print(neighbours)
            # print(DFSgeneration.dfsview.childrenNodes)
            # print(children)
            # print(parent)
            # print(self.allParents)
            # print(self.allChildren)
            # print('---------')
            



    def indexOf(self,test,value):
        for i in range(0,len(test)):
            if test[i] == value:
                return i
            
        return -1

  



