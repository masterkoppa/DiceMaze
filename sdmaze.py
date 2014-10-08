#!/bin/python

import sys
import math
from queue import PriorityQueue
from maze import Maze


def manhattan_distance(maze):
	c_row, c_col = maze.current
	g_row, g_col = maze.goal

	return math.fabs(c_row - g_row) + math.fabs(c_col - g_col)

def euclidian_distance(maze):
	c_row, c_col = maze.current
	g_row, g_col = maze.goal

	return math.sqrt(math.pow(c_row - c_col, 2) + math.pow(g_row - g_col, 2))

def brooklyn_distance(maze):
	c_row, c_col = maze.current
	g_row, g_col = maze.goal

	diff_row = math.fabs(c_row - g_row)
	diff_col = math.fabs(c_col - g_col)

	value = maze.board[c_row][c_col].getValue()

	if diff_row <= 3 and diff_col <= 3:
		return -100 / (max(diff_row, diff_col) + 1)
	else:
		return manhattan_distance(maze)

def dummy_heuristic(maze):
	return 0

class Wrapper(object):
	def __init__(self, maze, priority):
		self.maze = maze
		self.priority = priority

	def __lt__(self, other):
		return self.priority < other.priority

def aStar(graph, initialMaze, heuristic):
	frontier = PriorityQueue()
	frontier.put(Wrapper(initialMaze, 0))
	came_from = {}
	cost_so_far = {}
	came_from[initialMaze] = None
	cost_so_far[initialMaze] = 0

	nodes_generated = 1
	nodes_visited = 0

	while not frontier.empty():
		nodes_visited += 1
		current = frontier.get().maze

		if current.isGoal():
			print("Nodes visited: " + str(nodes_visited))
			print("Nodes generated: " + str(nodes_generated))
			return buildPath(came_from, current)

		for n in current.getNeighbors(graph):
			new_cost = cost_so_far[current] + 1
			if n not in cost_so_far or new_cost < cost_so_far[n]:
				cost_so_far[n] = new_cost
				priority = new_cost + heuristic(n)
				frontier.put(Wrapper(n, priority))
				nodes_generated += 1
				came_from[n] = current

	# No solution
	print("Nodes visited: " + str(nodes_visited))
	print("Nodes generated: " + str(nodes_generated))

def buildPath(parent_graph, goalNode):
	if(goalNode == None):
		return []
	else:
		return buildPath(parent_graph, parent_graph[goalNode]) + [goalNode]

def getDirection(m_from, m_to):
	from_row, from_col = m_from.current
	to_row, to_col = m_to.current

	diff_row = from_row - to_row
	diff_col = from_col - to_col

	if diff_row == 0 and diff_col == 1:
		return "West"
	elif diff_row == 0 and diff_col == -1:
		return "East"
	elif diff_row == 1 and diff_col == 0:
		return "North"
	elif diff_row == -1 and diff_col == 0:
		return "South"
	else:
		return "Invalid"

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
	initialMaze = Maze(mazeLines)

	#print("Dummy Heuristic")
	#results = aStar(graph, initialMaze, dummy_heuristic)
	print("-------------------------------------------")
	print("Brooklyn Distance")
	results = aStar(graph, initialMaze, brooklyn_distance)
	print("-------------------------------------------")

	#Nuke the graph
	graph = {}

	print("Manhattan Distance")
	results = aStar(graph, initialMaze, manhattan_distance)
	print("-------------------------------------------")

	# Nuke graph
	graph = {}

	print("Euclidian Distance")
	results = aStar(graph, initialMaze, euclidian_distance)
	print("-------------------------------------------\n\n")

	if results != None:
		print("Starting Position")
		print("-----------------")
		print(results[0])

		for i in range(1, len(results)):
			print("-----------------")
			print("Move: " + str(i))
			m_from = results[i-1]
			m_to = results[i]
			print("Direction: " + getDirection(m_from, m_to))
			print("-----------------")
			print(results[i])


		print("Number of move to goal: " + str(len(results)))
	else:
		print("No Solution")


if __name__ == '__main__':
	main()
	#testDieRoll()
