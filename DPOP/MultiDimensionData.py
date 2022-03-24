from Dimension import *
from ReductDimensionResult import *


class MultiDimensionData:

    def __init__(self,dimensions,data):
        self.dimensions = dimensions
        self.data = data
        #print(dimensions)

    def getDimensions(self):
        return self.dimensions

    def getData(self):
        return self.data

    def indexOf(self,dimensions,dimensionName):
        if dimensions != None:
            for i in range(0,len(dimensions)):
                if dimensions[i].getName() == dimensionName:
                    return i

            return -1

        else:
            for i in range(0,len(self.dimensions)):
                if self.dimensions[i].getName() == dimensionName:
                    return i

            return -1

    def isReductable(self,dimensionName):
        return self.dimensions.get(self.indexOf(None,dimensionName)).isReductable()

    
    def reductDimension(self,dimensionName,reductDimentionMethod):
        dimensionToReductIndex = self.indexOf(None,dimensionName)
        dimensionToReduct = self.dimensions[dimensionToReductIndex]

        dimensionsNew = []
        for dimen in self.dimensions:
            dimensionsNew.append(Dimension(None,None,None,dimen))
        dimensionsNew.pop(dimensionToReductIndex)

        periodsNew = []
        for i in range(0,len(self.dimensions)):
            temp = 1
            for j in range(i+1,len(self.dimensions)):
                temp *= self.dimensions[j].getSize()
                #print(temp)

            periodsNew.append(temp)
        #print(dimensionToReductIndex)
        for i in range(0,dimensionToReductIndex):
            periodsNew[i] /= dimensionToReduct.getSize()
            #print(periodsNew[i])
        
        periodsNew[dimensionToReductIndex] = 0
        #print(periodsNew)
        #print(len(self.data) / dimensionToReduct.getSize())
        dataNew = [0] * int(len(self.data) / dimensionToReduct.getSize())
        resultIndexes = [0] * len(dataNew)
        agentValueIndexes = [0] * len(self.dimensions)
        dataIndex = 0
        dataIndexNew = 0
        curDimension = len(self.dimensions)-1
        #print(dataNew)
        #print(len(self.data))
        if reductDimentionMethod == ReductDimensionResult.REDUCT_DIMENSION_WITH_MIN:
            for i in range(0,len(dataNew)):
                dataNew[i] = 999999
            while dataIndex < len(self.data):
                #print('---------')
                #print(dataIndexNew)
                dataIndex = int(dataIndex)
                dataIndexNew = int(dataIndexNew)
                if self.data[dataIndex] < dataNew[dataIndexNew]:
                    dataNew[dataIndexNew] = self.data[dataIndex]
                    resultIndexes[dataIndexNew] = agentValueIndexes[dimensionToReductIndex]
                agentValueIndexes[curDimension] += 1
                dataIndexNew += periodsNew[curDimension]
                #print(dataIndexNew)
                while agentValueIndexes[curDimension] >= self.dimensions[curDimension].getSize():
                    agentValueIndexes[curDimension] = 0
                    dataIndexNew -= self.dimensions[curDimension].getSize()*periodsNew[curDimension]
                    curDimension -= 1
                    if curDimension == -1:
                        dataIndexNew=self.dimensions[0].getSize()*periodsNew[0]
                        break
                    agentValueIndexes[curDimension] += 1
                    if curDimension != dimensionToReductIndex:
                        dataIndexNew += periodsNew[curDimension]
                        #print(dataIndexNew)
                        #print(periodsNew[curDimension])
                curDimension = len(agentValueIndexes)-1
                dataIndex += 1
                

        else:
            for i in range(0,len(dataNew)):
                dataNew[i] = 0
            while dataIndex < len(self.data):
                if self.data[dataIndex] > dataNew[dataIndexNew]:
                    dataNew[dataIndexNew] = self.data[dataIndex]
                    resultIndexes[dataIndexNew] = agentValueIndexes[dimensionToReductIndex]
                agentValueIndexes[curDimension] += 1
                dataIndexNew += periodsNew[curDimension]
                while agentValueIndexes[curDimension] >= self.dimensions.get(curDimension).getSize():
                    agentValueIndexes[curDimension] = 0
                    dataIndexNew -= self.dimensions.get(curDimension).getSize()*periodsNew[curDimension]
                    curDimension -= 1
                    if curDimension == -1:
                        dataIndexNew=self.dimensions[0].getSize()*periodsNew[0]
                        break
                    agentValueIndexes[curDimension] += 1
                    if curDimension != dimensionToReductIndex:
                        dataIndexNew += periodsNew[curDimension]
                curDimension = len(agentValueIndexes)-1
                dataIndex += 1
        mdData = MultiDimensionData(dimensionsNew,dataNew)
        return ReductDimensionResult(mdData, resultIndexes)


    



    def mergeDimension(self,mdDataB):
        dimensionsNew = []
       
        for dimen in self.dimensions:
            dimensionsNew.append(Dimension(None,None,None,dimen))
        for dimen in mdDataB.dimensions:
            index = MultiDimensionData.indexOf(self,dimensionsNew,dimen.getName())
            if index == -1:
                dimensionsNew.append(dimen)
            else:
                dimensionsNew[index].mergeConstraintCount(dimen)
        # for i in dimensionsNew:
        #     print(i.name)
        # print('----')
        # print(len(dimensionsNew))
        # print('----')
        dimensionsNew.sort(key=compare)
        
        if len(mdDataB.dimensions) == 0 and mdDataB.data != None and len(mdDataB.data) == 1:
            dataNewTemp = [0]*len(self.data)
            for i in range(0,len(dataNewTemp)):
                dataNewTemp[i] = self.data[i] + mdDataB.data[0]
            return MultiDimensionData(dimensionsNew,dataNewTemp)
        elif len(self.dimensions) == 0 and self.data != None and len(self.data) == 1:
            dataNewTemp = [0]*len(mdDataB.data)
            for i in range(0,len(dataNewTemp)):
                dataNewTemp[i] = mdDataB.data[i] + self.data[0]
            return MultiDimensionData(dimensionsNew,dataNewTemp)
        periodsA = [0] * len(dimensionsNew)
        
        for i in range(0,len(dimensionsNew)):
            index=self.indexOf(None,dimensionsNew[i].getName())
            if index == -1:
                periodsA[i] = 0

            else:
                temp = 1
                for j in range(index+1,len(self.dimensions)):
                    temp *= self.dimensions[j].getSize()
                periodsA[i] = temp
        periodsB = [0] * len(dimensionsNew)
        for i in range(0,len(dimensionsNew)):
            index=mdDataB.indexOf(None,dimensionsNew[i].getName())
            if index == -1:
                periodsB[i] = 0

            else:
                temp = 1
                for j in range(index+1,len(mdDataB.dimensions)):
                    temp *= mdDataB.dimensions[j].getSize()
                periodsB[i] = temp
        dataNewLength = 1
        for dimen in dimensionsNew:
            dataNewLength *= dimen.getSize()

        dataNew = [0]*dataNewLength
        agentValueIndexes = [0] * len(dimensionsNew)
        dataIndexNew = 0
        dataIndexA = 0
        dataIndexB = 0
        
        curDimension=len(agentValueIndexes)-1
        #print(len(dimensionsNew))
        #print('\n')
        #print(dataNew)
        #print(self.data)
        while dataIndexNew < len(dataNew):
            # print('----------')
            # print(dataIndexB)
            dataNew[dataIndexNew]+=self.data[dataIndexA]
            dataNew[dataIndexNew]+=mdDataB.data[dataIndexB]
            agentValueIndexes[curDimension]+=1
            dataIndexA+=periodsA[curDimension]
            dataIndexB+=periodsB[curDimension]
            #print(dataIndexB)
            #print(dataNew)
            while agentValueIndexes[curDimension]>=dimensionsNew[curDimension].getSize():
                dataIndexA-=periodsA[curDimension]*agentValueIndexes[curDimension]
                dataIndexB-=periodsB[curDimension]*agentValueIndexes[curDimension]
                agentValueIndexes[curDimension]=0
                
                curDimension-=1
                if curDimension==-1:
                    break
                agentValueIndexes[curDimension]+=1
                dataIndexA+=periodsA[curDimension]
                dataIndexB+=periodsB[curDimension]
            # print(dataIndexB)
            # print('----------')
            curDimension=len(agentValueIndexes)-1
            dataIndexNew += 1
        #print(dataNew)
        return MultiDimensionData(dimensionsNew,dataNew)
    
    def dimensionSize(self):
        # for i in self.dimensions:
            # print(i)
        return len(self.dimensions)


    def arrayToString(self,arr):
        if arr == None or len(arr) == 0:
            return ""
        s = '['
        for i in range(0,len(arr)-1):
            s += str(arr[i]) + ','
        s += str(arr[len(arr)-1]) + ']'
        return s

    def toString(self):
        return self.arrayToString(self.data)

