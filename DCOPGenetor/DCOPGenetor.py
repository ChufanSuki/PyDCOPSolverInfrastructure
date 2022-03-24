from xml.etree import ElementTree as ET
from prettyXml import prettyXml
import os

from GeneateRandomGraph import UndirectedGraph

class DCOPGenetor:
    fixKeys ='p1'
    nbHeaderLine=4

    def __init__(self,saveDir,constraintsModel,nbInstances,nbAgents,domainSize,minP1,maxP1,stepP1,minCost,maxCost):
        self.__path=saveDir
        self.__nbInstances = nbInstances
        self.__constraintsModel = constraintsModel
        
        self.__nbAgents = nbAgents
        self.__domainSize = domainSize
        self.__minP1 = minP1
        self.__maxP1 = maxP1
        self.__minCost = minCost
        self.__maxCost = maxCost
        self.__typeOfBenchmark = "RandomDCOP"
        self.__model = "Simple"




    def generate(self):
        assert self.__minP1 <= self.__maxP1 , "minimum densty must be less or equal than maximum density"
        assert self.__minP1 > 0 and self.__maxP1 <= 100 , "the density must be between [0,100]"
        assert self.__nbAgents * (self.__nbAgents -1)/2 * self.__minP1 /100 >= self.__nbAgents -1 , "\nWe can not generate a connected graph with the density " + str(self.__minP1) + " such that n="+ str(self.__nbAgents)
        

        for i in range (0,self.__nbInstances):
            instances = self.generateInstance(self.__nbInstances,self.__minP1)
            prettyXml(instances, '\t', '\n')
            tree = ET.ElementTree(instances) 
            path = self.__path + '/' + str(self.__nbInstances) + '_' + str(self.__nbAgents) + '_' +str(self.__minP1)
            folder = os.path.exists(path)
            if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
                os.makedirs(path) 
            filename = path + "/RandomDCOP_" + str(self.__nbAgents) + "_" + str(self.__domainSize) + "_" + str(i+1) + ".xml"
            tree.write(filename,encoding = "UTF-8",xml_declaration=True)
        

    
    def generateInstance(self , nbOfInstance , p1):
        instance = ET.Element("instance")
        instance.append(self.getPresentation(nbOfInstance,"DCOP"))
        graph = UndirectedGraph(self.__nbAgents,p1)
        instance.append(graph.getAgents())
        instance.append(graph.getDomaines(self.__domainSize))
        instance.append(graph.getVariables())
        nbConstraint = graph.getNbEdges()
        nbTuples = self.__domainSize * self.__domainSize
        if self.__constraintsModel == "TKC":
            constraints = graph.getConstraints()
            constraints.set("initialCost", str(self.__minCost))
            constraints.set("maximalCost", "infinity")
            instance.append(constraints)
            instance.append(graph.getSoftRelations(False, self.__domainSize, 0, self.__minCost, self.__maxCost))
            instance.append(self.getGuiPresentation(nbOfInstance, p1, nbConstraint, nbTuples))



        
        return instance


    def getPresentation(self,nbOfInstance,type1):
        presentation = ET.Element("presentation")
        presentation.set("name", "instance" + str(nbOfInstance))
        presentation.set("type", type1)
        presentation.set("benchmark", self.__typeOfBenchmark)
        presentation.set("model", self.__model)
        presentation.set("constraintModel", self.__constraintsModel)
        presentation.set("format", "XDisCSP 1.0")
        return presentation

    def getGuiPresentation(self,nbOfInstance, p1, nbConstraint, nbTuples):
        presentation = ET.Element("GuiPresentation")
        presentation.set("type", "DCOP")
        presentation.set("benchmark", self.__typeOfBenchmark)
        presentation.set("name", "instance" + str(nbOfInstance))
        presentation.set("model", self.__constraintsModel)
        presentation.set("nbAgents", str(self.__nbAgents))
        presentation.set("domainSize", str(self.__domainSize))
        presentation.set("density", str(p1))
        presentation.set("tightness", "0")
        presentation.set("nbConstraints", str(nbConstraint))
        presentation.set("nbTuples", str(nbTuples))
        return presentation
        


if __name__ == '__main__':
    g = DCOPGenetor('kk','TKC',1,5,10,40,80,30,0,100)
    g.generate()
    