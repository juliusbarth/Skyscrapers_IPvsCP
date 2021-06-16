/*********************************************
 * OPL 12.9.0.0 Model
 * Author: jfb2444
 * Creation Date: Aug 21, 2020 at 10:51:45 AM
 *********************************************/

 // Use Constraint Programming engine
 using CP;
 
 // Data
 
 int n = ...;							// Size n x n
 range Numbers = 1..n;
 int visNorth[Numbers] 			= ...; 	// Visibility from North
 int visSouth[Numbers] 			= ...; 	// Visibility from South
 int visWest[Numbers] 			= ...; 	// Visibility from West
 int visEast[Numbers] 			= ...; 	// Visibility from East
 int cellClue[Numbers][Numbers] = ...; 	// Cell clues
 
 
 int nbVisClues = 0;
 int nbCellClues = 0;
 float densityVisClues;
 float densityCellClues;
 execute { 
 	for(var i in Numbers) { 	
 		if(visNorth[i] >= 0) {
 		 	nbVisClues = nbVisClues + 1;
 		}
 		if(visSouth[i] >= 0) {
 		 	nbVisClues = nbVisClues + 1;
 		}
 		if(visWest[i] >= 0) {
 		 	nbVisClues = nbVisClues + 1;
 		}
 		if(visEast[i] >= 0) {
 		 	nbVisClues = nbVisClues + 1;
 		}
 		for (var j in Numbers) {
 			if(cellClue[i][j] >= 0) {
 				nbCellClues = nbCellClues +1; 			
 			} 		
 		} 	
 	}
 	densityVisClues = nbVisClues / (4*n); 
 	densityCellClues = nbCellClues / (n*n);
 	writeln("Visibility clue denisty: " + densityVisClues);
 	writeln("Cell clue denisty: " + densityCellClues);
 }
 
 // Decision variables
 dvar int x[Numbers][Numbers] in Numbers; 		// Value of cell (i,j)
 dvar int vNorth[Numbers][Numbers] in 0..1;		// Cell (i,j) visible from North
 dvar int vSouth[Numbers][Numbers] in 0..1;		// Cell (i,j) visible from South
 dvar int vWest[Numbers][Numbers] in 0..1;		// Cell (i,j) visible from West
 dvar int vEast[Numbers][Numbers] in 0..1;		// Cell (i,j) visible from East

 // Constraints
 subject to {
 
  	// Latin Square Constraints
 	forall(i in Numbers) {
 		allDifferent(all (j in Numbers) x[i][j] );			// Each number once per row
 		allDifferent(all (j in Numbers) x[j][i] );  		// Each number once per column		
	}
	
	// Cell clues (-1 if no clue given)
	forall(i in Numbers, j in Numbers) {
		if(cellClue[i][j] >= 0) {
			x[i][j] == cellClue[i][j];		
		}	
	}	
 	
 	// Visibility Constraints (-1 if not clue given)
	forall(i in Numbers) {
		if(visNorth[i] >= 0) {
			sum(j in Numbers) vNorth[j][i] == visNorth[i];		
		}
		if(visSouth[i] >= 0) {
			sum(j in Numbers) vSouth[j][i] == visSouth[i];
		}
		if(visWest[i] >= 0) {
			sum(j in Numbers) vWest[i][j] == visWest[i];
		}
		if(visEast[i] >= 0) {
			sum(j in Numbers) vEast[i][j] == visEast[i];		
		}
	}
	
	// First Row/Column of any direction is always visible
	forall(i in Numbers) {
		vNorth[1][i] == 1;
		vSouth[n][i] == 1;
		vWest[i][1] == 1;
		vEast[i][n] == 1;
	}
	
	// North Visibility
	forall(i in 2..n, j in Numbers) {	
		// Set visible to 1 if no larger skyscrapers block the view
		x[i][j] >= max(i1 in 1..i-1) x[i1][j] => vNorth[i][j] == 1;
		// Set visible to 0 if any larger skyscrapers block the view
		forall(i1 in 1..i-1) {
			x[i][j] <= x[i1][j] => vNorth[i][j] == 0;		
		}		
	}
	
	
	// South Visibility
	forall(i in 1..n-1, j in Numbers) {	
		// Set visible to 1 if no larger skyscrapers block the view
		x[i][j] >= max(i1 in i+1..n) x[i1][j] => vSouth[i][j] == 1;
		// Set visible to 0 if any larger skyscrapers block the view
		forall(i1 in i+1..n) {
			x[i][j] <= x[i1][j] => vSouth[i][j] == 0;		
		}		
	}
	
	// West Visibility
	forall(i in 2..n, j in Numbers) {	
		// Set visible to 1 if no larger skyscrapers block the view
		x[j][i] >= max(i1 in 1..i-1) x[j][i1] => vWest[j][i] == 1;
		// Set visible to 0 if any larger skyscrapers block the view
		forall(i1 in 1..i-1) {
			x[j][i] <= x[j][i1] => vWest[j][i] == 0;		
		}		
	}
	
	// East Visibility
	forall(i in 1..n-1, j in Numbers) {	
		// Set visible to 1 if no larger skyscrapers block the view
		x[j][i] >= max(i1 in i+1..n) x[j][i1] => vEast[j][i] == 1;
		// Set visible to 0 if any larger skyscrapers block the view
		forall(i1 in i+1..n) {
			x[j][i] <= x[j][i1] => vEast[j][i] == 0;		
		}		
	}
	/**/
	
 } 

 
