from games import Game, Window
import pygame
import math

SQUARE_SIZE = 50

PADDING_X = SQUARE_SIZE
PADDING_Y = SQUARE_SIZE

class TicTacToe(Game):
	def __init__(self, graphics, human):
		super().__init__(graphics, human)
		self.board = [[0 for y in range(3)] for x in range(3)]
		
		if self.graphics:
			self.window = Window(SQUARE_SIZE * 3 + PADDING_X * 2, SQUARE_SIZE * 3 + PADDING_X * 2, "Tic Tac Toe")
			self.window.grid_area = self.grid_area = pygame.Surface((SQUARE_SIZE * 3, SQUARE_SIZE * 3))
			self.window.colours = {-1: (200, 0, 0), 0: (255, 255, 255), 1: (0, 0, 200)}
			if self.human:
				self.currentSquare = [0,0]
	
	def getPossibleMoves(self):
		possibleMoves = {}
		for x in range(0, 3):
			for y in range(0, 3):
				if self.board[x][y] == 0:
					possibleMoves[(x, y)] = 0
		return possibleMoves
	
	def getEvaluation(self):
		scores = {-1: 0, 1: 0}
		
		for p in [1, -1]:
			for x in range(0, 3):
				if self.board[x][0] == self.board[x][1] == self.board[x][2] == p:
					scores[p] = float('inf')
			for y in range(0, 3):
				if self.board[0][y] == self.board[1][y] == self.board[2][y] == p:
					scores[p] = float('inf')
			if self.board[0][0] == self.board[1][1] == self.board[2][2] == p:
				scores[p] = float('inf')
			if self.board[0][2] == self.board[1][1] == self.board[2][0] == p:
				scores[p] = float('inf')
				
		return scores[1] - scores[-1]
	
	def playMove(self, move):
		t = {"board": [row[:] for row in self.board]}
		self.board[move[0]][move[1]] = self.currentPlayer
		
		self.updateGame()
			
		return t
		
	def drawGame(self):
		if self.graphics:
			for x in range(0, len(self.board)):
				for y in range(0, len(self.board[x])):
					pygame.draw.rect(self.window.grid_area, self.window.colours[self.board[x][y]], (SQUARE_SIZE*x, SQUARE_SIZE*y, SQUARE_SIZE, SQUARE_SIZE))
					pygame.draw.rect(self.window.grid_area, (0,0,0), (SQUARE_SIZE*x, SQUARE_SIZE*y, SQUARE_SIZE, SQUARE_SIZE), 1)
			
			if self.human and not self.isGameOver and self.currentPlayer == 1:
					pygame.draw.rect(self.window.grid_area, tuple(min(255, c+150) for c in self.window.colours[self.currentPlayer]), (SQUARE_SIZE*self.currentSquare[0], SQUARE_SIZE*self.currentSquare[1], SQUARE_SIZE, SQUARE_SIZE))
					pygame.draw.rect(self.window.grid_area, (0,0,0), (SQUARE_SIZE*self.currentSquare[0], SQUARE_SIZE*self.currentSquare[1], SQUARE_SIZE, SQUARE_SIZE), 1)
			
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
							self.currentSquare[1] = max(0, self.currentSquare[1] - 1)
						elif event.key == pygame.K_DOWN:
							self.currentSquare[1] = min(2, self.currentSquare[1] + 1)
						elif event.key == pygame.K_LEFT:
							self.currentSquare[0] = max(0, self.currentSquare[0] - 1)
						elif event.key == pygame.K_RIGHT:
							self.currentSquare[0] = min(2, self.currentSquare[0] + 1)
						elif event.key == pygame.K_RETURN:
							if tuple(self.currentSquare) in self.getPossibleMoves():
								return tuple(self.currentSquare)
		else:
			x = -1
			y = -1
			
			while not (0 <= x < 2 and 0 <= y < 2 and self.board[x][y] == 0): 
				x = int(input("\nX: "))
				y = int(input("Y: "))
				if not (0 <= x < 2 and 0 <= y < 2 and self.board[x][y] == 0):
					print("\nInvalid grid position.")
			
			return (x,y)
