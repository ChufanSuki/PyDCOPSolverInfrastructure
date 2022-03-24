import math

class Dimension:
    

    def __init__(self,name,size,priority,dimen):
        if dimen == None:
            self.name = name
            self.size = size
            self.priority = priority
            self.constraintCountTotal = 99999999
            self.constraintCount = 0
        else:
            self.name = dimen.name
            self.size = dimen.size
            self.priority = dimen.priority
            self.constraintCountTotal = dimen.constraintCountTotal
            self.constraintCount = dimen.constraintCount

    def getName(self):
        return self.name

    def getSize(self):
        return self.size

    def getPriority(self):
        return self.priority

    def mergeConstraintCount(self,dimen):
        self.constraintCount += dimen.constraintCount
        self.constraintCountTotal = self.constraintCountTotal if self.constraintCountTotal <= dimen.constraintCountTotal else dimen.constraintCountTotal


    def setConstraintCountTotal(self,constraintCountTotal):
        self.constraintCountTotal = constraintCountTotal

    def isReductable(self):
        return (int(math.ceil(self.constraintCount))) >= self.constraintCountTotal

    def equals(self,dimen):
        return self.name == dimen.name

    def toString(self):
        return "["+self.name+" "+str(self.size)+" "+str(self.priority)+" "+str(self.constraintCountTotal)+" "+str(self.constraintCount)+"]"
