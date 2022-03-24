

class Message:
    TYPE_TERMINATE_MESSAGE = 9999

    def __init__(self,idSender,idReceiver,type1,value):
        self.idSender = idSender
        self.idReceiver = idReceiver
        self.type = type1
        self.value = value


    def getIdSender(self):
        return self.idSender

    def getIdReceiver(self):
        return self.idReceiver

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def toString(self):
        return str(self.idSender) + str(self.idReceiver) + str(self.type)
        
