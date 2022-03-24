#import sys
#sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\CycleQueue\\')
# import sys
# import os
# path = os.path.dirname(os.path.dirname(__file__))

# sys.path.append(path+'/CycleQueue/')

from Result import *
from Message import *
from AgentCycle import *
import random
from ResultCycle import *


class DasA_Agent(AgentCycle):
    TYPE_VALUE_MESSAGE = 0
    cycleCountEnd = 0    #结束轮次
    p = 0        #选择概率
    KEY_LOCALCOST = "KEY_LOCALCOST"
    KEY_NCCC="KEY_NCCC"


    def __init__(self,idi,name,level,domain,cycleCountEnd,p):
        super().__init__(idi,name,level,domain)
        DasA_Agent.cycleCountEnd = cycleCountEnd   #迭代次数
        DasA_Agent.p = p   #每次可能选择的概率
        self.nccc = 0
        self.receivedQuantity = 0   #接收信息的次数
        self.cycleCount = 0    #该Agent的迭代次数
        self.neighboursQuantity = 0    #与邻居通信的次数
        self.neighboursValueIndex = {}    #<neighbour 的 Index, neighbourValue 的  Index>
        self.wrong = 0   #出错的次数
        self.wrongNumber = 0
        self.receivedWrongNumber = 0
        self.localCost = 0     #该Agent的代价
    

    def initRun(self):
        super().initRun()
        self.localCost = 2147483647
        self.valueIndex = int(random.random()*len(self.domain))   #随机一个初始值
        self.neighboursValueIndex = {}
        self.neighboursQuantity = len(self.neighbours)

        for i in range(0,len(self.neighbours)):
            self.neighboursValueIndex[i] = 0
        self.sendValueMessages()
    
    def sendValueMessages(self):
        for neighbourIndex in range(0,self.neighboursQuantity):
            msg = Message(self.id,self.neighbours[neighbourIndex],DasA_Agent.TYPE_VALUE_MESSAGE,self.valueIndex)
            self.sendMessage(msg)


    def work(self,i):
        self.wrong = 0
        if i != self.neighboursQuantity:
            self.wrong = 1
            self.wrongNumber = i


    def disposeMessage(self,msg):
        senderIndex = 0
        senderId = msg.getIdSender()
        # print('--------')
        # print(self.name)
        # print(senderId)
        # print(msg.getValue())
        for i in range(0,len(self.neighbours)):
            if self.neighbours[i] == senderId:
                senderIndex = i
                break

        self.neighboursValueIndex[senderIndex] = msg.getValue()
        # print(self.neighbours)
        # print(self.neighboursValueIndex)


    def allMessageDisposed(self):
        #print(self.cycleCount)
        if self.cycleCount >= DasA_Agent.cycleCountEnd:
            self.stopRunning()   
        else:
            self.cycleCount += 1
            self.localCost = self.local()
            if random.random() < DasA_Agent.p:   #随机选择是否改变最小值
                selectMinCost = [0] * len(self.domain)  
                for i in range(0,len(self.domain)):     #设置当前Agent的取值
                    for j in range(0,len(self.neighbours)):     #遍历当前邻居发过来的信息                    
                        selectMinCost[i] += self.constraintCosts[self.neighbours[j]][i][self.neighboursValueIndex[j]]
                selectValueIndex = 0
                selectOneMinCost = selectMinCost[0]
                #寻找此时的最小代价
                for i in range(1,len(self.domain)):
                    if selectOneMinCost > selectMinCost[i] and selectMinCost[i] != self.valueIndex:
                        selectOneMinCost = selectMinCost[i]
                        selectValueIndex = i
                if selectOneMinCost < self.localCost:  #如果小于就更换取值
                    # print('----------------')
                    # print(selectOneMinCost)
                    # print(self.localCost)
                    self.valueIndex = selectValueIndex
                    self.sendValueMessages()   #通知邻居节点当前情况不是最小值的情况
                    
                self.nccc += 1


    def local(self):
        localCostTemp = 0
        
        for i in range(0,len(self.neighbours)):
            #对当前Agent取值时与邻居发过来的信息的代价
            localCostTemp += self.constraintCosts[self.neighbours[i]][self.valueIndex][self.neighboursValueIndex[i]]   #通过矩阵进行代价计算

        return localCostTemp

    def localSearchCheck(self):
        if len(self.msgQueue) == 0:
            print("msgQueue is empty!!!")


    def runFinished(self):
        super().runFinished()
        result = {}
        result[DasA_Agent.KEY_ID] = self.id
        result[DasA_Agent.KEY_NAME] = self.name
        result[DasA_Agent.KEY_LOCALCOST] = self.localCost
        result[DasA_Agent.KEY_NCCC] = self.nccc
        #print(result)

        self.msgMailer.setResult(result)
        




    def printResults(self,results):
        totalCost = 0
        ncccTemp = 0
        for result in results:
            if ncccTemp < result[DasA_Agent.KEY_NCCC]:
                ncccTemp = result[DasA_Agent.KEY_NCCC]
            totalCost += result[DasA_Agent.KEY_LOCALCOST]/2

        print('totalCost: ' + str(totalCost) + '  nccc:' + str(ncccTemp))
        
        ret = ResultCycle()
        ret.nccc = ncccTemp
        ret.totalCost = totalCost

        return ret

    def easyMessageContent(self,msg,sender,receiver):
        s = 'from ' + sender.getName() + 'to ' + receiver.getName + 'type ' + self.messageContent(msg)
        return s

    def messageContent(self,msg):
        if msg.getType() == DasA_Agent.TYPE_VALUE_MESSAGE:
            val = msg.getValue()
            valueIndex = val
            return "value["+str(valueIndex)+"]"

        else:
            return 'unknown'

    def messageLost(self,msg):
        print(self.thread.name+": message lost in agent "+self.name)


        
                


            






