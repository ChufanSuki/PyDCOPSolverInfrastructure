class Result:
    
    def __init__(self,rs):
        if rs == None:
            self.totalCost = 0
            self.messageQuantity = 0
            self.lostRatio = 0
            self.totalTime = 0
            self.otherResults = {}
            self.agentValues = {}
        else:
            self.messageQuantity=rs.messageQuantity
            self.lostRatio=rs.lostRati
            self.totalTime=rs.totalTime
            self.agentValues=rs.agentValues
            self.totalCost = rs.totalCost
            self.otherResults = {}


    def min(self,rs):
        self.messageQuantity = self.messageQuantity if self.messageQuantity < rs.messageQuantity else rs.messageQuantity
        self.lostRatio = self.lostRatio if self.lostRatio < rs.lostRatio else rs.lostRatio
        self.totalTime = self.totalTime if self.totalTime < rs.totalTime else rs.totalTime
        self.totalCost = self.totalCost if self.totalCost < rs.totalCost else rs.totalCost

    def max(self,rs):
        self.messageQuantity = self.messageQuantity if self.messageQuantity > rs.messageQuantity else rs.messageQuantity
        self.lostRatio = self.lostRatio if self.lostRatio > rs.lostRatio else rs.lostRatio
        self.totalTime = self.totalTime if self.totalTime > rs.totalTime else rs.totalTime
        self.totalCost = self.totalCost if self.totalCost > rs.totalCost else rs.totalCost

    def add(self,rs,validCount):
        self.messageQuantity += int(1.0*rs.messageQuantity/validCoun)
        self.lostRatio += int(1.0*rs.lostRatio/validCount)
        self.totalTime += int(1.0*rs.totalTime/validCount)
        self.totalCost += int(1.0*rs.totalCost/validCount)

    def minus(self,rs,validCount):
        self.messageQuantity -= int(1.0*rs.messageQuantity/validCoun)
        self.lostRatio -= int(1.0*rs.lostRatio/validCount)
        self.totalTime -= int(1.0*rs.totalTime/validCount)
        self.totalCost -= int(1.0*rs.totalCost/validCount)


