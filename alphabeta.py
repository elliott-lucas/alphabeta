import time
import pygame

class AlphaBeta():
	def __init__(self):
		self.totalEvaluations = 0
		
	def alphaBeta(self, game, depth, alpha, beta):
		possibleMoves = game.getPossibleMoves()
		if depth == 0 or len(possibleMoves) == 0:
			self.totalEvaluations += 1
			return game.getEvaluation()
		if game.currentPlayer == 1:
			result = float('-inf')
			for m in possibleMoves:
				t = game.playMove(m)
				result = max(result, self.alphaBeta(game, depth-1, alpha, beta))
				game.revertGame(t)
				if result >= beta or result == float('inf'):
					break
				alpha = max(alpha, result)
			return result
		else:
			result = float('inf')
			for m in possibleMoves:
				t = game.playMove(m)
				result = min(result, self.alphaBeta(game, depth-1, alpha, beta))
				game.revertGame(t)
				if result <= alpha or result == float('-inf'):
					break
				beta = min(beta, result)
			return result
			
	def miniMax(self, game, depth):
		possibleMoves = game.getPossibleMoves()
		if depth == 0 or len(possibleMoves) == 0:
			self.totalEvaluations += 1
			return game.getEvaluation()
		if game.currentPlayer == 1:
			result = float('-inf')
			for m in possibleMoves:
				t = game.playMove(m)
				result = max(result, self.miniMax(game, depth-1))
				game.revertGame(t)
				if result == float('inf'):
					break
			return result
		else:
			result = float('inf')
			for m in possibleMoves:
				t = game.playMove(m)
				result = min(result, self.miniMax(game, depth-1))
				game.revertGame(t)
				if result == float('-inf'):
					break
			return result
		
	def chooseMove(self, game, depth, prune):
		possibleMoves = game.getPossibleMoves()
		bestScore = float('-inf') * game.currentPlayer
		
		if len(possibleMoves) == 0:
			return None
		
		for m in possibleMoves:
			t = game.playMove(m)
			if prune:
				possibleMoves[m] = self.alphaBeta(game, depth-1, float('-inf'), float('inf'))
			else:
				possibleMoves[m] = self.miniMax(game, depth-1)
			game.revertGame(t)
			if game.currentPlayer == 1:
				bestScore = max(bestScore, possibleMoves[m])
			else:
				bestScore = min(bestScore, possibleMoves[m])
				
		move = list(possibleMoves.keys())[list(possibleMoves.values()).index(bestScore)]
		
		return move

	def playGame(self, game, depth, prune=True):
		self.totalEvaluations = 0
		startTime = time.time()
		game.drawGame()
		
		while game.isGameRunning:
			if not game.isGameOver:
				print("\nPLAYER %s'S TURN.\n" % game.currentPlayer)
				
				if (game.human and game.currentPlayer == 1):
					move = game.getInput()
					game.playMove(move)
					print("You chose %s" % str(move))
					
				else:
					print("Thinking...")
					move = self.chooseMove(game, depth, prune)
					
					if move == None:
						game.isGameOver = True
						game.winningPlayer = 0
					else:
						print("Player %s chooses %s" % (game.currentPlayer, move))
						game.playMove(move)
				
				game.drawGame()
				if game.isGameOver:
					if game.winningPlayer == 0:
						print("\nIT'S A DRAW!\n")
					else:
						print("\nPLAYER %s WINS!\n" % game.winningPlayer)
					print("Total Moves: %s" % game.totalMoves)
					print("Total Evaluations: %s" % self.totalEvaluations)
					if not game.graphics:
						game.isGameRunning = False
					
					endTime = time.time()
