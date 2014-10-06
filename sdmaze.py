#!/bin/python

import sys

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

	'''
	move

	- direction 
				1 - west
				2 - north
				3 - east
				4 - south
	'''
	def move(self, direction):

		print('Making move')
		#print('Currently at ' + self.current[0] + ' , ' + self.current[1])

		# Start solving

		left = 0
		north = 1
		right = 2
		south = 3
		top = 4
		bottom = 5

		position = self.position

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
		
		# Nuke the current entry
		c_row, c_col = self.current
		self.board[c_row][c_col] = self.Node()
		n_row, n_col = self.current

		if(direction == 1):
			n_col -= 1
		elif(direction == 2):
			n_row += 1
		elif(direction == 3):
			n_col += 1
		elif(direction == 4):
			n_row -= 1

		self.current = (n_row, n_col)
		self.board[n_row][n_col] = self.Node(value = position[top])





		return position












	

def main():
	args = sys.argv

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

	m.move(3)
	print(str(m))
	m.move(3)
	print(str(m))





if __name__ == '__main__':
	main()
	#testDieRoll()
