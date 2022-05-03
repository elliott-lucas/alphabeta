from games import Game

class TwentyOne(Game):
	def __init__(self, graphics=True, human=True):
		super().__init__(graphics, human)
		self.nums = []
	
	def getPossibleMoves(self):
		if sum([n[1] for n in self.nums]) < 21:
			return {1: 0, 2: 0, 3: 0}
		else:
			return {}
	
	def getEvaluation(self):
		if sum([n[1] for n in self.nums]) >= 21:
			return self.nums[-1][0] * float('inf')
		else:
			return 0
	
	def playMove(self, move):
		t = {"nums": [row[:] for row in self.nums]}
		self.nums.append([self.currentPlayer, move])
		self.totalMoves += 1
		
		if self.getEvaluation() == float('inf') * self.currentPlayer:
			self.isGameOver = True
			self.winningPlayer = self.currentPlayer
		else:
			self.currentPlayer = -self.currentPlayer
			
		return t
