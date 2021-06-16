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
clueDensitySquare = 0
clueDensityVisibility = 1

nbInstances = 50

# Record runtimes
solTimes = np.empty((nbInstances))

# Settings
useVIs = 1

# Iterate through random seeds to geenrate different problem instances
for s in range(0,nbInstances):
    seed=s
    random.seed(seed)              # Set random seed for reproducibility
    
    # Parameter to set whether or not valid inequalities should be used
    '''[1 Element visible, all elements visible, bounds on tallest element position]'''
    if useVIs == True:
        useVI = [True, True, True]
    else:
        useVI = [False, False, False]
    
     # Output (sub-)directory defintions for output (create if necessary)
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'Results/')
    results_sub_dir = os.path.join(results_dir, 'Setting_S' + str(size) + '_VI' + str(useVIs) + '/')
    if not os.path.isdir(results_sub_dir):
        os.makedirs(results_sub_dir)
    
    # Generate problem instance
    cluesSquare, cluesVisReq = generateData(size, clueDensitySquare, clueDensityVisibility)

    # Solve problem instance
    height_sol, runtime = solveSkyscrapersPuzzle(size, cluesSquare, cluesVisReq, useVI)
    solTimes[s] = runtime
    
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
    plt.savefig(results_sub_dir + 'Skyscrapers_sol_S' + str(size) + '_R' + str(seed) + '_VI' + str(useVIs) + '.png')
    plt.show()

