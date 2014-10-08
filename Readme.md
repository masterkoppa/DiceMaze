SD Maze Readme
==============

## Running instructions

To run use the following command   

    python3 sdmaze.py <filename>   

Where:   
- python3 is the name for the binary for python version 3 for your system
- <filename> is the path or filename to the maze txt files as described in the assignment

## Output

The program will execute and display the stats for the 3 built in heuristics and then 
display the path to the goal for the given maze.

### Example

	-------------------------------------------
	Brooklyn Distance
	Nodes visited: 11
	Nodes generated: 16
	-------------------------------------------
	Manhattan Distance
	Nodes visited: 15
	Nodes generated: 22
	-------------------------------------------
	Euclidian Distance
	Nodes visited: 34
	Nodes generated: 43
	-------------------------------------------


	Starting Position
	-----------------
	1 . . . G 
	. . . . . 

	-----------------
	Move: 1
	Direction: South
	-----------------
	S . . . G 
	2 . . . . 

	-----------------
	Move: 2
	Direction: East
	-----------------
	S . . . G 
	. 4 . . . 

	-----------------
	Move: 3
	Direction: East
	-----------------
	S . . . G 
	. . 5 . . 

	-----------------
	Move: 4
	Direction: East
	-----------------
	S . . . G 
	. . . 3 . 

	-----------------
	Move: 5
	Direction: East
	-----------------
	S . . . G 
	. . . . 2 

	-----------------
	Move: 6
	Direction: North
	-----------------
	S . . . 1 
	. . . . . 

	Number of move to goal: 7

