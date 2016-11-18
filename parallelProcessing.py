import time
from multiprocessing import *

numProcesses = 10

def extract_ppm_header( filename ):
    outFile = open("output.header.txt", "w")
    with open( filename, 'r') as theFile:
        for i in range(4):
            fileInput = theFile.readline()
            outFile.write(fileInput)
    outFile.close()

'''
This function takes as input a filename and the start and number of elements to 
read, it opens the file and extracts all the information.
'''
def read_file( filename, processID, numProcesses ):
    ''' Start with reading the inputs and convert into integers'''
    fileInput = []

    startPoint = 0
    numValues = 0
    with open( filename, 'r') as theFile:
        fileInput = theFile.read().split()

    numPixels = (int(fileInput[7])*int(fileInput[8]))//numProcesses
    numValues = numPixels * 3
    startPoint = processID*numValues
    temp = [int(i) for i in fileInput[10:]]
    
    ''' extract the size number of elemennts from the input starting 
        at position startPoint '''
    input = temp[startPoint:startPoint+numValues]
    return input

def write_file(filename, section):
    ''' given a filename and a list of values, write them to the file.'''
    fout = open(filename, "w")
    for currentIndex in range(len(section)):
        
        fout.write(str(section[currentIndex])+" ")
        if((currentIndex+1) % 15 == 0 ):
            fout.write("\n")
        currentIndex += 1
    fout.close()
    
import os
def collapse_images( filenameBase, nProcesses ):
    '''Assuming that the output files that were processed were named
    <filenameBase><number>.txt, where <filenameBase> and <number> are 
    the parts of the output files containing the sections of the image, 
    collect them all in order and create a complete version of the 
    picture. The final picture is in the file "output.ppm". '''
    outFile = open("output.ppm","w")
    inFile = open("output.header.txt","r")
    
    for i in range(4):
        content = inFile.readline()
        outFile.write(content)
    inFile.close()
    
    os.remove("output.header.txt")
    for i in range(nProcesses):
        filename = filenameBase + str(i) + ".txt"
        inFile = open(filename, "r")
        content = inFile.read()
        outFile.write(content)
        inFile.close()
        os.remove(filename)
        
    outFile.close()

def greyscale_image(pNumber, nProcesses):
    mySection = read_file("bc-flowers.ppm", pNumber, nProcesses )
    i=0
    while i < len(mySection):
        value = (mySection[i] + mySection[i+1] + mySection[i+2]) // 3
        mySection[i] = value
        mySection[i+1] = value
        mySection[i+2] = value
        i = i + 3

    write_file("output"+str(pNumber)+".txt", mySection)

def greyscale_processing():
    extract_ppm_header("bc-flowers.ppm")
    
    processes=[]
    for i in range(1, numProcesses):
        processes.append(Process(target=greyscale_image, args=(i,numProcesses)))
        processes[i-1].start()

    greyscale_image(0,numProcesses)
    for i in range(1, numProcesses):
        processes[i-1].join()

    collapse_images("output", numProcesses)
