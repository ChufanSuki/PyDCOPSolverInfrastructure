class DFSview:

    def __init__(self,neighbourNodes):
        self.neighbourNodes = neighbourNodes   #无向图（邻接表存储)
        self.childrenNodes = {}      #生成树子节点
        self.parentNode = {}       #生成树父节点
        self.nodeLevel = {}        #节点层次，根节点为0层
        self.nodeIterated = {}      #节点是否遍历过
        self.neighbourCounts = {}    #与邻居节点相连的节点个数
        self.rootId = -1
        self.pseduHeight = 0
        # /*
		#  * 计算每个结点相邻结点的个数
		#  */
        for nodeId in self.neighbourNodes.keys():
            self.childrenNodes[nodeId] = []
            self.nodeIterated[nodeId] = False
            neighbours = self.neighbourNodes[nodeId]
            nodeNeighbourCounts = []

            for i in range(0,len(neighbours)):
                nodeNeighbourCounts.append(len(self.neighbourNodes[neighbours[i]]))

            self.neighbourCounts[nodeId] = nodeNeighbourCounts


    #获取伪树的父节点
    def getPseudoParents(self,nodeId):
        pseudoParents = []
        neightbour = self.neighbourNodes[nodeId]    #获取其所有的邻居结点
        for i in range(0,len(neightbour)):
            pseudo = -1
            parent = self.parentNode[nodeId]
            if parent == neightbour[i]:            #排除直接父亲结点
                continue
            if self.nodeLevel[nodeId] > self.nodeLevel[neightbour[i]]:
                pseudo = neightbour[i]
            if pseudo != -1:
                pseudoParent = 'X' + pseudo
                pseudoParents.append(pseudoParent)

        return pseudoParents

    def getParent(self):
        return 0





