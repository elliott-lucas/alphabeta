from games import Game

class TwentyOne(Game):
	def __init__(self, graphics, human):
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
			
	def getInput(self):
		while True:
			num = input("Pick a number [1, 2 or 3]: ")
			if num.isdigit():
				if int(num) >= 1 and int(num) <= 3:
					return int(num)
				else:
					print("Number must be between 1 and 3.")
			else:
				print("Not a number.")
	
	def playMove(self, move):
		t = {"nums": [row[:] for row in self.nums]}
		self.nums.append([self.currentPlayer, move])
		
		self.updateGame()
			
		return t
		
	def drawGame(self):
		print("The current sum is %s" % sum([n[1] for n in self.nums]))
