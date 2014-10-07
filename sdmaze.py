#!/bin/python

import sys
import copy
import random
from queue import PriorityQueue

initial_positions = [4,2,3,5,1,6]

class Maze(object):

	class Node(object):
		"""docstring for Node"""
		def __init__(self, value = None, blocked = False):
			self.blocked = blocked
			self.value = value

		def __str__(self):
			if self.blocked:
				return "* "
			
			if self.value == None:
				return ". "
			else:
				return str(self.value) + " "

		def __repr__(self):
			return str(self)

		def __deepcopy__(self, memo):
			return Maze.Node(self.value, self.blocked)

		def isBlocked(self):
			return self.blocked

		def getValue(self):
			return self.value
			
			

	"""docstring for Maze"""
	def __init__(self, board):
		self.start = (0,0)
		self.goal = (0,0)
		self.current = (0,0)
		self.board = []
		self.position = initial_positions

		rowIndex = 0
		for row in board:
			nodeRow = []
			colIndex = 0
			for col in row:
				if col == '*':
					nodeRow.append(self.Node(blocked = True))
				elif col == '.':
					nodeRow.append(self.Node())
				elif col == 'S':
					nodeRow.append(self.Node(value = 1))
					self.start = (rowIndex, colIndex)
					self.current = self.start
				elif col == 'G':
					nodeRow.append(self.Node())
					self.goal = (rowIndex, colIndex)

				colIndex +=1
			rowIndex += 1
			self.board.append(nodeRow)

		#print("Start:  " + str(self.start))
		#print("Goal:   " + str(self.goal))
		#print(str(self))

	def __str__(self):
		ret = ""

		rowIndex = 0
		for row in self.board:
			colIndex = 0
			for col in row:
				if rowIndex == self.goal[0] and colIndex == self.goal[1] and col.getValue() == None:
					ret += 'G '
				elif rowIndex == self.start[0] and colIndex == self.start[1] and col.getValue() == None:
					ret += 'S '
				else:
					ret += str(col)
				colIndex += 1
			rowIndex += 1
			ret += "\n"

		return ret

	def __eq__(self, other):
		if not isinstance(other,Maze):
			return False

		return self.current == other.current and self.position == other.position

	def __ne__(self, other):
		return not self.__eq__(other)

	'''
	'''
	def __lt__(self, other):
		if(self == other):
			return 0
		else:
			return -1 # Return this if there's a tie in heuristics

	def __hash__(self):
		return hash((self.current, tuple(self.position)))

	def isGoal(self):
		if(self.board[self.goal[0]][self.goal[1]].getValue() == 1):
			return True
		else:
			return False

	'''
	move

	- direction 
				1 - west
				2 - north
				3 - east
				4 - south
	'''
	def move(self, direction):
		'''
		print('Making move')
		if(direction == 1):
			print("Moving west  (<-)")
		elif(direction == 2):
			print("Moving north (^^)")
		elif(direction == 3):
			print("Moving east  (->)")
		elif(direction == 4):
			print("Moving south (\/)")
		#print('Currently at ' + self.current[0] + ' , ' + self.current[1])
		'''
		# Start solving

		left = 0
		north = 1
		right = 2
		south = 3
		top = 4
		bottom = 5

		position = copy.copy(self.position)
		
		c_row, c_col = self.current
		
		n_row, n_col = self.current

		if(direction == 1):
			n_col -= 1
		elif(direction == 2):
			n_row -= 1
		elif(direction == 3):
			n_col += 1
		elif(direction == 4):
			n_row += 1

		if(n_col < 0 or n_row < 0):
			return False

		if(n_row >= len(self.board) or n_col >= len(self.board[0])):
			return False

		if(self.board[n_row][n_col].isBlocked()):
			return False

		if(direction == 1):
			temp = position[top]
			position[top] = position[right]
			position[right] = position[bottom]
			position[bottom] = position[left]
			position[left] = temp
		elif(direction == 2):
			temp = position[top]
			position[top] = position[south]
			position[south] = position[bottom]
			position[bottom] = position[north]
			position[north] = temp
		elif(direction == 3):
			temp = position[top]
			position[top] = position[left]
			position[left] = position[bottom]
			position[bottom] = position[right]
			position[right] = temp
		elif(direction == 4):
			temp = position[top]
			position[top] = position[north]
			position[north] = position[bottom]
			position[bottom] = position[south]
			position[south] = temp
		else:
			print("Error incorrect move")
			return False

		if(position[top] == 6):
			return False

		# Nuke the current entry
		self.board[c_row][c_col] = self.Node()

		self.current = (n_row, n_col)
		self.board[n_row][n_col] = self.Node(value = position[top])
		self.position = position

		return True



def aStar(graph, initialMaze, heuristic):
	
	frontier = PriorityQueue()
	frontier.put(initialMaze, 0)
	came_from = {}
	cost_so_far = {}
	came_from[initialMaze] = None
	cost_so_far[initialMaze] = 0

	while not frontier.empty():
		current = frontier.get()

		if current.isGoal():
			printSearchStats(came_from, graph)
			return buildPath(came_from, current)

		for n in graph[current]:
			new_cost = cost_so_far[current] + 1
			if n not in cost_so_far or new_cost < cost_so_far[n]:
				cost_so_far[n] = new_cost
				priority = new_cost + heuristic(n)
				frontier.put(n, priority)
				came_from[n] = current



def printSearchStats(parent_graph, graph):
	nodes_visited = len(parent_graph.keys())
	nodes_in_graph = len(graph.keys())

	print("Number of nodes visited: " + str(nodes_visited))
	print("Number of nodes created: " + str(nodes_in_graph))


def buildPath(parent_graph, goalNode):
	if(goalNode == None):
		return []
	else:
		return buildPath(parent_graph, parent_graph[goalNode]) + [goalNode]





def copyMaze(maze):
	return copy.deepcopy(maze)

def buildNeighboors(maze):

	ret = []
	for dir in range(1,5):
		temp = copyMaze(maze)
		if(temp.move(dir)):
			ret += [temp]

	return ret

def printGraphStats(graph):
	print("Number of possible states: " + str(len(graph.keys())))

def main():
	args = sys.argv
	graph = {}

	if(len(args) <= 1):
		print("Usage: sdmaze <filename>")
		return

	filename = args[1]

	mazeLines = []

	for i in open(filename):
		line = []
		i = i.strip()
		for char in i:
			line.append(char)

		mazeLines.append(line)

	#print(mazeLines)
	initialMaze = Maze(mazeLines)


	#move_count = 0
	
	#print("Number of moves: " + str(move_count))
	graph[initialMaze] = []
	while([] in graph.values()):
		newGraph = graph.copy()
		for key in graph.keys():
			if len(graph[key]) == 0:
				neigh = buildNeighboors(key)
				newGraph[key] = neigh

				for n in neigh:
					if not (n in graph.keys()):
						newGraph[n] = []
		graph = newGraph
	'''
	for m in graph.keys():
		print("State")
		print(m)
		print("Neighboors")
		for n in graph[m]:
			print(n)
			print("")
		print("-------------------------------")
	printGraphStats(graph)
	'''

	winnable = False
	for m in graph.keys():
		if(m.isGoal()):
			winnable = True
			break
	#print("Is it possible to win?")
	#print(winnable)

	results = aStar(graph, initialMaze, lambda current_state: 0)

	for i in results:
		print(i)






if __name__ == '__main__':
	main()
	#testDieRoll()
