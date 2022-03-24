###接口类

from abc import abstractmethod, ABCMeta


class ScoringHeuristic(metaclass=ABCMeta):
	
    

    
    @abstractmethod
    def getScores(self):
        """定义接口名，但不需要实现其功能，由继承此类的子类实现"""
        pass

    @abstractmethod
    def getScores_two(self,nodeID,dfsview):
        """定义接口名，但不需要实现其功能，由继承此类的子类实现"""
        pass

    @abstractmethod
    def getScores_three(self,orderingView):
        """定义接口名，但不需要实现其功能，由继承此类的子类实现"""
        pass

    
