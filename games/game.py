class Game(object):
	def __init__(self):
		self.currentPlayer = 1
		self.totalMoves    = 0
		self.isGameOver    = False
		self.winningPlayer = None
		
	def getPossibleMoves(self):
		raise NotImplementedError('Subclasses must override Game()!')
		
	def getEvaluation(self):
		raise NotImplementedError('Subclasses must override Game()!')
		
	def playMove(self):
		raise NotImplementedError('Subclasses must override Game()!')
