# -*- coding: utf-8 -*-
"""
Created on Tue May 12 22:08:55 2020

@author: jfb2444
"""

###############################################################################
################################  Imports #####################################
###############################################################################
import os
from datetime import datetime
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator
from DataGeneration import generateData
from SkyscrapersPuzzle_IP import solveSkyscrapersPuzzle

# Pseudoclear console
for i in range(25):
    print("")
dateTimeObj = datetime.now()
print("New run @", dateTimeObj)

# Data
size = 8
cluesVisReq = np.empty((size, 4))
cluesSquare = np.empty((size, size))
cluesSquare[:] = np.NaN

visNorth	= [4,-1,-1,5,2,-1,-1,4]; 	
visSouth 	= [-1,-1,2,-1,-1,4,3,-1]; 	
visWest	= [-1,-1,-1,3,6,3,3,-1]; 	
visEast	= [-1,5,-1,4,-1,1,3,-1];	
	
for i in range(0,size):
    cluesVisReq[i][0] = visNorth[i]
    cluesVisReq[i][1] = visSouth[i]
    cluesVisReq[i][2] = visWest[i]
    cluesVisReq[i][3] = visEast[i]
    for d in range(0,4):
        if cluesVisReq[i][d] == -1:
            cluesVisReq[i][d] = np.NaN
          
cluesSquare = [	[-1,-1,-1,-1,-1,-1,-1,-1],
 				[-1,-1,-1,-1,2,-1,-1,-1],
 				[-1,-1,-1,-1,-1,-1,-1,-1],
 				[-1,-1,-1,-1,-1,2,-1,4],
 				[-1,-1,5,6,-1,-1,-1,-1],
 				[-1,-1,1,-1,-1,5,4,-1],
 				[-1,-1,-1,-1,-1,-1,-1,-1],
 				[-1,-1,-1,-1,-1,-1,-1,-1] ]

for i in range(0,size):
    for j in range(0,size):
        if cluesSquare[i][j] == -1:
            cluesSquare[i][j] = np.NaN
        else:
            # -1 because this IP code builds skyscrapers of height 0..n-1 not 1..n,
            # but the supplied data assumes 1..n
            cluesSquare[i][j] = cluesSquare[i][j] - 1 
            

# Settings
useVIs = 1

# Parameter to set whether or not valid inequalities should be used
'''[1 Element visible, all elements visible, bounds on tallest element position]'''
if useVIs == True:
    useVI = [True, True, True]
else:
    useVI = [False, False, False]

 # Output (sub-)directory defintions for output (create if necessary)
script_dir = os.path.dirname(__file__)
results_dir = os.path.join(script_dir, 'Results/')
results_sub_dir = os.path.join(results_dir, 'Setting_S' + str(size) + 'H_VI' + str(useVIs) + '/')
if not os.path.isdir(results_sub_dir):
    os.makedirs(results_sub_dir)

# Solve problem instance
height_sol, runtime = solveSkyscrapersPuzzle(size, cluesSquare, cluesVisReq, useVI)
solTimes = runtime

# 3D barplot of solution
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
posX = np.repeat(list(range(0,size)),size)
posY = (list(range(0,size)) * size)
posZ = np.zeros(size*size)
width = 0.25 
depth = 0.25 
height = list(height_sol.flatten())
colors = plt.cm.jet( np.array(height) / size )

ax1.bar3d(posX, posY, posZ, width, depth, height, color = colors, shade = True)
ax1.set_xlabel('west')
ax1.set_ylabel('south')
ax1.set_zlabel('height')
# Turn off tick labels for x and y coordinates
ax1.set_yticklabels([])
ax1.set_xticklabels([])
# Integer tick marks for z coordinate
ax1.zaxis.set_major_locator(MaxNLocator(integer=True))
# Tight layout
plt.tight_layout()
# Save and display figure
plt.savefig(results_sub_dir + 'Skyscrapers_sol_S' + str(size) + 'H_VI' + str(useVIs) + '.png')
plt.show()

