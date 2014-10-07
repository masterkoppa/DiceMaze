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
	print("No solution")
	print("Nodes visited: " + str(nodes_visited))
	print("Nodes generated: " + str(nodes_generated))

def buildPath(parent_graph, goalNode):
	if(goalNode == None):
		return []
	else:
		return buildPath(parent_graph, parent_graph[goalNode]) + [goalNode]


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
	#print("-------------------------------------------")
	print("Manhattan Distance")
	results = aStar(graph, initialMaze, manhattan_distance)
	print("-------------------------------------------")

	# Nuke graph
	#graph = {}

	#print("Euclidian Distance")
	#results = aStar(graph, initialMaze, euclidian_distance)
	#print("-------------------------------------------\n\n")

	for i in results:
		print(i)

	print(len(results))






if __name__ == '__main__':
	main()
	#testDieRoll()
