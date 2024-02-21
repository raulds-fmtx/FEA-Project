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
        l1 = f'Node #{self.__num} at x = {self.__loc}:\n'
        l2 = f'\tV({self.__loc}) = {self.__shear_app}\n'
        l3 = f'\tM({self.__loc}) = {self.__moment_app}\n'
        output = l1 + l2 + l3
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
    __ElementK = None # Stiffness matrix
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
        l1 = f'Element of Node #{self.__lNode.get_num()} and Node #{self.__rNode.get_num()}:\n'
        l2 = f'L = {self.__length}\n'
        l3 = f'K = {self.__K}\n'
        l4 = str(self.__lNode)
        l5 = str(self.__rNode)
        output = l1 + l2 + l3 + l4 + l5
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
        if self.__ElementK == None:
            L = self.__length
            K1 = np.array([12/L**3,6/L**2,-12/L**3,6/L**2],dtype=float)
            K2 = np.array([6/L**2,4/L,-6/L**2,2/L],dtype=float)
            K3 = np.array([-12/L**3,-6/L**2,12/L**3,-6/L**2])
            K4 = np.array([6/L**2,2/L,-6/L**2,4/L],dtype=float)
            self.__ElementK = EI * np.array([[K1],[K2],[K3],[K4]],dtype=float)
        return self.__ElementK
    def get_dofArr(self):
        '''Getter __dofArr : Returns private member __dofArr'''
        return self.__dofArr

class Beam:
    # private members
    __E = None # Young's Modulus
    __h = None # Beam height
    __w = None # Beam width
    __L = None # Beam Length
    __EI = None # EIzz
    __nodeCount = None # number of Nodes
    __memberList = None # Ordered list of member elements
    __globalK = None # Global Stifness Matrix, (rows,cols) ordered by dof
    __globalFbc = None # Global Boundary Conditions, rows ordered by dof
    # private methods
    def __init__(self,E,h,w,memberList,nodeCount):
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
        self.__E = E
        self.__h = h
        self.__w = w
        self.__L = sum([i.get_length() for i in memberList])
        self.__EI = E*w*h**3 / 12
        self.__nodeCount = nodeCount
        self.__memberList = memberList
    def __str__():
        return 
    # public methods
    def assembleGlobalStiffnessMatrix(self):
        return self.__globalK
    def imposeConstraints(self,dofList):
        return self.__globalK
    def setGlobalFbc(self,BCList):
        return
    def solver(self):
        nodalDisp = None
        return nodalDisp

