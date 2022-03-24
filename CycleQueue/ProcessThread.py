from abc import abstractmethod, ABCMeta
import threading

class ProcessThread():
    __metaclass__ = ABCMeta

    def __init__(self,threadName):
        self.thread = None
        self.threadName = threadName
        self.running = False

    def startProcess(self):
        if self.thread == None:
            if self.threadName == None:
                self.thread = threading.Thread(target=self.task)
            else:
                
                self.thread = threading.Thread(target=self.task,name=self.threadName)
            self.thread.start()

    def task(self):
        self.running = True
        self.initializeProcess()
        self.runProcess()
        self.finalizeProcess()
        self.running = False

    def stopRunning(self):
        if self.thread != None:
            self.running = False
            # self.thread = threading.Thread(target=task).ident

    def isRunning(self):
        return self.running

    def initializeProcess(self):
        pass

    def finalizeProcess(self):
        pass
    

    @abstractmethod
    def runProcess(self):
        pass





    
