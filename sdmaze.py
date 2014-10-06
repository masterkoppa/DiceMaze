#!/bin/python

import sys
import copy
import random

initial_positions = [4,2,3,5,1,6]

class Maze(object):

	class Node(object):
		"""docstring for Node"""
		def __init__(self, value = None, blocked = False):
			self.blocked = blocked
			self.value = value
			

		def __str__(self):

			if self.blocked:
				return "*"
			
			if self.value == None:
				return "."
			else:
				return str(self.value)

		def __repr__(self):
			return str(self)

		def copyNode(self):
			return Node(self.value, self.blocked)

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

		print("Start:  " + str(self.start))
		print("Goal:   " + str(self.goal))
		print(str(self))

	def __str__(self):
		ret = ""

		rowIndex = 0
		for row in self.board:
			colIndex = 0
			for col in row:
				ret += str(col)
				colIndex += 1
			rowIndex += 1
			ret += "\n"

		return ret

	def __eq__(self, other):
		return self.current == other.current and self.position == other.position

	def __ne__(self, other):
		return not self.__eq__(other)

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

	print(mazeLines)
	m = Maze(mazeLines)

	#move_count = 0
	
	#print("Number of moves: " + str(move_count))
	graph[m] = []
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

	for m in graph.keys():
		print("State")
		print(m)
		print("Neighboors")
		for n in graph[m]:
			print(n)
			print("")
		print("-------------------------------")
	printGraphStats(graph)






if __name__ == '__main__':
	main()
	#testDieRoll()
