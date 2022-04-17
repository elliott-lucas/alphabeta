import time
import random
import copy

from tictactoe import TicTacToe
from hex import Hex

SEARCH_DEPTH = 4

class GamePlayer():
	def __init__(self):
		self.totalTime        = 0
		self.totalEvaluations = 0
		
	def alphaBeta(self, game, depth, alpha, beta):
		possibleMoves = game.getPossibleMoves()
		if depth == 0 or len(possibleMoves) == 0:
			self.totalEvaluations += 1
			return game.getEvaluation()
		else:
			if game.currentPlayer == 1:
				result = float('-inf')
				for m in possibleMoves:
					g = copy.deepcopy(game)
					g.playMove(m)
					result = max(result, self.alphaBeta(g, depth-1, alpha, beta))
					if result >= beta or result == float('inf'):
						break
					alpha = max(alpha, result)
				return result
			else:
				result = float('inf')
				for m in possibleMoves:
					g = copy.deepcopy(game)
					g.playMove(m)
					result = min(result, self.alphaBeta(g, depth-1, alpha, beta))
					if result <= alpha or result == float('-inf'):
						break
					beta = min(beta, result)
				return result
		
	def chooseMove(self, game):
		possibleMoves = game.getPossibleMoves()
		
		if len(possibleMoves) == 0:
			return None
		else:
			bestScore = float('-inf') * game.currentPlayer
		
		for m in possibleMoves:
			g = copy.deepcopy(game)
			g.playMove(m)
			possibleMoves[m] = self.alphaBeta(g, SEARCH_DEPTH-1, float('-inf'), float('inf'))
			if game.currentPlayer == 1:
				bestScore = max(bestScore, possibleMoves[m])
			else:
				bestScore = min(bestScore, possibleMoves[m])
			
		bestPossibleMoves = {}
		for m, s in possibleMoves.items():
			if s == bestScore:
				bestPossibleMoves[m] = s
		
		print("Best Score: %s " % bestScore, end="")
		if bestScore == float('-inf') * game.currentPlayer:
			print("[Impossible to Win]")
		elif bestScore == float('inf') * game.currentPlayer:
			print("[Guaranteed to Win]")
		else:
			print("")
		
		print("Best Moves: %s " % list(bestPossibleMoves.keys()))
		move, _ = random.choice(list(bestPossibleMoves.items()))
		print("Move Chosen: %s" % str(move))
		
		return move
		
	def playGame(self, game):
		while not game.isGameOver:
			startTime = time.time()
				
			print("\nPLAYER %s'S TURN.\n" % game.currentPlayer)
			
			move = self.chooseMove(game)
			
			if move != None:
				game.playMove(move)
			else:
				game.isGameOver = True
				game.winningPlayer = 0
			
			endTime = time.time()
			self.totalTime += (endTime-startTime)
			
			print("Time Taken: %ss" % str(endTime-startTime))
			
			if game.isGameOver:
				if game.winningPlayer == 0:
					print("\nIT'S A DRAW!\n")
				else:
					print("\nPLAYER %s WINS!\n" % game.winningPlayer)
				print("Total Moves: %s" % game.totalMoves)
				print("Total Evaluations: %s" % self.totalEvaluations)
				print("Total Time Taken: %ss" % self.totalTime)
				
gamePlayer = GamePlayer()
gamePlayer.playGame(Hex())