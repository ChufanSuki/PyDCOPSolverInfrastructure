# import sys
# sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\CycleQueue\\')

from Result import *
from Message import *
from AgentCycle import *
import random
from ResultCycle import *
from MultiDimensionData import *
from Dimension import *
from ReductDimensionResult import *
from ResultDPOP import *
import sys


class DPOPAgent(AgentCycle):

    TYPE_VALUE_MESSAGE = 0
    TYPE_UTIL_MESSAGE = 1
    KEY_TOTAL_COST = "KEY_TOTAL_COST"
    KEY_UTIL_MESSAGE_SIZES = "KEY_UTIL_MESSAGE_SIZES"
    
    def __init__(self,idi,name,level,domain):
        super().__init__(idi,name,level,domain)
        self.parentLevels = []
        self.disposedChildrenCount = 0
        self.reductDimensionResultIndexes = []
        self.rawMDData = None
        self.dimensions = []
        self.utilMsgSizes = []
        self.totalCost = 0
        self.nccc = 0

    def initRun(self):
        super().initRun()
        self.parentLevels = [0]*len(self.allParents)
        
        for i in range(0,len(self.allParents)):
            self.parentLevels[i] = self.neighbourLevels[self.allParents[i]]
        if self.isRootAgent() == False:
            self.rawMDData = self.computeLocalUtils()
        if self.isLeafAgent() == True:
            result = self.rawMDData.reductDimension(str(self.id)+'',ReductDimensionResult.REDUCT_DIMENSION_WITH_MIN)
            self.rawMDData=result.getMdData()
            self.dimensions=self.rawMDData.getDimensions()
            self.reductDimensionResultIndexes=result.getResultIndex()
            self.sendUtilMessage(self.rawMDData)

    def runFinished(self):
        super().runFinished()
        result = {}
        result[DPOPAgent.KEY_ID] = self.id
        result[DPOPAgent.KEY_NAME] = self.name
        result[DPOPAgent.KEY_VALUE] = self.domain[self.valueIndex]
        result['NCCCs'] = self.nccc
        if self.isRootAgent() == True:
            result[DPOPAgent.KEY_TOTAL_COST] = self.totalCost
        result[DPOPAgent.KEY_UTIL_MESSAGE_SIZES] = self.utilMsgSizes
        self.msgMailer.setResult(result)
        print("Agent "+self.name+" stopped!")

    def printResults(self,results):
        totalCost = -1
        result = None
        sizeList = []
        nccc = 0
        for i in range(0,len(results)):
            result=results[i]
            id_ = int(result[DPOPAgent.KEY_ID])
            name_ = str(result[DPOPAgent.KEY_NAME])
            value_ = int(result[DPOPAgent.KEY_VALUE])
            if DPOPAgent.KEY_TOTAL_COST in result.keys():
                totalCost = int(result[DPOPAgent.KEY_TOTAL_COST])
            nccc += result['NCCCs']
            sizeList = sizeList + list(result[DPOPAgent.KEY_UTIL_MESSAGE_SIZES])
            displayStr="Agent "+name_+": id="+str(id_)+" value="+str(value_)
            #print(result[DPOPAgent.KEY_UTIL_MESSAGE_SIZES])
          
        sizeArr = sizeList
        total = 0
        for i in sizeArr:
            total += i
        minMaxAvg = self.minMaxAvg(sizeArr)
        #print(minMaxAvg)
        print('totalCost:'+str(totalCost))
        print('utilMsgCount:'+str(len(sizeArr))+' utilMsgSizeMin:'+str(minMaxAvg[0])+ 'byte ' +' utilMsgSizeMax:'+str(minMaxAvg[2])+ 'byte' +' utilMsgSizeAvg:'+str(minMaxAvg[4]) +'byte'+ ' total:'+str(total)+'byte')
        ret = ResultDPOP(None)
        ret.totalCost=totalCost
        ret.utilMsgCount=len(sizeArr)
        ret.utilMsgSizeMin=str(minMaxAvg[0]) + 'byte'
        ret.utilMsgSizeMax=str(minMaxAvg[2]) + 'byte'
        ret.utilMsgSizeAvg=str(minMaxAvg[4]) + 'byte'
        ret.total = str(total) + 'byte'
        ret.NCCCs = nccc
        ret.totalTime=2*(self.msgMailer.getAgentManager().getTreeHeight()-1) * 0
        
        return ret

    def messageContent(self,msg):
        
        if msg.getType() == DPOPAgent.TYPE_VALUE_MESSAGE:
            valueIndex= msg.getValue()
            print("value["+str(valueIndex)+"]")
        elif msg.getType() == DPOPAgent.TYPE_UTIL_MESSAGE:
            mdData = msg.getValue()
            for i in mdData.dimensions:
                print(i.name)
        
    def disposeMessage(self,msg):
        
        
        if msg.getType() == DPOPAgent.TYPE_VALUE_MESSAGE:
            self.disposeValueMessage(msg)
        elif  msg.getType() == DPOPAgent.TYPE_UTIL_MESSAGE:
            # self.utilMsgSizes.append(msg.getValue().dimensionSize())
            self.disposeUtilMessage(msg)
    
    def sendUtilMessage(self,multiDimentionalData):
        if self.isRootAgent() == True:
            return None
        #print(str(self.id)+ ' ' + str(self.parent))
        a =4*len(multiDimentionalData.data)
        #print(multiDimentionalData.dimensions)
        #print(a)
        self.utilMsgSizes.append(a)
        
        utilMsg = Message(self.id,self.parent,DPOPAgent.TYPE_UTIL_MESSAGE,multiDimentionalData)
        self.sendMessage(utilMsg)
    
    def disposeUtilMessage(self,msg):
        #self.nccc += 1
        if self.isRootAgent() == True and self.rawMDData == None:
            self.rawMDData = msg.getValue()
        else:
            self.rawMDData = self.rawMDData.mergeDimension(msg.getValue())
            
            
        self.disposedChildrenCount += 1
        if self.disposedChildrenCount>=len(self.children):
            
            #所有子节点(包括伪子节点)的UtilMessage都已收集完毕，
			#则可以进行针对本节点的降维，将最终得到的UtilMessage再往父节点发送
            result = self.rawMDData.reductDimension(str(self.id),ReductDimensionResult.REDUCT_DIMENSION_WITH_MIN)
            
            self.reductDimensionResultIndexes=result.getResultIndex()
            self.dimensions=result.getMdData().getDimensions()
            if self.isRootAgent()==True:
                self.totalCost=result.getMdData().getData()[0]
                self.valueIndex=self.reductDimensionResultIndexes[0]
                valueIndexes = {}
                valueIndexes[self.id] = self.valueIndex
                # print(valueIndexes)
                self.sendValueMessage(valueIndexes)
                self.stopRunning()
            else:
                self.sendUtilMessage(result.getMdData())

    def sendValueMessage(self,valueIndexes):
        if self.isLeafAgent() == True:
            return None
        
        for i in range(0,len(self.children)):
            valee = valueIndexes
            
            valueMsg = Message(self.id,self.children[i],DPOPAgent.TYPE_VALUE_MESSAGE,valee)
            self.sendMessage(valueMsg)

    def disposeValueMessage(self,msg):
        valueIndexes = msg.getValue()
        periods = [0]*len(self.dimensions)
        for i in range(0,len(self.dimensions)):
            temp = 1
            for j in range(i+1,len(self.dimensions)):
                temp*=self.dimensions[j].getSize()
            periods[i]=temp
        index=0
        for i in range(0,len(periods)):
            index += valueIndexes[int(self.dimensions[i].getName())] * periods[i]
        self.valueIndex=self.reductDimensionResultIndexes[index]
        valueIndexes[self.id] = self.valueIndex
        self.sendValueMessage(valueIndexes)
        self.stopRunning()


    '''
    /**
	 * 返回arr[]中的最小元素，序号，最大元素，序号，平均值
	 * @param arr
	 * @return {minValue, minIndex, maxValue, maxIndex, avgValue}
	 */
    '''

    def minMaxAvg(self,arr):
        minIndex=0
        minValue=arr[0]
        maxIndex=0
        maxValue=arr[0]
        total=arr[0]
        for i in range(1,len(arr)):
            if minValue>arr[i]:
                minIndex=i
                minValue=arr[i]
            if minValue<arr[i]:
                maxIndex=i 
                maxValue=arr[i]
            total+=arr[i]
        return [minValue,minIndex,maxValue,maxIndex,int(total/len(arr))]



    def computeLocalUtils(self):
        
        dataLength = 1
        dimensions = []
        for i in range(0,len(self.allParents)):
            
            parentId = self.allParents[i]
            dimensionSize = len(self.neighbourDomains[parentId])
            dimensions.append(Dimension(str(parentId)+'',dimensionSize,self.parentLevels[i],None))
            dataLength = dataLength*dimensionSize
        dimensions.append(Dimension(str(self.id)+"", len(self.domain), self.level,None))
        dataLength = dataLength*len(self.domain)

        agentValueIndexes = [0] * (len(self.allParents)+1)
        try:
            data = [0]*dataLength
        except:
            print('数据太大，内存溢出！')
            sys.exit(1)
        #data = [0]*dataLength
        dataIndex = 0
        curDimention=len(agentValueIndexes)-1
        while dataIndex < len(data):
            costSum=0
            for i in range(0,len(self.allParents)):
                costSum+=self.constraintCosts[self.allParents[i]][agentValueIndexes[len(agentValueIndexes)-1]][agentValueIndexes[i]]
            self.nccc += 1
            data[dataIndex]=costSum
            agentValueIndexes[curDimention]+=1  
            # print(agentValueIndexes[curDimention])
            # print(dimensions[curDimention].getSize())
            while agentValueIndexes[curDimention] >= dimensions[curDimention].getSize():
                agentValueIndexes[curDimention]=0
                curDimention-=1
                if curDimention == -1:
                    break
                agentValueIndexes[curDimention]+=1
            curDimention=len(agentValueIndexes)-1
            dataIndex += 1
        return MultiDimensionData(dimensions,data)

    def easyMessageContent(self,msg,sender,receiver):
        pass
        
