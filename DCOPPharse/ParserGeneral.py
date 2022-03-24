
from xml.etree import ElementTree as ET
from Problem import *

class ParserGeneral:

    def __init__(self,root,problemType):
        self.root = root
        self.problemType = problemType

    def parseContent(self,problem):
        agentNameIds = self.parseAgents(self.root.find('agents'),problem)
        if agentNameIds == None:
            print("parseAgents() fails!")
            return None

        if self.parseDomains(self.root.find("domains"),problem) == False:
            print("parseDomains() fails!")
            return None


        variableNameAgentIds = self.parseVariables(self.root.find("variables"),problem,agentNameIds)
        if variableNameAgentIds == None:
            print("parseVariables() fails!")
            return None

        if self.parseRelations(self.root.find('relations'),problem) == False:  #解析cost
            print("parseRelations() fails!")
            return None

        if self.parseConstraints(self.root.find('constraints'),problem,variableNameAgentIds) == False:
            print("parseConstraints() fails!")
            return None
        return problem
        

    def parseConstraints(self,element,problem,variableNameAgentIds):
        if element ==None:
            return False

        nbConstraints = -1
        try:
            nbConstraints = int(element.attrib['nbConstraints'])
        except:
            return False

        elementList = list(element)
        if nbConstraints != len(elementList):
            print("nbConstraints!=elementList.size()")
            return False

        #图的邻接表存储结构
        neighbourAgents = {}
        neighbourConstraintCosts = {}
        for agentId in problem.agentNames.keys():
            neighbourAgents[agentId] = []
            neighbourConstraintCosts[agentId] = {}


        for i in range(0,nbConstraints):
            arity = int(elementList[i].attrib['arity'])  #问题维度
            if arity != 2:   #我们针对的是二维问题
                print("arity!=2")
                return False
            constraintedParts = elementList[i].attrib["scope"].split(' ')
            leftAgentId = variableNameAgentIds[constraintedParts[0]]   #获取具有约束关系的第一个Agent
            rightAgentId = variableNameAgentIds[constraintedParts[1]]  ##获取具有约束关系的第一个Agent
            if leftAgentId > rightAgentId:
                temp = leftAgentId
                leftAgentId = rightAgentId
                rightAgentId = temp

            neighbourAgents[leftAgentId].append(rightAgentId)
            neighbourAgents[rightAgentId].append(leftAgentId)
            neighbourConstraintCosts[leftAgentId][rightAgentId] = elementList[i].attrib["reference"]
            neighbourConstraintCosts[rightAgentId][leftAgentId] = elementList[i].attrib["reference"]
            variable = str(leftAgentId) + " " + str(rightAgentId)
            problem.VariableRelation[elementList[i].attrib['reference']] = variable

        for agentId in problem.agentNames.keys():
            temp = neighbourAgents[agentId]
            test = []
            for i in temp:
                test.append(int(i))
            problem.neighbourAgents[agentId] = test
            costNames = []
            for i in range(0,len(temp)):
                costNames.append(neighbourConstraintCosts[agentId][test[i]])
            problem.agentConstraintCosts[agentId] = costNames

        return True

            


    def parseRelations(self,element,problem):
        if element ==None:
            return False

        nbRelations=-1
        try:
            nbRelations = int(element.attrib['nbRelations'])
        except:
            return False

        elementList = list(element)
        if nbRelations != len(elementList):
            print("nbRelations!=elementList.size()")
            return False

        for i in range(0,nbRelations):
            arity = int(elementList[i].attrib["arity"])
            if arity != 2:
                print("arity!=2")
                return False

            cost = []
            if self.problemType == "DisCSP":
                print("problemType is DisCSP!")

            else:
                cost = self.parseConstraintCost(elementList[i].text,problem,elementList[i].attrib["name"])
                nbTuples = int(elementList[i].attrib["nbTuples"])
                if nbTuples != len(cost):
                    print("nbValues!=cost length")
                    return False

            problem.costs[elementList[i].attrib['name']] = cost
            mi = cost[0]
            for j in range(0,len(cost)):
                if mi > cost[j]:
                    mi = cost[j]
            
            problem.relationCost[elementList[i].attrib['name']] = mi
        return True


    def parseConstraintCost(self,costStr,problem,relation):
        items = costStr.split("|")
        rowsize = 0
        colsize = 0
        costParts = []
        valuePairParts = {}
        index=0
        for i in range(0,len(items)):
            index = items[i].index(':')
            costParts.append(items[i][0:index])
            index2 = items[i].index(' ')
            
            temp = int(items[i][index + 1:index2])
            rowsize = rowsize if rowsize > temp else temp
            temp = int(items[i][index2+1:])
            colsize = colsize if colsize > temp else temp

            valuePairParts[items[i][index+1:]] = i

        valuePairPartsKeyArray = list(valuePairParts.keys())
        valuePairPartsKeyArray.sort(key=lambda arr:(int(arr.split(' ')[0]),int(arr.split(' ')[1])))
        costs = [0] * len(items)
        mi = 100000
        valuePair = ""
        #print(valuePairPartsKeyArray)
        for valuePairPartsKey in valuePairParts.keys():
            index3 = valuePairPartsKey.index(' ')
            row = int(valuePairPartsKey[0:index3])
            col = int(valuePairPartsKey[index3+1:])
            pos = (row-1)*colsize + (col - 1)

            costs[pos] = int(costParts[valuePairParts[valuePairPartsKey]])
            if mi > costs[pos]:
                mi = costs[pos]
                valuePair = valuePairPartsKey

        problem.VariableValue[relation] = valuePair
        return costs

     

    def parseVariables(self,element,problem,agentNameIds):
        if element ==None:
            return False

        nbVariables = -1
        try:
            nbVariables = int(element.attrib['nbVariables'])
        except:
            return False

        elementList = list(element)
        if nbVariables != len(elementList):
            print("nbVariables!=elementList.size()")
            return False

        if nbVariables != len(problem.agentNames):
            print("nbVariables!=problem.agentCount，要求每个agent中只包含一个variable")
            return None

        variableNameAgentIds = {}
        for i in range(0,nbVariables):
            agentId = agentNameIds[elementList[i].attrib["agent"]]
            variableNameAgentIds[elementList[i].attrib["name"]] = agentId
            problem.agentDomains[agentId] = elementList[i].attrib["domain"]

        return variableNameAgentIds



    def parseDomains(self,element,problem):
        if element ==None:
            return False

        nbDomains = -1
        try:
            nbDomains = int(element.attrib['nbDomains'])
        except:
            return False

        elementList = list(element)
        if nbDomains != len(elementList):
            print("nbDomains!=elementList.size()")
            return False

        for i in range(0,nbDomains):
            domain = self.parseFromTo(elementList[i].text)
            
            nbValues = int(elementList[i].attrib['nbValues'])
            if nbValues != len(domain):
                print("nbValues!=domain.length")
                return False
            problem.domains[elementList[i].attrib["name"]] = domain

        return True


    def parseFromTo(self,fromToStr):
        fo = -1
        to = -1
        separator = ".."
        fo = int(fromToStr.split("..")[0])
        to = int(fromToStr.split("..")[1])

        ret = []
        for i in range(0,to):
            ret.append(i+fo)

        return ret



    def parseAgents(self,element,problem):
        if element == None:
            return None
        nbAgents = -1
        try:
            nbAgents = int(element.attrib['nbAgents'])
        except:
            print("errpr")
            return None

        elementList = list(element)
        if nbAgents != len(elementList):
            print("nbAgents!=elementList.size()")
            return None
        
        agentNameIds = {}
        try:
            for i in range(0,nbAgents):
                idi = int(elementList[i].attrib['id'])
                name = elementList[i].attrib['name']
                agentNameIds[name] = idi
                problem.agentNames[idi] = name

        
        except :
            return None

        return agentNameIds



        