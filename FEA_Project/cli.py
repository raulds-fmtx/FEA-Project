"""CLI interface for project_name project."""

from FEA_Project.read import *
import sys

def main():
    """
    The main function executes on commands:
    `python -m FEA_Project inFile.txt outFile.txt`.
    """
    
    # Open input and output files
    inFile = open("./input/" + sys.argv[1], "r")
    outFile = open("./output/" + sys.argv[2], "w")
    
    # Process data
    elementList, numNodes = readMesh(inFile,outFile) # list of elements and number of nodes
    E,h,w = readProperties(inFile,outFile) # properties of the beam
    Beam1 = Beam(E,h,w,numNodes,elementList) # construct beam
    constraintList = readConstraints(inFile,outFile,numNodes) # list of constraints
    loadArr = readLoads(inFile,outFile,numNodes) # array of applied loads at each dof

    # Close files
    inFile.close()
    outFile.close()
    
    