
class Problem:

    KEY_PARENT="parent"
    KEY_PSEUDO_PARENT="pseudo_parent"
    KEY_CHILDREN="children"
    KEY_NEIGHBOUR="neighbour"

    
    def __init__(self):
        self.domains = {}    #记录problem的领域，取值范围
        self.costs = {}      #记录每一个约束的可能取值
        self.agentNames = {}    #记录Agent的名字
        self.agentLevels = {}    #生成DFS树的节点层次等级？？
        self.treeDepth = 0       #生成树的高度
        self.pseudoHeight = 0
        self.agentDomains = {}    #各个Agent的领域
        self.variableDomains = {}   #暂且没有
        self.VariableDomains = {}   #暂且没有
        self.neighbourAgents = {}   #每个Agent的邻居节点
        self.parentAgents = {}     #生成的DFS树的父子节点 a:b,a的父母是b
        self.allParentAgents = {}   #伪树的全部父母节点
        self.childAgents = {}     #生成DS树的孩子节点
        self.allChildrenAgents = {}   #伪树的全部孩子节点
        self.agentConstraintCosts = {}   #各节点之间的约束集合
        self.relationCost = {}     #记录每个连接关系矩阵中的最小代价
        self.agentProperty = {}     #将agent中的评估代价作为其属性，暂时没用
        self.VariableRelation = {}    #对应的relation variable pair
        self.VariableValue ={}      #对应的relation value pair
        self.highNodes = {}    #蚁群算法使用参数，本平台暂时没用
        self.lowNodes = {}      #蚁群算法使用参数，本平台暂时没用
        self.priorities = {}    #蚁群算法使用参数，本平台暂时没用


    



