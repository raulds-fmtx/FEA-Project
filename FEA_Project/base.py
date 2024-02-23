"""
FEA-Project base module.

This is the principal module of the FEA-Project project.
    Contains classes and objects.

"""

import numpy as np

class Node:
    # private members
    __loc = None # x-coordinate of the Node
    __num = None # ordinal number of the Node
    # private methods
    def __init__(self,num,loc):
        '''Constructor
        
        Parameters
        ----------
        loc : float
            x-coordinate of the Node.
        num : int
            ordinal number associated with the Node.
        '''
        self.__loc = loc
        self.__num = num
    def __str__(self):
        '''String Format'''
        output = f'Node #{self.__num} at x = {self.__loc}:\n'
        return output
    # getter methods
    def get_loc(self):
        '''Getter __loc : Returns private member __loc'''
        return self.__loc
    def get_num(self):
        '''Getter __num : Returns private member __num'''
        return self.__num

class Element: 
    # private members
    __num = None # Number associated with element
    __lNode = None # Node on negative end of the element
    __rNode = None  # Node on positive end of the element
    __length = None # length of the Node
    __dofArr = None # Array of dof corresponding to stifness matrix
    # private methods
    def __init__(self,num,lNode,rNode):
        '''Constructor
        
        Parameters
        ----------
        num : int
            Ordinal number associated with element
        lNode : Node
            Left Node of the element.
        rNode : Node
            Right Node of the element.
        '''
        self.__num = num
        self.__lNode = lNode
        self.__rNode = rNode
        self.__length = rNode.get_loc() - lNode.get_loc()
        dofL = [2*(lNode.get_num()-1)+1,2*(lNode.get_num()-1)+2,2*(rNode.get_num()-1)+1,2*(rNode.get_num()-1)+2]
        self.__dofArr = np.array([[(dofL[0],dofL[0]),(dofL[0],dofL[1]),(dofL[0],dofL[2]),(dofL[0],dofL[3])],
                                  [(dofL[1],dofL[0]),(dofL[1],dofL[1]),(dofL[1],dofL[2]),(dofL[1],dofL[3])],
                                  [(dofL[2],dofL[0]),(dofL[2],dofL[1]),(dofL[2],dofL[2]),(dofL[2],dofL[3])],
                                  [(dofL[3],dofL[0]),(dofL[3],dofL[1]),(dofL[3],dofL[2]),(dofL[3],dofL[3])]],dtype=tuple)
    def __str__(self):
        '''String Format'''
        output = f'Element #{self.__num} of Node #{self.__lNode.get_num()} and Node #{self.__rNode.get_num()}, Length = {self.__length}\n'
        return output
    # getter methods
    def get_num(self):
        '''Getter __num : Returns private member __num'''
        return self.__num
    def get_lNode(self):
        '''Getter __lNode : Returns private member __lNode'''
        return self.__lNode
    def get_rNode(self):
        '''Getter __rNode : Returns private member __rNode'''
        return self.__rNode
    def get_length(self):
        '''Getter __length : Returns private member __length'''
        return self.__length
    def getElementK(self,EI):
        '''Calculates Element Stiffness Matrix K
        
        Return
        ------
        self.__ElementK : np.array (4x4)
            Stifness Matrix of the element
        '''
        L = self.__length
        K1 = np.array([12/L**3,6/L**2,-12/L**3,6/L**2],dtype=float)
        K2 = np.array([6/L**2,4/L,-6/L**2,2/L],dtype=float)
        K3 = np.array([-12/L**3,-6/L**2,12/L**3,-6/L**2])
        K4 = np.array([6/L**2,2/L,-6/L**2,4/L],dtype=float)
        ElementK = EI * np.array([[K1],[K2],[K3],[K4]],dtype=float)
        return ElementK
    def get_dofArr(self):
        '''Getter __dofArr : Returns private member __dofArr'''
        return self.__dofArr

class Beam:
    # private members
    __L = None # Beam Length
    __EI = None # EIzz
    __nodeCount = None # number of Nodes
    __memberList = None # Ordered list of member elements
    __globalK = None # globalK
    # private methods
    def __init__(self,E,h,w,numNodes,memberList):
        '''Constructor
        
        Parameters
        ----------
        E : float
            Young's Modulus
        h : float
            Height of the beam.
        w : float
            Width of the beam.
        memberList : Element[]
            Ordered list of all member elements of the beam.
            Ordered by number of the Element number.
        nodeCount : int
            number of Nodes making up the beam.
        '''
        self.__L = sum([i.get_length() for i in memberList])
        self.__EI = E*w*h**3 / 12
        self.__nodeCount = numNodes
        self.__memberList = memberList
        self.__globalK = np.zeros((numNodes,numNodes),dtype=float)
    def __str__(self):
        output = 'Beam of '
        for i in self.__memberList :
            output += f'Element #{i.get_num()} '
        output += '\n'
        return output
    # public methods
    def assembleGlobalStiffnessMatrix(self):
        return self.__globalK
    def imposeConstraints(self,constraintList):
        return self.__globalK
    def solver(self,loadArr):
        nodalDisp = None
        return nodalDisp

