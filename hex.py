import math
import random
import time
import pygame
from pygame import gfxdraw

GRID_WIDTH  = 4
GRID_HEIGHT = 4

SEARCH_DEPTH   = 4
SEARCH_PRUNING = True

GRAPHICS_ENABLED = True

HEXAGON_SIZE  = 50
HEXAGON_WIDTH = HEXAGON_SIZE * math.sqrt(3)

PADDING_X = HEXAGON_SIZE
PADDING_Y = HEXAGON_SIZE

SCREEN_WIDTH  = int(HEXAGON_WIDTH * (GRID_WIDTH + GRID_HEIGHT/2 - 0.5) + PADDING_X * 2)
SCREEN_HEIGHT = int(HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5) + PADDING_Y * 2)

class Window():
	def __init__(self):
		if GRAPHICS_ENABLED:
			pygame.init()
			pygame.display.set_caption("Hex")
			pygame.font.init()
			
			self.root      = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
			self.grid_area = pygame.Surface((int(HEXAGON_WIDTH * (GRID_WIDTH + GRID_HEIGHT/2 - 0.5)), int(HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5))))

class Game():
	def __init__(self):
		self.board            = [[0 for x in range(GRID_HEIGHT)] for y in range(GRID_WIDTH)]
		self.playerColours    = {-1: (200, 0, 0), 0: (255, 255, 255), 1: (0, 0, 200)}
		self.currentPlayer    = 1
		self.totalMoves       = 0
		self.totalEvaluations = 0
		self.isGameWon        = False
		self.isGameRunning    = False
		self.gameWindow       = Window()
		
	def getPossibleMoves(self, player, move):
		possibleMoves = {}
		for x in range(0, GRID_WIDTH):
			for y in range(0, GRID_HEIGHT):
				if self.board[x][y] == 1:
					if player == -1 and move == 1:
						possibleMoves[(x, y)] = 0
				if self.board[x][y] == 0:
					possibleMoves[(x, y)] = 0
		return possibleMoves
		
	def evaluateGame(self):
		paths = {-1: [], 1: []}
		scores = {-1: float('inf'), 1: float('inf')}
		
		for p in (1, -1):
			paths[p] = self.findPath(p)
			if len(paths[p]) > 0:
				scores[p] = len(paths[p]) - paths[p].count(p)
			else:
				scores[p] = float('inf')
				
		self.totalEvaluations += 1
		return scores[-1] - scores[1]
		
	def findPath(self, player):
		frontier = []
		cameFrom = {}
		costSoFar = {}
		
		if player == 1:
			for x in range(0, GRID_WIDTH):
				if self.board[x][0] in [player, 0]:
					frontier.append((0, (x, 0)))
					cameFrom[(x, 0)] = "start"
					costSoFar[(x, 0)] = (self.board[x][0] != player)
		else:
			for y in range(0, GRID_HEIGHT):
				if self.board[0][y] in [player, 0]:
					frontier.append((0, (0, y)))
					cameFrom[(0, y)] = "start"
					costSoFar[(0, y)] = (self.board[0][y] != player)
			
		while len(frontier) > 0:
			current = frontier.pop(0)[1]
			if (current[1] == GRID_HEIGHT-1 and player == 1) or (current[0] == GRID_WIDTH-1 and player == -1):
				if "goal" not in cameFrom or costSoFar[current] < costSoFar["goal"]:
					costSoFar["goal"] = costSoFar[current]
					cameFrom["goal"] = current
			
			neighbours = [(current[0], current[1]-1), (current[0]+1, current[1]-1), (current[0]-1, current[1]), (current[0]+1, current[1]), (current[0]-1, current[1]+1), (current[0], current[1]+1)]
			valid = []
				
			for n in neighbours:
				if n[0] < GRID_WIDTH and n[1] < GRID_HEIGHT and n[0] >= 0 and n[1] >= 0:
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
				
	def alphaBeta(self, player, move, depth, alpha, beta):
		possibleMoves = self.getPossibleMoves(player, move)
		if depth == 0 or len(possibleMoves) == 0:
			return self.evaluateGame()
		else:
			if player == 1:
				result = float('-inf')
				for m in possibleMoves:
					t = self.board[m[0]][m[1]]
					self.board[m[0]][m[1]] = player
					result = max(result, self.alphaBeta(-1, move+1, depth-1, alpha, beta))
					self.board[m[0]][m[1]] = t
					if result >= beta or result == float('inf'):
						break
					alpha = max(alpha, result)
				return result
			else:
				result = float('inf')
				for m in possibleMoves:
					t = self.board[m[0]][m[1]]
					self.board[m[0]][m[1]] = player
					result = min(result, self.alphaBeta(1, move+1, depth-1, alpha, beta))
					self.board[m[0]][m[1]] = t
					if result <= alpha or result == float('-inf'):
						break
					beta = min(beta, result)
				return result
				
	def miniMax(self, player, move, depth):
		possibleMoves = self.getPossibleMoves(player, move)
		if depth == 0 or len(possibleMoves) == 0:
			return self.evaluateGame()
		else:
			if player == 1:
				result = float('-inf')
				for m in possibleMoves:
					t = self.board[m[0]][m[1]]
					self.board[m[0]][m[1]] = player
					result = max(result, self.miniMax(-player, move+1, depth-1))
					self.board[m[0]][m[1]] = t
					if result == float('inf'):
						break
				return result
			else:
				result = float('inf')
				for m in possibleMoves:
					t = self.board[m[0]][m[1]]
					self.board[m[0]][m[1]] = player
					result = min(result, self.miniMax(-player, move+1, depth-1))
					self.board[m[0]][m[1]] = t
					if result == float('-inf'):
						break
				return result
					
	def pickMove(self, player):
		possibleMoves = self.getPossibleMoves(player, self.totalMoves)
		bestScore = float('-inf') * player
		
		for m in possibleMoves:
			t = self.board[m[0]][m[1]]
			self.board[m[0]][m[1]] = player
			if SEARCH_PRUNING:
				possibleMoves[m] = self.alphaBeta(-player, self.totalMoves+1, SEARCH_DEPTH-1, float('-inf'), float('inf'))
			else:
				possibleMoves[m] = self.miniMax(-player, self.totalMoves+1, SEARCH_DEPTH-1)
			self.board[m[0]][m[1]] = t
			if player == 1:
				bestScore = max(bestScore, possibleMoves[m])
			else:
				bestScore = min(bestScore, possibleMoves[m])
			if possibleMoves[m] == float('inf') * player:
				break
			
		bestPossibleMoves = {}
		for m, s in possibleMoves.items():
			if s == bestScore:
				bestPossibleMoves[m] = s

		print("Best Score: %s " % bestScore, end="")
		if bestScore == float('-inf') * player:
			print("[Impossible to Win]")
		elif bestScore == float('inf') * player:
			print("[Guaranteed to Win]")
		else:
			print("")
			
		print("Best Moves: %s " % list(bestPossibleMoves.keys()))
		move, _ = random.choice(list(bestPossibleMoves.items()))
		print("Move Chosen: %s" % str(move))
		
		return move
	
	def runGame(self):
		self.isGameRunning = True
		gameStartTime = time.time()
		gameTotalTime = 0
		
		while self.isGameRunning:
			if GRAPHICS_ENABLED:
				self.drawGame()
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
			if not self.isGameWon:
				moveStartTime = time.time()
				
				print("\nPLAYER %s'S TURN.\n" % self.currentPlayer)
										
				move = self.pickMove(self.currentPlayer)
				self.board[move[0]][move[1]] = self.currentPlayer
				self.totalMoves += 1
				
				moveEndTime = time.time()
				gameTotalTime += (moveEndTime-moveStartTime)
					
				score = self.evaluateGame()
				
				print("Current Score: %s " % score)
				print("Advantage: ", end="") 
				if score == float('inf') * self.currentPlayer:
					print("Player %i" % self.currentPlayer)
					self.isGameWon = True
				elif score == 0:
					print("None")
				else:
					print("Player %i" % int(score / abs(score)))
				
				print("Time Taken: %ss" % str(moveEndTime-moveStartTime))
				
				if self.isGameWon:
					self.winningPath = self.findPath(self.currentPlayer)
					print("\nPLAYER %s WINS!" % self.currentPlayer)
					print("Total Moves: %s" % self.totalMoves)
					print("Total Evaluations: %s" % self.totalEvaluations)
					print("Total Time Taken: %ss" % gameTotalTime)
					if not GRAPHICS_ENABLED:
						exit()
				else:
					self.currentPlayer = -self.currentPlayer
					
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
		
		if self.isGameWon:
			points = [((p[0]+0.5) * HEXAGON_WIDTH + p[1] * 0.5 * HEXAGON_WIDTH, 0.5*HEXAGON_SIZE*2 + 0.75*p[1]*HEXAGON_SIZE*2) for p in self.winningPath]
			pygame.draw.lines(self.gameWindow.grid_area, 'yellow', False, points, int(HEXAGON_SIZE/4))
			for p in points:
				pygame.draw.circle(self.gameWindow.grid_area, self.playerColours[self.currentPlayer], p, int(HEXAGON_SIZE/4 * 1.3))
				pygame.draw.circle(self.gameWindow.grid_area, 'yellow', p, int(HEXAGON_SIZE/4))
		
		self.gameWindow.root.blit(self.gameWindow.grid_area, (PADDING_X, PADDING_Y))
		pygame.display.flip()
		
game = Game()
game.runGame()
