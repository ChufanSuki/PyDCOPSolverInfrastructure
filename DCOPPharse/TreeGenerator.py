from abc import abstractmethod, ABCMeta

class TreeGenerator():
    __metaclass__ = ABCMeta

    def __init__(self,neighbors):
        self.TREE_GENERATOR_TYPE_DFS = "DFS"
        self.TREE_GENERATOR_TYPE_BFS = "BFS"
        self.neighbors = neighbors #无向图（邻接表存储）
        self.parents = {} #父节点
        self.allParents = {} #父节点和伪父节点
        self.children = {} #子节点
        self.allChildren = {} #子节点和伪子节点
        self.levels = {} #节点层次，根节点为0层
        self.height = 0
        self.rootId = -1
        self.nodeIterated = []

        for nodeId in self.neighbors.keys():
            self.allParents[nodeId] = []
            self.children[nodeId] = []
            self.allChildren[nodeId] = []
        


    # /**
	#  * 获取邻接表
	#  * @return
	#  */
    def getNeighbors(self):
        return self.neighbors


    # /**
	#  * 获取根节点
	#  * @return
	#  */
    def getRoot(self):
        return self.rootId


    # /**
	#  * 初始化根节点，在generate()之前调用
	#  * @
    def initRoot(self,root):
        self.rootId = root
    

    # /**
	#  * 构造生成树
	#  */
    @abstractmethod
    def generate(self):
        pass


    #     /**
	#  * 获取父节点
	#  * @return
	#  */
    def getParents(self):
        return self.parents


    # /**
	#  * 获取父节点和伪父节点
	#  * @return
	#  */
    def getAllParents(self):
        return self.allParents


    # /**
	#  * 获取子节点
	#  * @return
	#  */
    def getChildren(self):
        return self.children


    # /**
	#  * 获取子节点和伪子节点
	#  * @return
	#  */
    def getAllChildren(self):
        return self.allChildren


    # /**
	#  * 获取层次
	#  * @return
	#  */
    def getLevels(self):
        return self.levels


    # /**
	#  * 获取高度
	#  * @return
	#  */
    def getHeight(self):
        return self.height


    # /**
	#  * 从nodesArr中选择度数最高的节点;
	#  * 如果nodesArr中的节点均已遍历过，返回-1；
	#  * @param nodeId
	#  * @return
	#  */
    def getMaxNeighborsNodeId(self,nodesArr):
        if nodesArr == None:
            return -1

        maxDegreeNodeId = -1
        maxDegree = -1
        for nodeId in nodesArr:
            if nodeId not in self.nodeIterated:
                if maxDegree < len(self.neighbors[nodeId]):
                    maxDegree = len(self.neighbors[nodeId])
                    maxDegreeNodeId = nodeId


        return maxDegreeNodeId

    # /**
	#  * 从nodesSet中选择度数最高的节点;
	#  * 如果nodesSet中的节点均已遍历过，返回null；
	#  * @param nodeId
	#  * @return
	#  */
    def getMaxNeighborsNodeId(self,nodesSet):
        if nodesSet == None:
            return -1

        maxDegreeNodeId = -1
        maxDegree = -1
        for nodeId in nodesSet:
            if nodeId not in self.nodeIterated:
                if maxDegree < len(self.neighbors[nodeId]):
                    maxDegree = len(self.neighbors[nodeId])
                    maxDegreeNodeId = nodeId


        return maxDegreeNodeId

    # /**
	#  * 从nodesArr中选择度数最低的节点;
	#  * 如果nodesArr中的节点均已遍历过，返回-1;
	#  * @param nodeId
	#  * @return
	#  */
    def getMinNeighborsNodeId(self,nodesArr):
        if nodesArr == None:
            return -1

        minDegreeNodeId = -1
        minDegree = 10000000000
        for nodeId in nodesArr: 
            if nodeId not in self.nodeIterated:
                if minDegree > len(self.neighbors[nodeId]):
                    minDegree = len(self.neighbors[nodeId])
                    minDegreeNodeId = nodeId


        return minDegreeNodeId

    # /**
	#  * 从nodesSet中选择度数最低的节点;
	#  * 如果nodesSet中的节点均已遍历过，返回-1;
	#  * @param nodeId
	#  * @return
	#  */
    def getMinNeighborsNodeId(self,nodesSet):
        if nodesSet == None:
            return -1
        minDegreeNodeId = -1
        minDegree = 10000000000
        for nodeId in nodesSet: 
            if nodeId not in self.nodeIterated:
                if minDegree > len(self.neighbors[nodeId]):
                    minDegree = len(self.neighbors[nodeId])
                    minDegreeNodeId = nodeId


        return minDegreeNodeId
    
	#   从nodeId的邻居节点中随机选择一个节点；
	#   如果nodesArr中的节点均已遍历过，返回-1;
	#   @param nodeId
	#   @return
	#  /
    def getRandomNodeId(self,nodesArr):
        if nodesArr == None:
            return -1
        for i in range(0,len(nodesArr)):
            if nodeId not in self.nodeIterated:
                return nodesArr[i]

        return -1


   