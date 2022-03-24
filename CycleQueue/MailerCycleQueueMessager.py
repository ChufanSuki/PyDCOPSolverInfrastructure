from abc import abstractmethod, ABCMeta
from Message import *
from ProcessThread import *
from threading import Thread, Lock

class MailerCycleQueueMessager(ProcessThread):
    __metaclass__ = ABCMeta

    def __init__(self,threadName,temp,lock,event,test):
        super().__init__(threadName)
        self.msgQueue = []
        #temp[0]用于通知Agent开始,是bool类型,对应cycleBegin
        #temp[1]用于Agent通知消息中心开始，是bool类型，对应cycleEnd
        #temp[2]用于每轮Agent处理完信息标志,是int类型，对应cycleEndCount
        #temp[3]用于每轮开始总共运行的Agent，对应totalAgentCount
        #temp[4]用于抑制消息中心太快更新，对应OperateEndCount，totalAgentCount＝totalAgentCountTemp，而totalAgentCountTemp还未更新
        #temp[5]用于每轮运行的Agent总数更新，对应totalAgentCountTemp
        self.temp = temp
        self.lock = lock
        self.cycleCount = 0
        self.singal = event
        self.test = test


    def addMessage(self,msg):
        self.msgQueue.append(msg)

    def runProcess(self):
        self.initRun()

        while self.isRunning() == True:
            
            while self.temp[1] == False:    #通知消息开始工作
                # self.lock.acquire()
                # self.lock.release()
                self.singal.set()
                #self.test.clear()
                self.test.wait()
                

            if self.temp[1] == True:     #mailer开始
                while len(self.msgQueue) != 0:    #查看mailer是否有消息以及对消息进行处理
                    msg = None
                    try:
                        msg = self.msgQueue.pop(0)    #取出消息
                    except:
                        msg = None
                    if msg != None:     #对消息进行处理
                        self.disposeMessage(msg)    #将消息发送给对应的Agent
                self.dataInCycleIncrease()   #将每一轮的结果进行一个保存
            
                self.cycleCount += 1    #迭代次数加一

                self.temp[1] = False    #消息工作结束

                while self.temp[4] < self.temp[3]:    #如果还有操作没结束的Agent，此时mailer需要等待，防止有AGent完成后结束进程而邮箱更新太快没有记录
                    # self.lock.acquire()
                    # self.lock.release()
                    self.singal.set()
                    #self.test.clear()
                    self.test.wait()

                self.temp[4] = 0   #将操作还没结束设置成0，准备开始下一轮
                self.temp[3] = self.temp[5]     #看是否还有Agent在活动，并做记录
                self.temp[0] = True     #Agent可以开始处理消息了
                self.singal.set()
                #self.test.clear()
                self.test.wait()

        self.dataInCycleCorrection()     #进行最后的数据保存
        self.runFinished()     #执行完成操作

    def getCycleCount(self):
        return self.cycleCount

    def dataInCycleIncrease(self):
        pass

    def dataInCycleCorrection(self):
        pass

    def initRun(self):
        pass

    def runFinished(self):
        pass

    @abstractmethod
    def disposeMessage(self):
        pass

    @abstractmethod
    def messageLost(self):
        pass


                





