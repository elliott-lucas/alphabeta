from game import Game

class TicTacToe(Game):
	def __init__(self):
		super().__init__()
		self.board = [[0 for y in range(3)] for x in range(3)]
	
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
				if self.board[x].count(p) == 3:
					scores[p] = float('inf')
			for y in range(0, 3):
				if [x[y] for x in self.board].count(p) == 3:
					scores[p] = float('inf')
			
			if [self.board[i][i] for i in range(0, 3)].count(p) == 3:
				scores[p] = float('inf')
				
			if [self.board[i][3-i] for i in range(1, 3)].count(p) == 3:
				scores[p] = float('inf')
				
		return scores[1] - scores[-1]
	
	def playMove(self, move):
		self.board[move[0]][move[1]] = self.currentPlayer
		self.totalMoves += 1
		
		if self.getEvaluation() == float('inf') * self.currentPlayer:
			self.isGameOver = True
			self.winningPlayer = self.currentPlayer
		else:
			self.currentPlayer = -self.currentPlayer
