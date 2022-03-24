from MultiDimensionData import *

class ReductDimensionResult:
    REDUCT_DIMENSION_WITH_MAX = 0
    REDUCT_DIMENSION_WITH_MIN = 1

    def __init__(self,mdData,resultIndex):
        self.mdData = mdData
        self.resultIndex = resultIndex

    def getMdData(self):
        return self.mdData

    def setMdData(self,mdData):
        self.mdData = mdData

    def getResultIndex(self):
        return self.resultIndex

    def setResultIndex(self):
        self.resultIndex = resultIndex

    