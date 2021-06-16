# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 23:03:56 2020

@author: jfb2444
"""

import time
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import math


def solveSkyscrapersPuzzle(size, cluesSquare, cluesVisReq, useVI):
          
    # Create a new model
    print("\n-----------------------------")
    print("Building Model: Skyscrapers Puzzle")
    model = gp.Model("SkyscrapersPuzzle_Model")
    model.Params.OutputFlag = 1
    model.Params.varBranch = 2                  # The default -1 setting makes an automatic choice, depending on problem characteristics. Available alternatives are Pseudo Reduced Cost Branching (0), Pseudo Shadow Price Branching (1), Maximum Infeasibility Branching (2), and Strong Branching (3).

    Rows = range(0,size)
    Columns = range(0,size)
    Values = range(0,size) 
    Directions = range(0,4)     # 0 = North, 1 = South, 2 = West, 3 = East

    # Create variables
    x = model.addVars(Rows, Columns, Values, vtype=GRB.BINARY, obj=0, name="var_CellBinaryValue")
    z = model.addVars(Rows, Columns, vtype=GRB.INTEGER, obj=0, name="var_CellIntegerValue")
    y = model.addVars(Rows, Columns, Directions, vtype=GRB.BINARY, obj=0, name="var_CellIntegerValue")
    v = model.addVars(Rows, Columns, Rows, Columns, vtype=GRB.BINARY, obj=0, name="var_CellIntegerValue")
    
    # Define Constraints
    # One value per cell
    for i in Rows:
        for j in Columns:      
            model.addConstr( sum(x[i,j,k] for k in Values) == 1, "ct_OneValuePerCell[%s,%s]" % (i,j) )
            model.addConstr( sum(k * x[i,j,k] for k in Values) == z[i,j], "ct_CellValue[%s,%s]" % (i,j) )
    
    # Latin Square Constraints
    for k in Values:
        for i in Rows:      
            model.addConstr( sum(x[i,j,k] for j in Values) == 1, "ct_EveryValueOncePerRow[%s,%s]" % (k,i) )
        for j in Columns:      
            model.addConstr( sum(x[i,j,k] for i in Values) == 1, "ct_EveryValueOncePerColumn[%s,%s]" % (k,j) )
                       
    # Visibility Requirements Constraints
    for j in Columns:
        if math.isnan(cluesVisReq[j][0]) == False:
            model.addConstr( sum(y[i,j,0] for i in Rows) == cluesVisReq[j][0], "ct_VisibilityRequirementNorth[%s,%s]" % (j,0) )
        if math.isnan(cluesVisReq[j][1]) == False:
            model.addConstr( sum(y[i,j,1] for i in Rows) == cluesVisReq[j][1], "ct_VisibilityRequirementSouth[%s,%s]" % (j,1) )
    for i in Rows:
        if math.isnan(cluesVisReq[i][2]) == False:
            model.addConstr( sum(y[i,j,2] for j in Columns) == cluesVisReq[i][2], "ct_VisibilityRequirementWest[%s,%s]" % (i,2) )
        if math.isnan(cluesVisReq[i][3]) == False:
            model.addConstr( sum(y[i,j,3] for j in Columns) == cluesVisReq[i][3], "ct_VisibilityRequirementEast[%s,%s]" % (i,3) )
    
    # Visibility of cell in first row/column for each direction
    for j in Columns:
        model.addConstr( y[0,j,0] == 1, "ct_VisibilityFirstRowFromNorth[%s,%s]" % (j,0) )
        model.addConstr( y[size-1,j,1] == 1, "ct_VisibilityFirstRowFromSouth[%s,%s]" % (j,1) )
    for i in Rows:
        model.addConstr( y[i,0,2] == 1, "ct_VisibilityFirstRowFromWest[%s,%s]" % (i,2) )
        model.addConstr( y[size-1,j,3] == 1, "ct_VisibilityFirstRowFromSouth[%s,%s]" % (i,3) )

    # Relative Ordering Constraints
    for i in Rows:
        for j in Columns:
            for k in Rows:
                for l in Columns:
                    model.addConstr( z[k,l]  <= z[i,j] + size * v[i,j,k,l], "ct_RelativeOrderingA[%s,%s,%s,%s]" % (i,j,k,l) )
                    model.addConstr( z[k,l]  >= z[i,j] - size * (1 - v[i,j,k,l]), "ct_RelativeOrderingB[%s,%s,%s,%s]" % (i,j,k,l) )
    
    # Visibility of inner cells from each direction
    # Visibility from north
    for j in range(0,size):
        for i in range(1,size):
            model.addConstr( sum(v[i,j,k,j] for k in range(0,i))  >= 1 - size * y[i,j,0], "ct_VisibilityNorthA[%s,%s]" % (i,j) )
            model.addConstr( sum(v[i,j,k,j] for k in range(0,i))  <= size * (1 - y[i,j,0]), "ct_VisibilityNorthB[%s,%s]" % (i,j) )
    
    # Visibility from south
    for j in range(0,size):
        for i in range(0,size-1):
            model.addConstr( sum(v[i,j,k,j] for k in range(i+1,size))  >= 1 - size * y[i,j,1], "ct_VisibilitySouthA[%s,%s]" % (i,j) )
            model.addConstr( sum(v[i,j,k,j] for k in range(i+1,size))  <= size * (1 - y[i,j,1]), "ct_VisibilitySouthB[%s,%s]" % (i,j) )
            
    # Visibility from west
    for i in range(0,size):
        for j in range(1,size):
            model.addConstr( sum(v[i,j,i,l] for l in range(0,j))  >= 1 - size * y[i,j,2], "ct_VisibilityWestA[%s,%s]" % (i,j) )
            model.addConstr( sum(v[i,j,i,l] for l in range(0,j))  <= size * (1 - y[i,j,2]), "ct_VisibilityWestB[%s,%s]" % (i,j) )
    
    # Visibility from east
    for i in range(0,size):
        for j in range(0,size-1):
            model.addConstr( sum(v[i,j,i,l] for l in range(j+1,size))  >= 1 - size * y[i,j,3], "ct_VisibilityEastA[%s,%s]" % (i,j) )
            model.addConstr( sum(v[i,j,i,l] for l in range(j+1,size))  <= size * (1 - y[i,j,3]), "ct_VisibilityEastB[%s,%s]" % (i,j) )
    
    # Clues
    for i in range(0,size):
        for j in range(0,size):
            if math.isnan(cluesSquare[i][j]) == False:
                val = cluesSquare[i][j]
                model.addConstr( x[i,j,val] == 1, "ct_ClueA[%s,%s]" % (i,j) )
                model.addConstr( z[i,j] == val, "ct_ClueB[%s,%s]" % (i,j) )
                
    # Valid Inequalities
    # First sets of VIs: One skyscraper visible
    if useVI[0] == True:
        for d in range(0,4):
            for i in range(0,size):    
                if cluesVisReq[i][d] == 1:
                    if d == 0:
                        model.addConstr( x[0,i,size-1] == 1, "ct_FirstMaxNorthA[%s]" % (i) )
                        model.addConstr( z[0,i] == size-1, "ct_FirstMaxNorthB[%s]" % (i) )
                    elif d == 1:
                        model.addConstr( x[size-1,i,size-1] == 1, "ct_FirstMaxSouthA[%s]" % (i) )
                        model.addConstr( z[size-1,i] == size-1, "ct_FirstMaxSouthB[%s]" % (i) )
                    elif d == 2:
                        model.addConstr( x[i,0,size-1] == 1, "ct_FirstMaxWestA[%s]" % (i) )
                        model.addConstr( z[i,0] == size-1, "ct_FirstMaxWestB[%s]" % (i) )
                    elif d == 3:
                        model.addConstr( x[i,size-1,size-1] == 1, "ct_FirstMaxEastA[%s]" % (i) )
                        model.addConstr( z[i,size-1] == size-1, "ct_FirstMaxEastB[%s]" % (i) )
            
    # Second sets of VIs: All skyscrapers visible
    if useVI[1] == True:
        for d in range(0,4):
            for i in range(0,size):                
                if cluesVisReq[i][d] == size:
                    if d == 0:
                        for j in range(0,size):
                            model.addConstr( x[j,i,j] == 1, "ct_AllPositionsNorthA[%s,%s]" % (i,j) )
                            model.addConstr( z[j,i] == j, "ct_AllPositionsNorthB[%s,%s]" % (i,j) )
                    elif d == 1:
                        for j in range(0,size):
                            model.addConstr( x[size-1-j,i,j] == 1, "ct_AllPositionsSouthA[%s,%s]" % (i,j) )
                            model.addConstr( z[size-1-j,i] == j, "ct_AllPositionsSouthB[%s,%s]" % (i,j) )
                    elif d == 2:
                        for j in range(0,size):
                            model.addConstr( x[i,j,j] == 1, "ct_AllPositionsWestA[%s,%s]" % (i,j) )
                            model.addConstr( z[i,j] == j, "ct_AllPositionsWestB[%s,%s]" % (i,j) )
                    elif d == 3:
                        for j in range(0,size):
                            model.addConstr( x[i,size-1-j,j] == 1, "ct_AllPositionsEastA[%s,%s]" % (i,j) )
                            model.addConstr( z[i,size-1-j] == j, "ct_AllPositionsEastB[%s,%s]" % (i,j) )                        
                      
    # Third set of VIs: Bounds on skyscraper positions   
    if useVI[2] == True:
        for d in range(0,4):
            for j in range(0,size):
                if math.isnan(cluesVisReq[j][d]) == False and cluesVisReq[j][d] >=2:
                    for k in range(size-int(cluesVisReq[j][d])+1,size):
                        if d == 0:
                            model.addConstr( sum( x[i,j,k] for i in range(0,int(cluesVisReq[j][d])-size+k-2)) == 0, "ct_BoundNorthGenericA[%s,%s]" % (j,k) )
                            for i in range(0,int(cluesVisReq[j][d])-size+k-2):
                                model.addConstr( z[i,j] <= k-1, "ct_BoundNorthGenericB[%s,%s,%s]" % (j,k,i) )
                    for k in range(size-int(cluesVisReq[j][d])+1,size):    
                        if d == 1:
                            model.addConstr( sum( x[i,j,k] for i in range(2*size-int(cluesVisReq[j][d])-k+1,size)) == 0, "ct_BoundSouthGenericA[%s,%s]" % (j,k) )
                            for i in range(2*size-int(cluesVisReq[j][d])-k+1,size):
                                model.addConstr( z[i,j] <= k-1, "ct_BoundSouthGenericB[%s,%s,%s]" % (j,k,i) )
            for i in range(0,size):
                if math.isnan(cluesVisReq[i][d]) == False and cluesVisReq[i][d] >=2:
                    for k in range(size-int(cluesVisReq[i][d])+1,size):
                        if d == 2:
                            model.addConstr( sum( x[i,j,k] for j in range(0,int(cluesVisReq[i][d])-size+k-2)) == 0, "ct_BoundWestGenericA[%s,%s]" % (i,k) )
                            for j in range(0,int(cluesVisReq[i][d])-size+k-2):
                                model.addConstr( z[i,j] <= k-1, "ct_BoundWestGenericB[%s,%s,%s]" % (i,k,j) )
                    for k in range(size-int(cluesVisReq[i][d])+1,size):    
                        if d == 3:
                            model.addConstr( sum( x[i,j,k] for j in range(2*size-int(cluesVisReq[i][d])-k+1,size)) == 0, "ct_BoundEastGenericA[%s,%s]" % (i,k) )
                            for j in range(2*size-int(cluesVisReq[i][d])-k+1,size):
                                model.addConstr( z[i,j] <= k-1, "ct_BoundEastGenericB[%s,%s,%s]" % (i,k,j) )
        

                       
    # Solve the model
    print("\nSolving Puzzle")
    start_time = time.time()
    model.optimize()
    runtime = time.time() - start_time
    model.write("SkyscrapersPuzzle.lp")

    
    # Postprocessing
    print("\nPostprocessing") # Check if feasible solution was found
    status=model.status
    if status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
        height_sol = np.empty((size,size))
        print("Solution: \n")      
        print(" ", end="")
        for i in Rows:
            print("----", end ="")
        print("")         
        for i in Rows:
            print("", end =" | ")
            for j in Columns:
                print(abs(round(z[i,j].x) + 1), end =" | ")
                height_sol[i][j] = z[i,j].x +1
            print()
            print(" ", end="")
            for i in Rows:
                print("----", end ="")
            print("")
     
    return height_sol, runtime
            
            
    if status == GRB.INFEASIBLE:
        print("Puzzle is infeasible.")            
                