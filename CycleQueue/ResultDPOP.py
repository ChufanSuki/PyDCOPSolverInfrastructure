
from Result import *

class ResultDPOP(Result):

    def __init__(self,rs):
        if rs == None:
            super().__init__(None)
            self.utilMsgCount = 0.00
            self.utilMsgSizeMin = 0.00
            self.utilMsgSizeMax = 0.00
            self.utilMsgSizeAvg = 0.00
            self.NCCCs = 0
            self.total = 0
        else:
            super().__init__(rs)
            self.utilMsgCount = 0.00
            self.utilMsgSizeMin = 0.00
            self.utilMsgSizeMax = 0.00
            self.utilMsgSizeAvg = 0.00
            self.NCCCs = 0
            self.total = 0

    


