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
		
	def playMove(self):
		raise NotImplementedError('Subclasses must override Game()!')
		
	def undoMove(self, t):
		self.__dict__.update(t)
		self.currentPlayer = -self.currentPlayer
		self.totalMoves -= 1
		self.isGameOver = False
		
	def drawGame(self):
		raise NotImplementedError('This game does not support graphics!')
		
	def getInput(self):
		raise NotImplementedError('This game does not support human players!')
	
class Window():
	def __init__(self, width, height, title):
		pygame.init()
		pygame.display.set_caption(title)
		
		self.root = pygame.display.set_mode((width, height))
