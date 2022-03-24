from abc import abstractmethod, ABCMeta
from Message import *
from AgentCycleQueueMessager import *
import time


class AgentCycle(AgentCycleQueueMessager):
    __metaclass__ = ABCMeta
    totalHeight = 0   #每个Agent维持一个树高的值，为根到叶子的距离，也就是叶子的level值
    KEY_ID = "KEY_ID"
    KEY_NAME = "KEY_NAME"
    KEY_VALUE = "KEY_VALUE"


    def __init__(self,idi,name,level,domain):
        super().__init__('Agent '+ name)
        self.id = idi
        self.level = level    #Agent的等级，也就是距离root的距离，根节点的值为0
        self.name = name
        self.domain = domain
        

        self.neighbours = []
        self.parent = []
        self.allParents = []
        self.pseudoParents = []
        self.allChildren = []
        self.children = []
        self.pseudoChildren = []

        # ACO算法优先级时用到的属性
        self.highPriorities = []
        self.lowPriorities = []
        self.priority = 0
        self.allNodes = []
        self.maxPriority = 0
        self.minPriority = 0
        self.neighbourDomains = {}
        self.neighbourLevels = {}
        self.constraintCosts = {}

        self.msgMailer = None
        self.valueIndex = 0
        self.localCost = 0

    def getId(self):
        return self.id

    def getName(self):
        return self.name
    
    def getValue(self):
        return self.domain[self.valueIndex]

    def getLocalCost(self):
        return self.localCost

    def excepttest(self,arrA,arrB):
        if arrA == None or arrB == None:
            return None
        exceptList = []
        for i in range(len(arrA)):
            try:
                test = arrB.index(arrA[i])
            except:
                exceptList.append(arrA[i])

        if len(exceptList) == 0:
            return None
        else:
            return exceptList



    def setNeibours(self,neighbours,parent,children,allParents,allChildren,neighbourDomains,constraintCosts,neighbourLevels):
        self.neighbours = neighbours
        self.parent = parent
        self.children = children
        self.allParents = allParents
        self.allChildren = allChildren
        if self.allChildren != None and self.children !=None:
            self.pseudoChildren = self.excepttest(self.allChildren,self.children)   #得到伪树中伪孩子。
        
        if self.allParents != None and self.parent != -1:
            t = []
            t.append(self.parent)
            self.pseudoParents = self.excepttest(self.allParents,t)    #得到伪树中的伪父母

        self.neighbourDomains = neighbourDomains
        self.constraintCosts = constraintCosts
        self.neighbourLevels = neighbourLevels


    def setMessageMailer(self,msgMailer):
        self.msgMailer = msgMailer

    def sendMessage(self,msg):
        self.msgMailer.addMessage(msg)

    def initRun(self):
        super().initRun()
        time.sleep(0.1)

    @abstractmethod
    def printResults(self,results):
        pass

    @abstractmethod
    def easyMessageContent(self,msg,sender,receiver):
        pass

    def isLeafAgent(self):
        return self.children == None or len(self.children) == 0

    def isRootAgent(self):
        return self.parent==-1




    
