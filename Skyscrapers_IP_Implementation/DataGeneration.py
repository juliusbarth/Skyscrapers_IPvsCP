# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 18:08:11 2020

@author: jfb2444
"""
import numpy as np
import random
from random import choice, shuffle
from copy import deepcopy
   
# Source: https://rosettacode.org/wiki/Random_Latin_Squares#Python

# Define functions for random Latin Square generation
def rls(n):
    if n <= 0:
        return []
    else:
        symbols = list(range(n))
        square = _rls(symbols)
        return _shuffle_transpose_shuffle(square)

def _shuffle_transpose_shuffle(matrix):
    square = deepcopy(matrix)
    shuffle(square)
    trans = list(zip(*square))
    shuffle(trans)
    return trans
 
def _rls(symbols):
    n = len(symbols)
    if n == 1:
        return [symbols]
    else:
        sym = choice(symbols)
        symbols.remove(sym)
        square = _rls(symbols)
        square.append(square[0].copy())
        for i in range(n):
            square[i].insert(i, sym)
        return square

def _check(square):
    transpose = list(zip(*square))
    assert _check_rows(square) and _check_rows(transpose), \
        "Not a Latin square"
 
def _check_rows(square):
    if not square:
        return True
    set_row0 = set(square[0])
    return all(len(row) == len(set(row)) and set(row) == set_row0
               for row in square)
'''
def writeDataFile(size, cluesSquare, cluesVisReq):
    dataFile = open("myfile.txt","w")
    dataFile.write("n = ",size)
    dataFile.write("n = ",size)
    dataFile.close() #to change file access modes 
'''    

def generateData(size, clueDensitySquare, clueDensityVisibility):
    
    #Generate the square randomly. Source: https://rosettacode.org/wiki/Random_Latin_Squares#Python
    print("\nGenerating Random Latin Square\n")
    square = rls(size)
    _check(square)
    values = np.zeros((size, size))
    cluesSquare = np.empty((size, size))
    cluesSquare[:] = np.NaN
    for i in range(0,size):
        for j in range(0,size):
            values[i][j] = square[i][j] 
            if random.uniform(0,1) < clueDensitySquare:
                cluesSquare[i][j] = values[i][j]    
    visReq = np.zeros((size, 4))
    print(values)
    
    # Visibilty variables
    vis = np.ones((size, size, 4))
    
    visReq = np.empty((size, 4))
    cluesVisReq = np.empty((size, 4))
    cluesVisReq[:] = np.NaN
    
    # Check visibility for North = 0, South = 1, West = 2 and East = 3 directions
    for i in range(0,size):
        for j in range(0,size):
            for k in range(0,i):
                if values[k][j] > values[i][j]:
                    vis[i][j][0] = 0    # Not visible from north
            for k in range(i,size):
                if values[k][j] > values[i][j]:
                    vis[i][j][1] = 0       # Not visible from south
            for l in range(0,j):
                if values[i][l] > values[i][j]:
                    vis[i][j][2] = 0    # Not visible from west
            for l in range(j,size):
                if values[i][l] > values[i][j]:
                    vis[i][j][3] = 0       # Not visible from east
           
    for k in range(0,size):
        visReq[k][0] = sum(vis[i][k][0] for i in range(0,size))
        visReq[k][1] = sum(vis[i][k][1] for i in range(0,size))
        visReq[k][2] = sum(vis[k][j][2] for j in range(0,size))
        visReq[k][3] = sum(vis[k][j][3] for j in range(0,size))
        if random.uniform(0,1) < clueDensityVisibility:
            cluesVisReq[k][0] = sum(vis[i][k][0] for i in range(0,size))
        if random.uniform(0,1) < clueDensityVisibility:
            cluesVisReq[k][1] = sum(vis[i][k][1] for i in range(0,size))
        if random.uniform(0,1) < clueDensityVisibility:
            cluesVisReq[k][2] = sum(vis[k][j][2] for j in range(0,size))
        if random.uniform(0,1) < clueDensityVisibility:
            cluesVisReq[k][3] = sum(vis[k][j][3] for j in range(0,size))
                
    return cluesSquare, cluesVisReq