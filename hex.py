import math
import random
import pygame
from pygame import gfxdraw

GRID_WIDTH  = 4
GRID_HEIGHT = 4

HEXAGON_SIZE   = 50
HEXAGON_WIDTH  = HEXAGON_SIZE * math.sqrt(3)
HEXAGON_HEIGHT = HEXAGON_SIZE * 2

PADDING_X = HEXAGON_SIZE
PADDING_Y = HEXAGON_SIZE

SCREEN_WIDTH  = int(math.sqrt(3)/2 * HEXAGON_SIZE * 2 * (GRID_WIDTH + math.floor(GRID_HEIGHT/2)) + PADDING_X * 2)
SCREEN_HEIGHT = int(HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5) + PADDING_Y * 2)

def convertTo1D(coords):
	return (coords[0] * GRID_WIDTH) + coords[1]
	
def convertTo2D(val):
	return [val % GRID_WIDTH, val - (val % GRID_WIDTH)]

class Window():
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Hex")
		pygame.font.init()
		
		self.root      = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.grid_area = pygame.Surface((int(math.sqrt(3)/2 * HEXAGON_SIZE * 2 * (GRID_WIDTH + math.floor(GRID_HEIGHT/2))), int(HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5))))
		
		self.font      = pygame.font.SysFont("arialblack", 30)
		self.text_area = self.font.render("", False, (255, 255, 255))

