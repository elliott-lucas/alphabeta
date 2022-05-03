from games import Game, Window
import pygame
from pygame import gfxdraw
import math

HEXAGON_SIZE  = 50
HEXAGON_WIDTH = HEXAGON_SIZE * math.sqrt(3)
PADDING_X     = HEXAGON_SIZE
PADDING_Y     = HEXAGON_SIZE

class Hex(Game):
	def __init__(self, graphics, human, w=4, h=4, swap=True):
		super().__init__(graphics, human)
		self.width     = w
		self.height    = h
		self.swap_rule = swap
		self.board     = [[0 for y in range(self.width)] for x in range(self.height)]
		
		if graphics:
			self.window = Window(int(HEXAGON_WIDTH * (self.width + self.height/2 - 0.5) + PADDING_X * 2), int(HEXAGON_SIZE * (1.5 * self.height + 0.5) + PADDING_Y * 2), "Hex")
			self.window.grid_area = pygame.Surface((int(HEXAGON_WIDTH * (self.width + self.height/2 - 0.5)), int(HEXAGON_SIZE * (1.5 * self.height + 0.5))))
			self.window.colours = {-1: (200, 0, 0), 0: (255, 255, 255), 1: (0, 0, 200)}
			
			if human:
				self.currentHexagon = [0,0]
		
	def getPossibleMoves(self):
		possibleMoves = {}
		for x in range(0, self.width):
			for y in range(0, self.height):
				if self.swap_rule and self.board[x][y] == 1 and self.currentPlayer == -1 and self.totalMoves == 1:
						possibleMoves[(x, y)] = 0
				if self.board[x][y] == 0:
					possibleMoves[(x, y)] = 0
		return possibleMoves
		
	def getEvaluation(self):
		scores = {-1: float('inf'), 1: float('inf')}
		paths = {}
		
		for p in (1, -1):
			paths[p] = self.findPath(p)
			if len(paths[p]) > 0:
				scores[p] = len(paths[p]) - paths[p].count(p)
				
		return scores[-1] - scores[1]
		
	def playMove(self, move):
		t = {"board": [row[:] for row in self.board]}
		self.board[move[0]][move[1]] = self.currentPlayer
		self.totalMoves += 1
		
		if self.getEvaluation() == float('inf') * self.currentPlayer:
			self.isGameOver = True
			self.winningPlayer = self.currentPlayer
		self.currentPlayer = -self.currentPlayer
			
		return t
		
	def findPath(self, player):
		frontier = []
		cameFrom = {}
		costSoFar = {}
		
		if player == 1:
			for x in range(0, self.width):
				if self.board[x][0] in [player, 0]:
					frontier.append((0, (x, 0)))
					cameFrom[(x, 0)] = "start"
					costSoFar[(x, 0)] = (self.board[x][0] != player)
		else:
			for y in range(0, self.height):
				if self.board[0][y] in [player, 0]:
					frontier.append((0, (0, y)))
					cameFrom[(0, y)] = "start"
					costSoFar[(0, y)] = (self.board[0][y] != player)
			
		while len(frontier) > 0:
			current = frontier.pop(0)[1]
			if (current[1] == self.height-1 and player == 1) or (current[0] == self.width-1 and player == -1):
				if "goal" not in cameFrom or costSoFar[current] < costSoFar["goal"]:
					costSoFar["goal"] = costSoFar[current]
					cameFrom["goal"] = current
			
			neighbours = [(current[0], current[1]-1), (current[0]+1, current[1]-1), (current[0]-1, current[1]), (current[0]+1, current[1]), (current[0]-1, current[1]+1), (current[0], current[1]+1)]
			valid = []
				
			for n in neighbours:
				if n[0] < self.width and n[1] < self.height and n[0] >= 0 and n[1] >= 0:
					if self.board[n[0]][n[1]] in [player, 0]:
						valid.append(n)
				
			for n in valid:
				cost = costSoFar[current] + (self.board[n[0]][n[1]] != player)
				if n not in cameFrom or cost < costSoFar[n]:
					costSoFar[n] = cost
					priority = cost
					frontier.append((priority, n))
					cameFrom[n] = current
			
		if "goal" in cameFrom:
			current = cameFrom["goal"]
			path = []
			while current != "start":
				path.append(current)
				current = cameFrom[current]
			path.reverse()
		else:
			path = []
			
		return path
		
	def drawGame(self):
		if self.graphics:
			pygame.gfxdraw.aapolygon(self.window.grid_area, ((HEXAGON_WIDTH/2, 0), (HEXAGON_WIDTH * (self.width-0.5), 0), (HEXAGON_WIDTH * (self.width) + HEXAGON_WIDTH/2 * (self.height - 2), HEXAGON_SIZE * (1.5 * self.height + 0.5)), (HEXAGON_WIDTH/2 * (self.height), HEXAGON_SIZE * (1.5 * self.height + 0.5))), self.window.colours[1])
			pygame.gfxdraw.filled_polygon(self.window.grid_area, ((HEXAGON_WIDTH/2, 0), (HEXAGON_WIDTH * (self.width-0.5), 0), (HEXAGON_WIDTH * (self.width) + HEXAGON_WIDTH/2 * (self.height - 2), HEXAGON_SIZE * (1.5 * self.height + 0.5)), (HEXAGON_WIDTH/2 * (self.height), HEXAGON_SIZE * (1.5 * self.height + 0.5))), self.window.colours[1])
			pygame.gfxdraw.aapolygon(self.window.grid_area, ((0, 1.5 * HEXAGON_SIZE), (self.width * HEXAGON_WIDTH, 0.5 * HEXAGON_SIZE), (HEXAGON_WIDTH * (self.width) + HEXAGON_WIDTH/2 * (self.height - 1), HEXAGON_SIZE * (1.5 * self.height - 1)), (HEXAGON_WIDTH/2 * (self.height - 1), HEXAGON_SIZE * (1.5 * self.height))), self.window.colours[-1])
			pygame.gfxdraw.filled_polygon(self.window.grid_area, ((0, 1.5 * HEXAGON_SIZE), (self.width * HEXAGON_WIDTH, 0.5 * HEXAGON_SIZE), (HEXAGON_WIDTH * (self.width) + HEXAGON_WIDTH/2 * (self.height - 1), HEXAGON_SIZE * (1.5 * self.height - 1)), (HEXAGON_WIDTH/2 * (self.height - 1), HEXAGON_SIZE * (1.5 * self.height))), self.window.colours[-1])
			
			for x in range(0, len(self.board)):
				for y in range(0, len(self.board[x])):
					pygame.gfxdraw.aapolygon(self.window.grid_area, [((x+0.5) * HEXAGON_SIZE * math.sqrt(3) + y * HEXAGON_SIZE * math.sqrt(3)/2 + HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (y+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.window.colours[self.board[x][y]])
					pygame.gfxdraw.filled_polygon(self.window.grid_area, [((x+0.5) * HEXAGON_SIZE * math.sqrt(3) + y * HEXAGON_SIZE * math.sqrt(3)/2 ++ HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (y+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.window.colours[self.board[x][y]])
					pygame.gfxdraw.aapolygon(self.window.grid_area, [((x+0.5) * HEXAGON_SIZE * math.sqrt(3) + y * HEXAGON_SIZE * math.sqrt(3)/2 + HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (y+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (0,0,0))
			
			if self.human and not self.isGameOver and self.currentPlayer == 1:
				pygame.gfxdraw.aapolygon(self.window.grid_area, [((self.currentHexagon[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.currentHexagon[1] * HEXAGON_SIZE * math.sqrt(3)/2 + HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.currentHexagon[1]+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], tuple(min(255, c+150) for c in self.window.colours[self.currentPlayer]))
				pygame.gfxdraw.filled_polygon(self.window.grid_area, [((self.currentHexagon[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.currentHexagon[1] * HEXAGON_SIZE * math.sqrt(3)/2 ++ HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.currentHexagon[1]+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], tuple(min(255, c+150) for c in self.window.colours[self.currentPlayer]))
				pygame.gfxdraw.aapolygon(self.window.grid_area, [((self.currentHexagon[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.currentHexagon[1] * HEXAGON_SIZE * math.sqrt(3)/2 + HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.currentHexagon[1]+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (0,0,0))
				
			self.window.root.blit(self.window.grid_area, (PADDING_X, PADDING_Y))
			pygame.display.flip()
		else:
			for i in range(len(self.board)):
				for x in self.board:
					print("%s," % x[i],end="")
				print("")
		
	def getInput(self):
		if self.graphics:
			while True:
				self.drawGame()
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_UP:
							self.currentHexagon[1] = max(0, self.currentHexagon[1] - 1)
						elif event.key == pygame.K_DOWN:
							self.currentHexagon[1] = min(self.height-1, self.currentHexagon[1] + 1)
						elif event.key == pygame.K_LEFT:
							self.currentHexagon[0] = max(0, self.currentHexagon[0] - 1)
						elif event.key == pygame.K_RIGHT:
							self.currentHexagon[0] = min(self.width-1, self.currentHexagon[0] + 1)
						elif event.key == pygame.K_RETURN:
							if tuple(self.currentHexagon) in self.getPossibleMoves():
								return tuple(self.currentHexagon)
		else:
			x = -1
			y = -1
			
			while (not (0 <= x < self.width and 0 <= y < self.height)) or self.board[x][y] != 0: 
				x = int(input("\nX: "))
				y = int(input("Y: "))
				if (not (0 <= x < self.width and 0 <= y < self.height)) or self.board[x][y] != 0:
					print("\nInvalid grid position.")
			
			return (x,y)