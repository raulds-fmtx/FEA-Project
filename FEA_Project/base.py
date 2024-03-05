"""
FEA-Project base module.

This is the principal module of the FEA-Project project.
    Contains classes and objects.

"""

import numpy as np
import copy as cp

class Node:
    # private members
    __loc = None # x-coordinate of the Node
    __num = None # ordinal number of the Node
    # private methods
    def __init__(self,num : int,loc : int):
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
    def getLoc(self): return self.__loc
    def getNum(self): return self.__num

class Element: 
    # private members
    __num = None # Number associated with element
    __lNode = None # Node on negative end of the element
    __rNode = None  # Node on positive end of the element
    __length = None # length of the Node
    __dofArr = None # Array of dof corresponding to stifness matrix
    # private methods
    def __init__(self,num : int,lNode : Node,rNode : Node):
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
        self.__length = rNode.getLoc() - lNode.getLoc()
        dofL = [2*(lNode.getNum()-1)+1,2*(lNode.getNum()-1)+2,2*(rNode.getNum()-1)+1,2*(rNode.getNum()-1)+2]
        self.__dofArr = np.array([[(dofL[0],dofL[0]),(dofL[0],dofL[1]),(dofL[0],dofL[2]),(dofL[0],dofL[3])],
                                  [(dofL[1],dofL[0]),(dofL[1],dofL[1]),(dofL[1],dofL[2]),(dofL[1],dofL[3])],
                                  [(dofL[2],dofL[0]),(dofL[2],dofL[1]),(dofL[2],dofL[2]),(dofL[2],dofL[3])],
                                  [(dofL[3],dofL[0]),(dofL[3],dofL[1]),(dofL[3],dofL[2]),(dofL[3],dofL[3])]],dtype=tuple)
    def __str__(self):
        '''String Format'''
        output = f'Element #{self.__num} of Node #{self.__lNode.getNum()} and Node #{self.__rNode.getNum()}, Length = {self.__length}\n'
        return output
    # getter methods
    def getNum(self): return self.__num
    def getLNode(self): return self.__lNode
    def getRNode(self): return self.__rNode
    def getLength(self): return self.__length
    def getDOFArr(self): return self.__dofArr
    # As Defined in Part 2
    def getElementK(self,EI : float):
        '''Calculates Element Stiffness Matrix K
        
        Return
        ------
        self.__ElementK : np.ndarray, shape = (2,2), dtype = float
            Stifness Matrix of the element
        '''
        L = self.__length
        K1 = np.array([12/L**3,6/L**2,-12/L**3,6/L**2],dtype=float)
        K2 = np.array([6/L**2,4/L,-6/L**2,2/L],dtype=float)
        K3 = np.array([-12/L**3,-6/L**2,12/L**3,-6/L**2],dtype=float)
        K4 = np.array([6/L**2,2/L,-6/L**2,4/L],dtype=float)
        ElementK = EI * np.array([[K1][0],[K2][0],[K3][0],[K4][0]],dtype=float)
        return ElementK

class Beam:
    # private members
    __L = None # Beam Length
    __EI = None # EIzz
    __nodeCount = None # number of Nodes
    __memberList = None # Ordered list of member elements
    __globalK = None # globalK
    # private methods
    def __init__(self,E : float,h : float,w : float,numNodes : int,memberList : list):
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
        self.__L = sum([i.getLength() for i in memberList])
        self.__EI = E*w*h**3 / 12
        self.__nodeCount = numNodes
        self.__memberList = memberList
        self.__globalK = self.__assembleGlobalStiffnessMatrix__()
    def __str__(self):
        output = 'Beam of '
        for i in self.__memberList :
            output += f'Element #{i.getNum()} '
        output += '\n'
        return output
    def __assembleGlobalStiffnessMatrix__(self):
        '''Assembles global stiffness matrix from data obtained from each element
        
        Return
        ------
        globalK = np.ndarray(), shape = (__nodeCount*2,__nodeCount*2), dtype = float
            unconstrained globalK matrix
        '''
        # Create empty global stiffness matrix
        globalK = np.zeros((self.__nodeCount*2,self.__nodeCount*2),dtype=float)
        
        # Cycle through adding elementK matrix to globalK matrix
        for element in self.__memberList:
            # Get element information
            elementK = element.getElementK(self.__EI)
            elementK_coords = element.getDOFArr()
            # Cycle through arrays
            for i in range(elementK.shape[0]) :
                for j in range(elementK.shape[1]) :
                    dof1, dof2 = elementK_coords[i,j]
                    globalK[dof1-1,dof2-1] += elementK[i,j]
        
        # Return globalK
        return globalK
    # getter methods
    def getglobalK(self) : return self.__globalK # returns unconstrained globalK matrix
    def getEI(self) : return self.__EI # returns EIzz
    def getElementList(self) : return self.__memberList # returns memberList
    # public methods
    def imposeConstraints(self,constraintList : list):
        '''Adds 1e30 along indices at locations on the diagonal specified by constraintList
        
        Parameters
        ----------
        constraintList : list
            list of booleans where the index refers to the position upon the diagonal of the globalK matrix where a constraint may be imposed.
            
        Return
        ------
        globalK : np.ndarray, shape = (__nodeCount*2,__nodeCount*2), dtype = float
            constrained global stiffness matrix
        '''
        # Copy globalK
        globalK = cp.copy(self.__globalK)
        # Add 1e30 to diagonal as specified by constraintList
        for i in range(len(constraintList)) :
            if constraintList[i] :
                globalK[i,i] += 1e30
    
        return globalK
    def solver(self,constraintList: list, loadArr : np.ndarray):
        '''Solves for nodal displacements
        
        Parameters
        ----------
        constraintList : list
            list of booleans where the index refers to the position upon the diagonal of the globalK matrix where a constraint may be imposed.
        loadArr : np.ndarray, shape = (__nodeCount*2,1), dtype = float
            vector of the applied loads
        
        Return
        ------
        nodalDisp : np.ndarray, shape = (__nodeCount*2,1), dtype = float
            vector of the nodal displacements
        '''
        # Get constrained global K matrix
        K = self.imposeConstraints(constraintList)
        # Solve for nodal displacements
        nodalDisp = np.linalg.solve(K,loadArr)
        
        return nodalDisp