class Game():
	def __init__(self):		
		self.board          = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]
		self.currentHexagon = [0,0]
		self.playerColours  = {-1: (200, 0, 0), 0: (255, 255, 255), 1: (0, 0, 200)}
		self.currentPlayer  = 1
		self.bestPaths      = list(self.evaluateGame()[1:])
		self.isFirstTurn    = True
		self.isGameWon      = False
		self.isGameRunning  = False
		self.gameWindow     = Window()
	
	def evaluateGame(self):
		bestPathP1 = []
		bestScoreP1 = float('inf')
		for i in range(0, GRID_WIDTH):
			for j in range(0, GRID_WIDTH):
				p = self.findPath([i, 0], [j, GRID_HEIGHT-1], 1)
				if len(p) == 0:
					score = float('inf')
				else:
					score = len(p)
				for k in p:
					if self.board[k[0]][k[1]] == 1:
						score -= 1
				if score < bestScoreP1:
					bestScoreP1 = score
					bestPathP1 = p
								
		bestPathP2 = []
		bestScoreP2 = float('inf')
		for i in range(0, GRID_HEIGHT):
			for j in range(0, GRID_HEIGHT):
				p = self.findPath([0, i], [GRID_WIDTH-1, j], -1)
				if len(p) == 0:
					score = float('inf')
				else:
					score = len(p)
				for k in p:
					if self.board[k[0]][k[1]] == -1:
						score -= 1
				if score < bestScoreP2:
					bestScoreP2 = score
					bestPathP2 = p
				
		return bestScoreP2 - bestScoreP1, bestPathP1, bestPathP2
	
	def findPath(self, start, goal, p):
		if self.board[start[0]][start[1]] in [p, 0]:
			frontier = []
			frontier.append((0, start))
			
			cameFrom = {}
			cameFrom[convertTo1D(start)] = None
			
			costSoFar = {}
			costSoFar[convertTo1D(start)] = 0
			
			while len(frontier) > 0:
				current = frontier.pop(0)[1]
				
				if current == goal:
					break
				
				neighbours = [[current[0],   current[1]-1], 
							  [current[0]+1, current[1]-1], 
							  [current[0]-1, current[1]], 
							  [current[0]+1, current[1]], 
							  [current[0]-1, current[1]+1], 
							  [current[0],   current[1]+1]]
				
				valid = []
				
				for n in neighbours:
					if n[0] < GRID_WIDTH and n[1] < GRID_HEIGHT and n[0] >= 0 and n[1] >= 0:
						if self.board[n[0]][n[1]] in [p, 0]:
							valid.append(n)
				
				for n in valid:
					cost = costSoFar[convertTo1D(current)] + 1
					if convertTo1D(n) not in cameFrom or cost < costSoFar[convertTo1D(n)]:
						costSoFar[convertTo1D(n)] = cost
						priority = cost
						frontier.append((priority, n))
						cameFrom[convertTo1D(n)] = current
			
			if convertTo1D(goal) in cameFrom:
				current = goal
				path = []
				while current != start:
					path.append(current)
					current = cameFrom[convertTo1D(current)]
				path.append(start)
				path.reverse()
			else:
				path = []
		else:
			path = []
		
		return path	
		
	def runGame(self):
		self.isGameRunning = True
		
		while self.isGameRunning:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.isGameRunning = False
					pygame.quit()
					exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.isGameRunning = False
						pygame.quit()
						exit()
					elif event.key == pygame.K_RIGHT:
						self.currentHexagon[0] = min(self.currentHexagon[0] + 1, GRID_WIDTH - 1)
					elif event.key == pygame.K_LEFT:
						self.currentHexagon[0] = max(self.currentHexagon[0] - 1, 0)
					elif event.key == pygame.K_DOWN:
						self.currentHexagon[1] = min(self.currentHexagon[1] + 1, GRID_HEIGHT - 1)
					elif event.key == pygame.K_UP:
						self.currentHexagon[1] = max(self.currentHexagon[1] - 1, 0)
					elif event.key == pygame.K_RETURN:
						if self.board[self.currentHexagon[0]][self.currentHexagon[1]] == 0 or (self.currentPlayer == -1 and self.isFirstTurn):
							self.board[self.currentHexagon[0]][self.currentHexagon[1]] = self.currentPlayer
							
							eval, self.bestPaths[0], self.bestPaths[1] = self.evaluateGame()
							
							print("Evaluation: " + str(eval) + ", ", end="")
							if eval == float('inf'):
								print("Blue has won!")
							elif eval > 0:
								print("Blue has the advantage")
							elif eval == 0:
								print("Game is even")
							elif eval == float('inf'):
								print("Red has won!")
							else:
								print("Red has the advantage")
								
							self.currentPlayer = -self.currentPlayer
						
							if (self.currentPlayer == -1 and self.isFirstTurn):
								self.isFirstTurn == False
			
			self.drawGame()
							
	def drawGame(self):
		pygame.gfxdraw.aapolygon(self.gameWindow.grid_area, ((HEXAGON_WIDTH/2, 0), (HEXAGON_WIDTH * (GRID_WIDTH-0.5), 0), (HEXAGON_WIDTH * (GRID_WIDTH) + HEXAGON_WIDTH/2 * (GRID_HEIGHT - 2), HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5)), (HEXAGON_WIDTH/2 * (GRID_HEIGHT), HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5))), self.playerColours[1])
		pygame.gfxdraw.filled_polygon(self.gameWindow.grid_area, ((HEXAGON_WIDTH/2, 0), (HEXAGON_WIDTH * (GRID_WIDTH-0.5), 0), (HEXAGON_WIDTH * (GRID_WIDTH) + HEXAGON_WIDTH/2 * (GRID_HEIGHT - 2), HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5)), (HEXAGON_WIDTH/2 * (GRID_HEIGHT), HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5))), self.playerColours[1])
		pygame.gfxdraw.aapolygon(self.gameWindow.grid_area, ((0, 1.5 * HEXAGON_SIZE), (GRID_WIDTH * HEXAGON_WIDTH, 0.5 * HEXAGON_SIZE), (HEXAGON_WIDTH * (GRID_WIDTH) + HEXAGON_WIDTH/2 * (GRID_HEIGHT - 1), HEXAGON_SIZE * (1.5 * GRID_HEIGHT - 1)), (HEXAGON_WIDTH/2 * (GRID_HEIGHT - 1), HEXAGON_SIZE * (1.5 * GRID_HEIGHT))), self.playerColours[-1])
		pygame.gfxdraw.filled_polygon(self.gameWindow.grid_area, ((0, 1.5 * HEXAGON_SIZE), (GRID_WIDTH * HEXAGON_WIDTH, 0.5 * HEXAGON_SIZE), (HEXAGON_WIDTH * (GRID_WIDTH) + HEXAGON_WIDTH/2 * (GRID_HEIGHT - 1), HEXAGON_SIZE * (1.5 * GRID_HEIGHT - 1)), (HEXAGON_WIDTH/2 * (GRID_HEIGHT - 1), HEXAGON_SIZE * (1.5 * GRID_HEIGHT))), self.playerColours[-1])
		
		for x in range(0, len(self.board)):
			for y in range(0, len(self.board[x])):
				pygame.gfxdraw.aapolygon(self.gameWindow.grid_area, [((x+0.5) * HEXAGON_SIZE * math.sqrt(3) + y * HEXAGON_SIZE * math.sqrt(3)/2 + HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (y+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.playerColours[self.board[x][y]])
				pygame.gfxdraw.filled_polygon(self.gameWindow.grid_area, [((x+0.5) * HEXAGON_SIZE * math.sqrt(3) + y * HEXAGON_SIZE * math.sqrt(3)/2 ++ HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (y+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.playerColours[self.board[x][y]])
				pygame.gfxdraw.aapolygon(self.gameWindow.grid_area, [((x+0.5) * HEXAGON_SIZE * math.sqrt(3) + y * HEXAGON_SIZE * math.sqrt(3)/2 + HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (y+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (0,0,0))
		
		for r in range(0, int(HEXAGON_SIZE/4),3):
			pygame.gfxdraw.polygon(self.gameWindow.grid_area, [((self.currentHexagon[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.currentHexagon[1] * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE-r) * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.currentHexagon[1]+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE-r) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (0,255,0))
			pygame.gfxdraw.aapolygon(self.gameWindow.grid_area, [((self.currentHexagon[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.currentHexagon[1] * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE-r) * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.currentHexagon[1]+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE-r) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (0,255,0))
		
		for p in self.bestPaths[0]:
			pygame.gfxdraw.aapolygon(self.gameWindow.grid_area, [((p[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + p[1] * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE/2) * math.cos(2 * math.pi * (i / 6 + 1/12)), (p[1]+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE/2) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.playerColours[1])
			pygame.gfxdraw.filled_polygon(self.gameWindow.grid_area, [((p[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + p[1] * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE/2) * math.cos(2 * math.pi * (i / 6 + 1/12)), (p[1]+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE/2) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.playerColours[1])
		
		for p in self.bestPaths[1]:
			if p in self.bestPaths[0]:
				pygame.gfxdraw.aapolygon(self.gameWindow.grid_area, [((p[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + p[1] * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE/2) * math.cos(2 * math.pi * (i / 6 + 1/12)), (p[1]+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE/2) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (100, 0, 100))
				pygame.gfxdraw.filled_polygon(self.gameWindow.grid_area, [((p[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + p[1] * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE/2) * math.cos(2 * math.pi * (i / 6 + 1/12)), (p[1]+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE/2) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (100,0,100))
			else:
				pygame.gfxdraw.aapolygon(self.gameWindow.grid_area, [((p[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + p[1] * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE/2) * math.cos(2 * math.pi * (i / 6 + 1/12)), (p[1]+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE/2) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.playerColours[-1])
				pygame.gfxdraw.filled_polygon(self.gameWindow.grid_area, [((p[0]+0.5) * HEXAGON_SIZE * math.sqrt(3) + p[1] * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE/2) * math.cos(2 * math.pi * (i / 6 + 1/12)), (p[1]+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE/2) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.playerColours[-1])
			
		
		self.gameWindow.root.blit(self.gameWindow.grid_area, (PADDING_X, PADDING_Y))
		self.gameWindow.root.blit(self.gameWindow.text_area, ((SCREEN_WIDTH - self.gameWindow.text_area.get_rect().width)/2, (PADDING_Y - self.gameWindow.text_area.get_rect().height)/2))
		pygame.display.flip()
		
game = Game()
game.runGame()