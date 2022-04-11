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

HEXAGON_SIZE   = 50
HEXAGON_WIDTH  = HEXAGON_SIZE * math.sqrt(3)
HEXAGON_HEIGHT = HEXAGON_SIZE * 2

PADDING_X = HEXAGON_SIZE
PADDING_Y = HEXAGON_SIZE

SCREEN_WIDTH  = int(math.sqrt(3)/2 * HEXAGON_SIZE * 2 * (GRID_WIDTH + math.floor(GRID_HEIGHT/2)) + PADDING_X * 2)
SCREEN_HEIGHT = int(HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5) + PADDING_Y * 2)

class Window():
	def __init__(self):
		if GRAPHICS_ENABLED:
			pygame.init()
			pygame.display.set_caption("Hex")
			pygame.font.init()
			
			self.root      = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
			self.grid_area = pygame.Surface((int(math.sqrt(3)/2 * HEXAGON_SIZE * 2 * (GRID_WIDTH + math.floor(GRID_HEIGHT/2))), int(HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5))))

class Game():
	def __init__(self):
		self.board          = [[0 for x in range(GRID_HEIGHT)] for y in range(GRID_WIDTH)]
		self.playerColours  = {-1: (200, 0, 0), 0: (255, 255, 255), 1: (0, 0, 200)}
		self.currentPlayer  = 1
		self.isFirstTurn    = True
		self.isGameWon      = False
		self.isGameRunning  = False
		self.gameWindow     = Window()
		
	def getPossibleMoves(self, board, player):
		possibleMoves = {}
		for x in range(0, GRID_WIDTH):
			for y in range(0, GRID_HEIGHT):
				if board[x][y] == 1:
					if player == -1 and self.isFirstTurn:
						possibleMoves[(x, y)] = 0
				if board[x][y] == 0:
					possibleMoves[(x, y)] = 0
		return possibleMoves

	def findPath(self, player):
		frontier = []
		cameFrom = {}
		costSoFar = {}
		
		if player == 1:
			for x in range(0, GRID_WIDTH):
				if self.board[x][0] in [player, 0]:
					frontier.append((0, (x, 0)))
					cameFrom[(x, 0)] = "start"
					costSoFar[(x, 0)] = 0
		else:
			for y in range(0, GRID_HEIGHT):
				if self.board[0][y] in [player, 0]:
					frontier.append((0, (0, y)))
					cameFrom[(0, y)] = "start"
					costSoFar[(0, y)] = 0
			
		while len(frontier) > 0:
			current = frontier.pop(0)[1]
			if (current[1] == GRID_HEIGHT-1 and player == 1) or (current[0] == GRID_WIDTH-1 and player == -1):
				cameFrom["goal"] = current
				break
			
			neighbours = [(current[0], current[1]-1), (current[0]+1, current[1]-1), (current[0]-1, current[1]), (current[0]+1, current[1]), (current[0]-1, current[1]+1), (current[0], current[1]+1)]
			valid = []
				
			for n in neighbours:
				if n[0] < GRID_WIDTH and n[1] < GRID_HEIGHT and n[0] >= 0 and n[1] >= 0:
					if self.board[n[0]][n[1]] in [player, 0]:
						valid.append(n)
				
			for n in valid:
				cost = costSoFar[current] + 1
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
		
	def evaluateGame(self, board):
		paths = {-1: [], 1: []}
		scores = {-1: float('inf'), 1: float('inf')}
		
		for p in (1, -1):
			paths[p] = self.findPath(p)
			if len(paths[p]) > 0:
				scores[p] = len(paths[p]) - paths[p].count(p)
			else:
				scores[p] = float('inf')
				
		return scores[-1] - scores[1], paths
				
	def alphaBeta(self, board, depth, player, alpha, beta):
		possibleMoves = self.getPossibleMoves(board, player)
		if depth == 0 or len(possibleMoves) == 0:
			return self.evaluateGame(board)[0]
		else:
			if player == 1:
				for m in possibleMoves:
					t = self.board[m[0]][m[1]]
					board[m[0]][m[1]] = player
					result = self.alphaBeta(board, depth - 1, -1, alpha, beta)
					board[m[0]][m[1]] = t
					if result >= beta or result == float('inf'):
						break
					alpha = max(alpha, result)
				return result
			else:
				for m in possibleMoves:
					t = self.board[m[0]][m[1]]
					board[m[0]][m[1]] = player
					result = self.alphaBeta(board, depth - 1, 1, alpha, beta)
					board[m[0]][m[1]] = t
					if result <= alpha or result == float('-inf'):
						break
					beta = min(beta, result)
				return result
				
	def miniMax(self, board, depth, player):
		possibleMoves = self.getPossibleMoves(board, player)
		if depth == 0 or len(possibleMoves) == 0:
			return self.evaluateGame(board)[0]
		else:
			if player == 1:
				best = float('-inf')
				for m in possibleMoves:
					t = self.board[m[0]][m[1]]
					board[m[0]][m[1]] = player
					result = self.miniMax(board, depth - 1, -1)
					board[m[0]][m[1]] = t
					if result >= best:
						best = result
						if best == float('inf'):
							break
				return best
			else:
				best = float('inf')
				for m in possibleMoves:
					t = self.board[m[0]][m[1]]
					board[m[0]][m[1]] = player
					result = self.miniMax(board, depth - 1, 1)
					board[m[0]][m[1]] = t
					if result <= best:
						best = result
						if best == float('-inf'):
							break
				return best
					
	def pickMove(self, player):
		possibleMoves = self.getPossibleMoves(self.board, player)
		bestScore = float('-inf') * player
		
		for m in possibleMoves:
			t = self.board[m[0]][m[1]]
			self.board[m[0]][m[1]] = player
			if SEARCH_PRUNING:
				possibleMoves[m] = self.alphaBeta(self.board, SEARCH_DEPTH-1, -player, float('-inf'), float('inf'))
			else:
				possibleMoves[m] = self.miniMax(self.board, SEARCH_DEPTH-1, -player)
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
			
		print("Moves: %s " % list(bestPossibleMoves.keys()))
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
					
				score, _ = self.evaluateGame(self.board)
										
				print("Current Score: %s " % score)
				print("Advantage: ", end="") 
				if score == float('inf') * self.currentPlayer:
					print("Player %i wins!" % self.currentPlayer)
					self.isGameWon = True
				elif score == 0:
					print("None")
				else:
					print("Player %i" % int(score / abs(score)))
						
				if (self.currentPlayer == -1 and self.isFirstTurn):
					self.isFirstTurn = False
					
				self.currentPlayer = -self.currentPlayer	
				
				moveEndTime = time.time()
				gameTotalTime += (moveEndTime-moveStartTime)
				
				print("Time Taken: %ss" % str(moveEndTime-moveStartTime))
				
				if self.isGameWon:
					print("\nGAME OVER.")
					print("Total Time Taken: %ss" % gameTotalTime)
					
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
		
		self.gameWindow.root.blit(self.gameWindow.grid_area, (PADDING_X, PADDING_Y))
		pygame.display.flip()
		
game = Game()
game.runGame()
