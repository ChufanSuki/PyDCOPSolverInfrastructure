# import sys
# sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\DCOPPharse\\')
# sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\DSA\\')
# sys.path.append('c:\\Users\\Klaus\\Desktop\\DCOP\\DPOP\\')

from Problem import * 
from AgentCycle import *
from DsaA_Agent import *
from DPOPAgent import *

class AgentManagerCycle:

    def __init__(self,problem,agentType,num,gai):
        self.agents = {}
        self.treeHeight=0
        for agentId in problem.agentNames.keys():
            agent = None
            if agentType == 'DPOP':
                agent = DPOPAgent(
                    agentId,
                    problem.agentNames[agentId],
                    problem.agentLevels[agentId],
                    problem.domains[problem.agentDomains[agentId]]
                )
            elif agentType == 'DSA_A':   #DSA算法
                agent = DasA_Agent(
                        agentId,    #Agent编号
                        problem.agentNames[agentId],   #Agent名字
                        problem.agentLevels[agentId],  #Agent在DFS中的等级
                        problem.domains[problem.agentDomains[agentId]],  #Agent所属domain的取值列表
                        num,
                        gai
                )
            
            
            neighbourDomains = {}    #邻居的doamin取值集合
            constraintCosts = {}   #该Agent到邻居Agent的Cost集合,是一个二维列表，当前Agent到邻居的二维矩阵，行为邻居取值，列为当前Agent取值，矩阵的值为他们的代价
            neighbourAgentIds = problem.neighbourAgents[agentId]   #该Agent的邻居
            neighbourLevels = {}    #各邻居在DFS树结构中的level
            for i in range(0,len(neighbourAgentIds)):
                neighbourDomains[neighbourAgentIds[i]] = problem.domains[problem.agentDomains[neighbourAgentIds[i]]]
                neighbourLevels[neighbourAgentIds[i]] = problem.agentLevels[neighbourAgentIds[i]]
            
            neighbourAgentCostNames = problem.agentConstraintCosts[agentId]   #获取与邻居约束的约束名字，例如['R0', 'R1', 'R2']
            for i in range(0,len(neighbourAgentCostNames)):    #一一进行对应,扩展成二维列表，并完善constraintCosts
                if agentId < neighbourAgentIds[i]:
                    constraintCosts[neighbourAgentIds[i]] = self.toTwoDimension(
                        problem.costs[neighbourAgentCostNames[i]],
                        len(problem.domains[problem.agentDomains[agentId]]),
                        len(problem.domains[problem.agentDomains[neighbourAgentIds[i]]])
                    )
                else:                                        #因为我们约束代价存放是两个Agent对应是按照左边ID小，右边ID大的顺序进行存放的
                    temp = self.toTwoDimension(
                        problem.costs[neighbourAgentCostNames[i]],
                        len(problem.domains[problem.agentDomains[neighbourAgentIds[i]]]),
                        len(problem.domains[problem.agentDomains[agentId]])
                        
                    )
                    constraintCosts[neighbourAgentIds[i]] = self.reverse(temp)
            # print('---------')
            # print(neighbourAgentCostNames)
            # print(agentId)
            # print(problem.agentConstraintCosts)
            # print(neighbourDomains)
            # print(neighbourLevels)
            # for i in constraintCosts.keys():
            #     print(i)
            #     print(constraintCosts[i])
            agent.setNeibours(problem.neighbourAgents[agentId],  #Agent的邻居
                problem.parentAgents[agentId],   #DFS树中的父母
                problem.childAgents[agentId],    #DFS树中的孩子
                problem.allParentAgents[agentId],   #DFS树中的所有父母
                problem.allChildrenAgents[agentId],  #DFS树中的所有孩子
                neighbourDomains,   #邻居节点的domains
                constraintCosts,    #上文刚刚所求的代价矩阵
                neighbourLevels   #邻居所对应的DFS树的层次
            )
            self.agents[agent.getId()] = agent

            AgentCycle.totalHeight = 0   #算树高
            for tempAgent in self.agents.values():
                if AgentCycle.totalHeight < tempAgent.level:
                    AgentCycle.totalHeight = tempAgent.level
            if self.treeHeight < problem.agentLevels[agentId]:
                self.treeHeight = problem.agentLevels[agentId]
        self.treeHeight += 1

    def getTreeHeight(self):
        return self.treeHeight

    def getAgent(self,agentId):
        if agentId in self.agents.keys():
            return self.agents[agentId]
        else:
            return None

    def getAgentValues(self):
        agentValues = {}
        for agent in self.agents.values():
            agentValues[agent.getId()] = agent.getValue()

        return agentValues

    def getAgents(self):
        return self.agents

    def getAgentCount(self):
        return len(self.agents)

    def startAgents(self,msgMailer):
        for agent in self.agents.values():
            agent.setMessageMailer(msgMailer)
            agent.startProcess()

    def stopAgents(self):
        for agent in self.agents.values():
            agent.stopRunning()

    def printResults(self,results):
        if len(results) > 0:
            agent = None
            for agentId in self.agents.keys():
                # print('-------')
                # print(self.agents.keys())
                agent = self.agents[agentId]
                break
            return agent.printResults(results)

        return None

    def easyMessageContent(self,msg):
        senderAgent = self.getAgent(msg.getIdSender())
        receiverAgent=self.getAgent(msg.getIdReceiver())
        return senderAgent.easyMessageContent(msg, senderAgent, receiverAgent)

    def getTotalCost(self):
        totalCost = 0
        for agent in self.agents.values():
            if agent != None:
                totalCost += agent.getLocalCost()

        totalCost = totalCost/2
        return totalCost
    




    def toTwoDimension(self,arr,rows,cols):
        if arr == None or int(rows)*int(cols)!=len(arr):
            return None
        ret = []
        for i in range(0,int(rows)):
            tet = []
            for j in range(0,int(cols)):
               tet.append(arr[i*cols+j])
            ret.append(tet)
           
        # print(ret)
        # print("++++++++++++++++++++++++")
        return ret

    def reverse(self,source):
        temp = []
        for i in range(0,len(source)):
            txt = []
            for j in range(0,len(source[0])):
                txt.append(source[j][i])
            #txt.reverse()
            temp.append(txt)
        return temp

        
