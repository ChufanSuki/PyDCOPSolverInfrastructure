

class PriorityView:

    def __init__(self,neighbourNodes):
        self.neighbourNodes = neighbourNodes #无向图（邻接表存储）
        self.highNodes = {} #生成高优先级结点
        self.lowNodes = {}  #生成低优先级结点
        self.priority = {}  #每个结点的优先级
        self.nodeIterated = {} #节点是否遍历过
        self.neighbourCounts = {}
        self.allNodes = []
        self.maxPriority=-1
        self.minPriority=-1


        for nodeId in self.neighbourNodes.keys():
            self.highNodes[nodeId] = []
            self.lowNodes[nodeId] = []
            self.nodeIterated[nodeId] = False

            neighbours = self.neighbourNodes[nodeId]
            nodeNeighbourCounts = [0]*len(neighbours)

            for i in range(0,len(nodeNeighbourCounts)):
                nodeNeighbourCounts[i] = len(self.neighbourNodes[neighbours[i]])

            self.neighbourCounts[nodeId] = nodeNeighbourCounts

        self.getAllNodes()


    def getAllNodes(self):
        for nodeId in self.neighbourNodes.keys():
            self.allNodes.append(nodeId)
