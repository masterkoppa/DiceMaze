import copy

class Maze(object):
	"""
	Maze object

	Represents the state of the Dice Maze

	Properties:

	- start    : The start coordinates
	- goal     : The goal coordinates
	- current  : Current location of the dice
	- board    : A 2d list representation of nodes that forms the board
	- position : A list representing the location of all numbers in the dice. See move
	"""

	"""
	The starting configuration for the dice at the start position
	"""
	initial_positions = [4,2,3,5,1,6]

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
			
			

	
	def __init__(self, board, bypass = False):
		"""
		Initialize the maze with the dice at the start position
		in its start configuration.
		"""
		if bypass:
			return

		self.start = (0,0)
		self.goal = (0,0)
		self.current = (0,0)
		self.board = []
		self.position = Maze.initial_positions

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

	def __str__(self):
		"""
		Returns the maze in a similar configuration as the file input,
		with the exception of added spaces for readability. See Node.__str__
		"""
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

	def __hash__(self):
		return hash((self.current, tuple(self.position)))

	def __deepcopy__(self, memo):
		newCopy = Maze([], bypass = True)
		newCopy.start = self.start
		newCopy.goal = self.goal
		newCopy.current = self.current
		newCopy.board = copy.deepcopy(self.board, memo)
		newCopy.position = copy.deepcopy(self.position, memo)

		return newCopy

	def _build_neighbors(self):
		"""
		Returns a list of possible maze configurations if the dice where
		to be moved in all possible positions. Handles valid and invalid moves.

		Externally use getNeighbors
		"""
		ret = []
		for dir in range(1,5):
			temp = copy.deepcopy(self)
			if(temp.move(dir)):
				ret += [temp]

		return ret

	def getNeighbors(self, graph):
		"""
		Returns a list of possible maze configurations if the dice where
		to be moved in all possible positions. Handles valid and invalid moves.

		This method handles caching via the graph dictionary. Will do lookup there 
		before generating the nodes.
		"""
		if(self in graph):
			return graph[self]
		else:
			neigh = self._build_neighbors()
			graph[self] = neigh
			return neigh


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