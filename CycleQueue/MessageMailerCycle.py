from Message import *
from AgentManagerCycle import *
from MailerCycleQueueMessager import *
from threading import Thread, Lock,Event
from AgentCycle import *
import time
from Result import *


class MessageMailerCycle(MailerCycleQueueMessager):

    def __init__(self,agentManager,ty):
        '''
        #temp[0]用于通知Agent开始,是bool类型,对应cycleBegin
        #temp[1]用于Agent通知消息中心开始，是bool类型，对应cycleEnd
        #temp[2]用于每轮Agent处理完信息标志,是int类型，对应cycleEndCount
        #temp[3]用于每轮开始总共运行的Agent，对应totalAgentCount
        #temp[4]用于抑制消息中心太快更新，对应OperateEndCount，totalAgentCount＝totalAgentCountTemp，而totalAgentCountTemp还未更新
        #temp[5]用于每轮运行的Agent总数更新，对应totalAgentCountTemp
        '''
        self.type = ty
        self.temp = [False,False,0,agentManager.getAgentCount(),agentManager.getAgentCount(),agentManager.getAgentCount()]
        self.singal = Event() #用于控制Agent的挂起与运行
        self.test = Event() #用于控制邮箱的挂起与运行
        self.lock = Lock() #加锁，控制访问临界变量
        super().__init__("Mailer",self.temp,self.lock,self.singal,self.test)  #构造并获取MailerCycleQueueMessager类的属性与方法
        self.agentManager = agentManager   #获取agentManager对象
        self.results = []    #计算结果列表
        self.eventListeners = []   #监听列表，目前预留字段，本平台暂时没用
        self.totalCostInCycle = []  #记录每次cycle记录
        self.timeCostInCycle = []    #记录cycle时间
        self.messageQuantityInCycle = []    #记录每次的通信次数
        self.messageLostQuantity = 0    #每个cycle丢失的消息次数
        self.messageQuantity = 0   #发送的消息的总数
        self.timeEnd = 0
        self.timeStart = 0
        self.initFinished = False   #是否初始化完成
        self.re = {}
        
        

    def setResult(self,result):
        self.results.append(result)

        if len(self.results) >= self.agentManager.getAgentCount():   #mailer停止函数
            self.stopRunning()

    def getResults(self):
        return self.results

    def easyMessageContent(self,msg):
        return self.agentManager.easyMessageContent(msg)

    def disposeMessage(self,msg):     #处理消息，将对应的消息发给对应的Agent
        self.messageQuantity += 1    #通信次数加一
        self.agentManager.getAgent(msg.getIdReceiver()).addMessage(msg)

    def getAgentManager(self):
        return self.agentManager
    def messageLost(msg):
        self.messageLostQuantity += 1


    def initRun(self):
        super().initRun()

        for agent in self.agentManager.getAgents().values():
            agent.setLocks(self.temp,self.lock,self.singal,self.test)

        self.timeStart = time.time()
        self.initFinished = True

    def runFinished(self):
        print("hello")
        super().runFinished()
        temp = self.agentManager.printResults(self.results)   #计算最后总的结果
        test = self.messageLostQuantity*100.0/(self.messageQuantity+self.messageLostQuantity)
        res = format(test, '.0%')
        #print("messageQuantity: "+str(self.messageQuantity)+" messageLostQuantity: "+str(self.messageLostQuantity)+" lostRatio: "+res)
        self.timeEnd = time.time()
        #print(self.messageQuantity)


        self.re['messageQuantity:'] = str(self.messageQuantity)
        self.re['messageLostQuantity:'] = str(self.messageLostQuantity)
        self.re['lostRatio:'] = res


        temp.messageQuantity=self.messageQuantity
        temp.lostRatio=int(self.messageLostQuantity*100.0/(self.messageQuantity+self.messageLostQuantity))
        temp.totalTime=self.timeEnd-self.timeStart
        temp.agentValues=self.agentManager.getAgentValues()
        #print("Mailer stopped, totalTime: "+str(format(temp.totalTime,'.3f') )+"s")
        #print("Cycle Count: "+str(self.cycleCount))

        self.re['Mailer stopped, totalTime:'] = str(format(temp.totalTime,'.3f') )+"s"
        self.re['Cycle Count: '] = str(self.cycleCount)
        result =temp
        #print("TotalCost: "+str(result.totalCost))
        #print("RunningTime: "+str(format(result.totalTime,'.3f'))+'s')
        #print("MessageQuantity: "+str(result.messageQuantity))

        self.re['TotalCost:'] = str(result.totalCost)
        self.re['RunningTime:'] = str(format(result.totalTime,'.3f'))+'s'
        
        
        if self.type == 'DPOP':
            self.re['NCCCs:'] = str(result.NCCCs)
            self.re['utilMsgCount:'] = temp.utilMsgCount
            #self.re['utilMsgSizeMin:'] = temp.utilMsgSizeMin
            #self.re['utilMsgSizeMax:'] = temp.utilMsgSizeMax
            self.re['utilMsgSizeAvg:'] = temp.utilMsgSizeAvg
            self.re['total:'] = temp.total
        for key in result.agentValues.keys():
            #print("Agent"+ str(key) + '：' +str(result.agentValues[key]))
            te = "Agent"+ str(key) +':'
            self.re[te] = str(result.agentValues[key])
        print(self.re)

        

    def dataInCycleIncrease(self):     #保存每个回合的totalcost
        if self.cycleCount == 0:       #除去初始化时Cost混乱时的统计
            return None
       
        self.totalCostInCycle.append(self.agentManager.getTotalCost())
        self.timeCostInCycle.append(time.time()-self.timeStart)
        self.messageQuantityInCycle.append(self.messageQuantity)

    def dataInCycleCorrection(self):
        correctCost = []
        correctTime = []
        correctMessages = []
        for i in range(0,self.cycleCount-1):
            correctCost.append(self.totalCostInCycle[i])
            correctTime.append(self.timeCostInCycle[i])
            correctMessages.append(self.messageQuantityInCycle[i])
        self.totalCostInCycle = correctCost
        self.timeCostInCycle = correctTime
        self.messageQuantityInCycle = correctMessages
        # print("修正后：")
        # print(self.totalCostInCycle)


    def initWait(self):  #为避免出现Agent线程开始而Mailer未初始化完成而出现错误
        while self.initFinished == False:
            try:
                print("--- sleep 200 ---")
                time.sleep(0.2)
            except:
                pass


    def join(self):
        self.thread.join()


        



        




