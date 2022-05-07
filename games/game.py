import pygame

class Game(object):
	def __init__(self, graphics, human):
		self.currentPlayer = 1
		self.winningPlayer = None
		self.isGameOver    = False
		self.isGameRunning = True
		self.totalMoves    = 0
		self.graphics      = graphics
		self.human         = human
		
	def getPossibleMoves(self):
		raise NotImplementedError('Subclasses must override Game()!')
		
	def getEvaluation(self):
		raise NotImplementedError('Subclasses must override Game()!')
		
	def getInput(self):
		raise NotImplementedError('Subclasses must override Game()!')
		
	def playMove(self):
		raise NotImplementedError('Subclasses must override Game()!')
	
	def updateGame(self):
		self.totalMoves += 1
		if self.getEvaluation() == float('inf') * self.currentPlayer:
			self.isGameOver = True
			self.winningPlayer = self.currentPlayer
		self.currentPlayer = -self.currentPlayer
	
	def revertGame(self, t):
		self.__dict__.update(t)
		self.totalMoves -= 1
		self.currentPlayer = -self.currentPlayer
		self.isGameOver = False
		self.winningPlayer = None
		
	def drawGame(self):
		raise NotImplementedError('Subclasses must override Game()!')
	
class Window():
	def __init__(self, width, height, title):
		pygame.init()
		pygame.display.set_caption(title)
		
		self.root = pygame.display.set_mode((width, height))
