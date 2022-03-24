import random
import itertools
from string import ascii_lowercase
from xml.etree import ElementTree as ET
import copy


class UndirectedGraph:
    def __init__(self,n,p1):
        self.__number = n
        self.p1 = p1
        self.__list = []
        self.__node_list = []
        self.__graph = {}
        self.__edges = []
        self.__generate_random_graph(n)
        self.__generate_edge(self.__graph)
        



    def __generate_letter(self):
        
        for size in itertools.count(1):
            for s in range(1,self.__number+1):
                yield "".join("A"+str(s))


    def __generate_random_graph(self,n):
       
       
        for node in self.__generate_letter():  # 循环创建结点
            self.__node_list.append(node)
            self.__number -= 1
            if self.__number == 0:
                break
        print(self.__node_list)

        for node in self.__node_list:
            self.__graph[node] = []  # graph为dict结构，初始化为空列表
        num = n * (n - 1) / 2 * self.p1 / 100
        for node in self.__node_list:  # 创建连接无向图（无加权值）
            #self.__number = random.randint(2,3)  # 随机取1-n个结点
            self.__number = 1
            if len(self.__graph[node])!=0:
                continue
            for i in range(self.__number):
                index = random.randint(0, n - 1)  # 某个结点的位置
                node_append = self.__node_list[index]
                while node_append == node:
                    index = random.randint(0, n - 1)
                    node_append = self.__node_list[index]
                if node_append not in self.__graph[node]:
                    self.__graph[node].append(node_append)
                    self.__graph[node_append].append(node)
                    num = num - 1
            if int(num == 0):
                break
        
        test = []
        dict4 = copy.deepcopy(self.__graph)   
        for i in dict4.keys():
            t = dict4[i]
            t.append(i)
            test.append(set(t))
        h = self.merge_list(test)
        merge = []
        for i in h:
            merge.append(list(i))
        print(self.__graph)
        print(merge)
        if len(merge)!=1:
            for i in (1,len(merge)-1):
                index1 = random.randint(0,len(merge[i])-1)
                index2 = random.randint(0,len(merge[i-1])-1)
                self.__graph[merge[i][index1]].append(merge[i-1][index2])
                self.__graph[merge[i-1][index2]].append(merge[i][index1])
                num = num - 1
                if num==0:
                    break
        if int(num) != 0:
            for i in range(0,int(num)):
                t = random.randint(0, n - 1)
               
                node = self.__node_list[t]
                self.__number = 1
                while True:
                    index = random.randint(0, n - 1)  # 某个结点的位置
                    
                    node_append = self.__node_list[index]
                    k = 0
                    while node_append in self.__graph[node]:   #找到一个与该Agent没有连接的点
                        node_append = self.__node_list[(index + 1) % n]
                        k = k + 1
                        if k == n:
                            break
                    if k==n:   #这说明它与其他节点都联通
                        break
                    if node_append not in self.__graph[node] and node != node_append:
                        self.__graph[node].append(node_append)
                        self.__graph[node_append].append(node)
                        break
                        
        print(self.__graph)


    def __generate_edge(self,graph):
        """
        draw the edge of graph
        :param graph: a dict of graph
        :return: a list of edge
        """
        
        for node in self.__graph:
            for neighbour in self.__graph[node]:
                
                if (neighbour,node) in self.__edges:
                    continue
                self.__edges.append((node, neighbour))
        print(self.__edges)
    

    def getAgents(self):
        nbAgents = len(self.__graph)
        agents = ET.Element("agents")
        agents.set("nbAgents",""+str(nbAgents))

        for i in range(1,nbAgents+1):
            agent = ET.Element("agent")
            agent.set("name","A"+str(i))
            agent.set("id",str(i))
            agent.set("description","agent "+str(i))
            agents.append(agent)

        return agents


    def getDomaines(self,domainSize):
        domains = ET.Element("domains")
        domains.set("nbDomains","1")
        domain = ET.Element("domain")
        domain.set("name","D1")
        domain.set("nbValues",""+str(domainSize))
        domain.text = "1.."+str(domainSize)
        domains.append(domain)
        return domains


    def getVariables(self):
        nbVariables = len(self.__graph)
        variables = ET.Element("variables")
        variables.set("nbVariables",""+str(nbVariables))

        for i in range(1,nbVariables+1):
            variable = ET.Element("variable")
            agId = i
            index = 1    #这里还不太懂字段的作用
            variable.set("agent", "A" + str(agId))
            variable.set("name", "X" + str(agId) + "." + str(index))
            variable.set("id", str(index))
            variable.set("domain", "D1")
            variable.set("description", "variable " + str(agId) + "." + str(index))
            variables.append(variable)
        
        return variables


    def getNbEdges(self):
        n = len(self.__edges)
        return n



    def getConstraints(self):
        nbConstraint = len(self.__edges)
        constraints = ET.Element("constraints")
        constraints.set("nbConstraints",""+str(nbConstraint))
        edges = self.__edges

        for c in range(0,nbConstraint):
            constraint = ET.Element("constraint")
            constraint.set("name", "C" + str(c))
            constraint.set("model", "TKC")
            constraint.set("arity", str(2))
            e = edges[c]
            var1 = e[0]
            index1 = 1
            var2 = e[1]
            index2 = 1
            constraint.set("scope", "X" + str(var1[1:]) + "." + str(index1) + " X" + str(var2[1:]) + "." + str(index2))
            constraint.set("reference", "R" + str(c))
            constraints.append(constraint)

        return constraints



    def getSoftRelations(self,maxDisCSP, domainSize, tightness, minCost, maxCost):
        nbConstraint = len(self.__edges)
        nbTuples = int(domainSize * domainSize * (100 - tightness) / 100)
        relations = ET.Element("relations")
        relations.set("nbRelations", "" + str(nbConstraint))

        for c in range(0,nbConstraint):
            relation = ET.Element("relation")
            relation.set("name", "R" + str(c))
            relation.set("arity", "2")
            relation.set("nbTuples", "" + str(nbTuples))
            relation.set("semantics", "soft")
            relation.set("defaultCost",  str(1) if maxDisCSP else "infinity")
            tuples = ""
            if maxDisCSP:
                cost = "0:"
                tuples = cost + self.GenerateRandomTuples(domainSize, nbTuples)
            else:
                tuples = self.GenerateRandomSoftTuples(domainSize, nbTuples, minCost, maxCost)

            relation.text = tuples
            relations.append(relation)

        return relations


    def GenerateRandomTuples(self,domainSize,nbTuples):
        indexes = []
        for i in range(0,domainSize*domainSize):
            indexes.append(i)
        tuples = ""

        for t in range(0,nbTuples):
            tup = indexes.pop(random.randint(0,len(indexes)-1))
            val1 = int(tup / domainSize + 1)
            val2 = int(tup % domainSize + 1)
            tuples = tuples + str(val1) + " " + str(val2) + "|"

        return tuples[0:len(tuples)-1]


    def GenerateRandomSoftTuples(self,domainSize, nbTuples, minCost, maxCost):
        sb = ""
        indexes = []

        for t in range(0,domainSize*domainSize):
            indexes.append(t)

        for t in range(0,int(nbTuples)):
            cost = random.randint(0,maxCost) + minCost
            sb = sb + str(cost) + ":"
            tup = indexes.pop(random.randint(0,len(indexes)-1))
            val1 = int(tup / domainSize + 1)
            val2 = int(tup % domainSize + 1)
            sb = sb + str(val1) + " " + str(val2) + "|"

        return sb[0:len(sb)-1]

    def merge_list(self,L):
        lenth = len(L)
        for i in range(1, lenth):
            for j in range(i):
                if L[i] == {0} or L[j] == {0}:
                    continue
                x = L[i].union(L[j])
                y = len(L[i]) + len(L[j])
                if len(x) < y:
                    L[i] = x
                    L[j] = {0}
        return [i for i in L if i != {0}]

        













    


    

    