def compare(dimen):
    return dimen.priority


if __name__=='__main__':
    dimensions = []
    dimensions.append(Dimension('A1',3,0,None))
    dimensions.append(Dimension('A5',3,4,None))
    mdDataA = MultiDimensionData(dimensions,[0,6,10,2,1,3,2,9,6])
    
    dimensions_B = []
    dimensions_B.append(Dimension('A2',3,1,None))
    dimensions_B.append(Dimension('A5',3,4,None))
    mdDataB = MultiDimensionData(dimensions_B,[5,2,7,6,3,11,6,9,4])
    
    
    dimensions_C = []
    dimensions_C.append(Dimension('A4',3,3,None))
    dimensions_C.append(Dimension('A5',3,4,None))
    mdDataC = MultiDimensionData(dimensions_C,[1,3,3,2,5,7,8,9,4])
    
   
    #print(mdDataA.data)

    
    targetData=mdDataA.mergeDimension(mdDataB)
    # print(targetData.dimensions)
    # print(targetData.data)
    targetData = targetData.mergeDimension(mdDataC)
    #print(targetData.data)
    targetData=targetData.reductDimension("A5", ReductDimensionResult.REDUCT_DIMENSION_WITH_MIN).getMdData()
    print(targetData.toString())


    


                



        

        



                
    
