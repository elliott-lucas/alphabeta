from game import Game

GRID_WIDTH  = 4
GRID_HEIGHT = 4
SWAP_RULE   = True

class Hex(Game):
	def __init__(self):
		super().__init__()
		self.board = [[0 for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
		
	def getPossibleMoves(self):
		possibleMoves = {}
		for x in range(0, GRID_WIDTH):
			for y in range(0, GRID_HEIGHT):
				if SWAP_RULE and self.board[x][y] == 1 and self.currentPlayer == -1 and self.totalMoves == 1:
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
		self.board[move[0]][move[1]] = self.currentPlayer
		self.totalMoves += 1
		
		if self.getEvaluation() == float('inf') * self.currentPlayer:
			self.isGameOver = True
			self.winningPlayer = self.currentPlayer
		else:
			self.currentPlayer = -self.currentPlayer
		
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