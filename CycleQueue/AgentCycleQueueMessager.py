from abc import abstractmethod, ABCMeta
from Message import *
from ProcessThread import *
from threading import Thread, Lock,Event

class AgentCycleQueueMessager(ProcessThread):
    __metaclass__ = ABCMeta

    def __init__(self,threadName):
        super().__init__(threadName)
        self.msgQueue = []

    def setLocks(self,temp,lock,event,test):
        self.temp = temp  
        #temp[0]用于通知Agent开始,是bool类型,对应cycleBegin
        #temp[1]用于Agent通知消息中心开始，是bool类型，对应cycleEnd
        #temp[2]用于每轮Agent处理完信息标志,是int类型，对应cycleEndCount
        #temp[3]用于每轮开始总共运行的Agent，对应totalAgentCount
        #temp[4]用于抑制消息中心太快更新，对应OperateEndCount，totalAgentCount＝totalAgentCountTemp，而totalAgentCountTemp还未更新
        #temp[5]用于每轮运行的Agent总数更新，对应totalAgentCountTemp
        self.lock = lock #加锁，进行原子操作
        self.singal = event
        self.test = test

    def addMessage(self,msg):
        self.msgQueue.append(msg)

    def initRun(self):
        pass

    def runFinished(self):
        pass

    @abstractmethod
    def disposeMessage(self,msg):
        pass

    @abstractmethod
    def allMessageDisposed(self):
        pass

    def messageLost(self,msg):
        pass



    def runProcess(self):
        self.initRun()
        if self.temp[1] == False:
            with self.lock:
                self.temp[2] += 1
            if self.temp[2] >= self.temp[3]:
                self.temp[2] = 0
                self.temp[1] = True
                self.test.set()
                #self.singal.clear()
                self.singal.wait()
                
                
        while self.isRunning() == True:   #Agent是否结束
            
            while self.temp[0] == False:   #Agent是否该处理信息了
               #print(self.threadName)
            #    self.lock.acquire()
            #    self.lock.release()
                self.test.set()
                #self.singal.clear()
                self.singal.wait()
                
            
            if self.temp[0] == True:
                #print("kkk")
                while len(self.msgQueue) !=0:    #msgQueue存在有给Agent的消息
                    msg = None
                    try:
                        msg = self.msgQueue.pop(0)
                    except:
                        msg = None     
                    if msg != None:
                        #with self.lock:
                        self.disposeMessage(msg)   #Agent装载消息
                #with self.lock:
                self.allMessageDisposed()     #Agent进行消息处理
                lastAgent = True     #判断是否是最后一个处理完的Agent
                with self.lock:
                    self.temp[2] += 1
                    number = self.temp[2]
                if number < self.temp[3]:   #不是最后一个Agent
                    lastAgent = False    
                    while self.temp[2] != 0:
                        # self.lock.acquire()
                        # self.lock.release()
                        #self.test.set()
                        #self.singal.clear()
                        self.singal.wait()
                elif number >= self.temp[3]:   #是最后一个Agent
                    lastAgent = True
                    with self.lock:
                        self.temp[2] = 0
                        if self.temp[0] == True:
                            self.temp[0] = False      #最后一个Agent消息处理完毕      
                if lastAgent == False:
                    if self.isRunning() == False:
                        pass
                    else:
                        with self.lock:
                            self.temp[4] += 1
                            # if self.OperateEndCount == self.totalAgentCount:
                if lastAgent == True:
                    if self.isRunning() == False:
                        pass
                    else:
                        with self.lock:
                            self.temp[4] += 1
                            # if self.OperateEndCount == self.totalAgentCount:
                    if self.temp[1] == False:
                        self.temp[1] = True
                        self.test.set()
                        #self.singal.clear()
                        self.singal.wait()
        with self.lock:
            self.temp[5] -= 1
            self.temp[4] += 1
        self.runFinished()


    
        

                


            


                      

            


