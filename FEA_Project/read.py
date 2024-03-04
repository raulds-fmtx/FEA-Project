from FEA_Project.base import *

def readMesh(inFile,outFile) :
    '''Echo prints collected and formatted data from inFile into outFile
        returns a tuple containting a list of Elements
        
        Parameters
        ----------
        inFile : file object
            file object enabling readMesh() to access the given file in the ./input directory
        outFile : file object
            file object enabling readMesh() to echo print the formatted data
            
        Return
        ------
        EList : list<Element>
            A list of elements
        
        '''
    nodeList = [] # List of Nodes
    elementList = [] # List of Elements
    
    # Get Number of Nodes
    line1 = inFile.readline().strip().split()
    numNodes = int(line1[0])
    numElements = int(line1[1])
    
    # Echo Print Number of Nodes
    outFile.write(f"Number of Nodes: {numNodes}\n")
    outFile.write(f"Number of Elements: {numElements}\n\n")
    
    # Get Nodes
    outFile.write("Nodes:\n")
    for i in range(numNodes) :
        lineNode = inFile.readline().strip().split() # read line
        nodeList.append(Node(int(lineNode[0]),int(lineNode[1]))) # add node to list
        # Echo Print Nodes
        outFile.write(str(nodeList[i]))
    outFile.write("\n")

    # Get Elements
    inFile.readline().strip().split() # Throw out junk line
    outFile.write("Elements:\n")
    for i in range(numElements) :
        lineElement = inFile.readline().strip().split() # read line
        elementList.append(Element(int(lineElement[0]),nodeList[int(lineElement[1])-1],nodeList[int(lineElement[2])-1])) # add element to list
        # Echo Print Elements
        outFile.write(str(elementList[i]))
    inFile.readline().strip().split() # Throw out junk line
    outFile.write("\n")
    
    return elementList, numNodes

def readProperties(inFile,outFile) :
    '''Echo prints collected and formatted data from inFile into outFile
        returns a tuple of properties (Young's Modulus, height, width)
        
        Parameters
        ----------
        inFile : file object
            file object enabling readProperties() to access the given file in the ./input directory
        outFile : file object
            file object enabling readProperties() to echo print the formatted data
            
        Return
        ------
        (E,h,w) : tuple<float>
            tuple of beam properties (Young's Modulus, height, width)

        '''
    # Get properties
    line = inFile.readline().strip().split()
    E = float(line[0])
    h = float(line[1])
    w = float(line[2])
    
    # Echo print properties
    outFile.write("Beam Properties:\n")
    outFile.write(f"E = {E}\n")
    outFile.write(f"h = {h}\n")
    outFile.write(f"w = {w}\n\n")
    
    # Read junk line
    inFile.readline().strip().split()
    
    return E,h,w

def readConstraints(inFile,outFile,numNodes : int) :
    '''Echo prints collected and formatted data from inFile into outFile
        returns a boolean lists
        
        Parameters
        ----------
        inFile : file object
            file object enabling readConstraints() to access the given file in the ./input directory
        outFile : file object
            file object enabling readConstraints() to echo print the formatted data
        numNodes : int
            number of nodes in the beam
            
        Return
        ------
        listConstraints : list<Boolean>
            list of booleans where True at index i corresponds to a constraint at the ith degree of freedom

        '''
    # Create constraint list defaulted to number of dof
    constraintList = [False for i in range(numNodes*2)]
    # Read junk line
    inFile.readline().strip().split()
    # Read constraints
    consts = inFile.readline().strip().split()
    # map constraints into constraint list
    for i in consts :
        constraintList[int(i)-1] = True
    # Read junk line
    inFile.readline().strip().split()
    # echo print constraints
    outFile.write('List of DOF set to 0:\n')
    for i in consts :
        outFile.write(f'{i} ')
    outFile.write('\n\n')
    
    return constraintList

def readLoads(inFile,outFile,numNodes : int) :
    '''Echo prints collected and formatted data from inFile into outFile
        returns a numpy array of applied loads at each dof
        
        Parameters
        ----------
        inFile : file object
            file object enabling readProperties() to access the given file in the ./input directory
        outFile : file object
            file object enabling readProperties() to echo print the formatted data
        numNodes : int
            number of nodes in the beam
            
        Return
        ------
        LoadArr : np.array, shape = (numNodes*2,1), dtype = float
            numpy array of applied loads at each dof

        '''
    # Create LoadArr
    LoadArr = np.zeros((numNodes*2,1),dtype=float)
    # get number of Point Loads
    numLoads = int(inFile.readline().strip().split()[0])
    # Get number of Point Loads
    outFile.write("Point Loads:\n")
    for i in range(numLoads) :
        lineLoad = inFile.readline().strip().split() # read line
        LoadArr[int(lineLoad[0])-1,0] = float(lineLoad[1]) # add load to LoadArr
        # Echo Print Nodes
        outFile.write(f'{lineLoad[1]} at DOF {lineLoad[0]}\n')
    outFile.write("\n")
    
    return LoadArr

def reportResults(outFile,nodalDisp : np.ndarray,numNodes: int) :
    '''Writes formatted nodal displacement data into outFile
        
        Parameters
        ----------
        outFile : file object
            file object enabling writeDisps() to record the formatted data
        nodalDisp : np.ndarray, shape = (numNodes*2,1), dtype = float
            Array of calculated nodal displacements
        numNodes : int
            Number of nodes in the beam
            
        Return
        ------
        LoadArr : np.array, shape = (numNodes*2,1), dtype = float
            numpy array of applied loads at each dof
        '''
    
    # Write header
    outFile.write('Nodal Displacements:\n')
    # Format Nodal Displacements
    for i in range(numNodes):
        disp1 = '{:.4e}'.format(nodalDisp[i*2,0])
        disp2 = '{:.4e}'.format(nodalDisp[i*2+1,0])
        outFile.write('{:>5} {:>11} {:>11}\n'.format(i+1,disp1,disp2))
    