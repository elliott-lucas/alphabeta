import math
import random
import pygame
from pygame import gfxdraw

GRID_WIDTH  = 4
GRID_HEIGHT = 4

HEXAGON_SIZE   = 50
HEXAGON_WIDTH  = HEXAGON_SIZE * math.sqrt(3)
HEXAGON_HEIGHT = HEXAGON_SIZE * 2

PADDING_X = HEXAGON_SIZE
PADDING_Y = HEXAGON_SIZE

SCREEN_WIDTH  = int(math.sqrt(3)/2 * HEXAGON_SIZE * 2 * (GRID_WIDTH + math.floor(GRID_HEIGHT/2)) + PADDING_X * 2)
SCREEN_HEIGHT = int(HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5) + PADDING_Y * 2)


		
class Hexagon():
	def __init__(self, x, y):
		Hexagon.colors = {-1: (200, 0, 0), 0: (255, 255, 255), 1: (0, 0, 200)}
		self.x        = x
		self.y        = y
		self.owner    = 0
		self.selected = False
		self.color    = Hexagon.colors[self.owner]
		
	def setOwner(self, value):
		self.owner = value
		self.color = Hexagon.colors[self.owner]
		
	def drawHexagon(self, surface):
		pygame.gfxdraw.aapolygon(surface, [((self.x+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.y * HEXAGON_SIZE * math.sqrt(3)/2 + HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.y+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.color)
		pygame.gfxdraw.filled_polygon(surface, [((self.x+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.y * HEXAGON_SIZE * math.sqrt(3)/2 ++ HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.y+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], self.color)

		pygame.gfxdraw.aapolygon(surface, [((self.x+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.y * HEXAGON_SIZE * math.sqrt(3)/2 + HEXAGON_SIZE * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.y+0.675) * HEXAGON_SIZE * 1.5 + HEXAGON_SIZE * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (0,0,0))
		
	def drawSelected(self, surface):
		for r in range(0, int(HEXAGON_SIZE/4),3):
			pygame.gfxdraw.polygon(surface, [((self.x+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.y * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE-r) * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.y+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE-r) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (0,255,0))
			pygame.gfxdraw.aapolygon(surface, [((self.x+0.5) * HEXAGON_SIZE * math.sqrt(3) + self.y * HEXAGON_SIZE * math.sqrt(3)/2 + (HEXAGON_SIZE-r) * math.cos(2 * math.pi * (i / 6 + 1/12)), (self.y+0.675) * HEXAGON_SIZE * 1.5 + (HEXAGON_SIZE-r) * math.sin(2 * math.pi * (i / 6 + 1/12))) for i in range(6)], (0,255,0))

class Window():
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Hex")
		pygame.font.init()
		
		self.root      = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.grid_area = pygame.Surface((int(math.sqrt(3)/2 * HEXAGON_SIZE * 2 * (GRID_WIDTH + math.floor(GRID_HEIGHT/2))), int(HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5))))
		
		self.font      = pygame.font.SysFont("arialblack", 30)
		self.text_area = self.font.render("", False, (255, 255, 255))
		

class Game():
	def __init__(self):
		self.hexagons         = []
		self.hexagon_selected = [0,0]
		self.current_player   = 1
		self.first_turn       = True
		self.game_won 		  = False
		
		for i in range(0, GRID_WIDTH):
			self.hexagons.append([])
			for j in range(0, GRID_HEIGHT):
				self.hexagons[i].append(Hexagon(i, j))
				
		self.window = Window()
		
	def checkRoute(self, x, y, checked):
		checked.append([x, y])
		if self.hexagons[x][y].owner == 1 and y == GRID_HEIGHT - 1:
			return 1
		elif self.hexagons[x][y].owner == -1 and x == GRID_WIDTH - 1:
			return -1
		else:
			neighbours = [[x, y-1], [x+1, y-1], [x-1, y], [x+1, y], [x-1, y+1], [x, y+1]]
			
			for n in neighbours:
				if n[0] < GRID_WIDTH and n[1] < GRID_HEIGHT and n[0] >= 0 and n[1] >= 0:
					if n not in checked:
						if self.hexagons[n[0]][n[1]].owner == self.hexagons[x][y].owner:
							result = self.checkRoute(n[0], n[1], checked)
							if result != 0:
								return result
			return 0
	
	def run(self):
		running = True

		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()
					exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						exit()
						
					if self.game_won == False:
						if event.key == pygame.K_RIGHT:
							self.hexagon_selected[0] = min(self.hexagon_selected[0] + 1, GRID_WIDTH - 1)
						elif event.key == pygame.K_LEFT:
							self.hexagon_selected[0] = max(self.hexagon_selected[0] - 1, 0)
						elif event.key == pygame.K_DOWN:
							self.hexagon_selected[1] = min(self.hexagon_selected[1] + 1, GRID_HEIGHT - 1)
						elif event.key == pygame.K_UP:
							self.hexagon_selected[1] = max(self.hexagon_selected[1] - 1, 0)
						elif event.key == pygame.K_RETURN:
							if self.hexagons[self.hexagon_selected[0]][self.hexagon_selected[1]].owner == 0 or (self.current_player == -1 and self.first_turn):
								self.hexagons[self.hexagon_selected[0]][self.hexagon_selected[1]].setOwner(self.current_player)
								if (self.current_player == -1 and self.first_turn):
									self.first_turn = False
								
								if self.current_player == 1:
									for i in range(0, GRID_WIDTH):
										if self.hexagons[i][0].owner == 1 and self.game_won == False:
											result = self.checkRoute(i, 0, [])
											if result != 0:
												self.game_won = True
												self.window.text_area = self.window.font.render("Blue wins!", False, (255,255,255))
												
								else:
									for j in range(0, GRID_HEIGHT):
										if self.hexagons[0][j].owner == -1 and self.game_won == False:
											result = self.checkRoute(0, j, [])
											if result != 0:
												self.game_won = True
												self.window.text_area = self.window.font.render("Red wins!", False, (255,255,255))
											
								self.current_player = -self.current_player
			self.draw()
	
	def draw(self):
		pygame.gfxdraw.aapolygon(self.window.grid_area, (
			(HEXAGON_WIDTH/2, 0), 
			(HEXAGON_WIDTH * (GRID_WIDTH-0.5), 0), 
			(HEXAGON_WIDTH * (GRID_WIDTH) + HEXAGON_WIDTH/2 * (GRID_HEIGHT - 2), HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5)), 
			(HEXAGON_WIDTH/2 * (GRID_HEIGHT), HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5))), (0,0,200))
	
		pygame.gfxdraw.filled_polygon(self.window.grid_area, (
			(HEXAGON_WIDTH/2, 0), 
			(HEXAGON_WIDTH * (GRID_WIDTH-0.5), 0), 
			(HEXAGON_WIDTH * (GRID_WIDTH) + HEXAGON_WIDTH/2 * (GRID_HEIGHT - 2), HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5)), 
			(HEXAGON_WIDTH/2 * (GRID_HEIGHT), HEXAGON_SIZE * (1.5 * GRID_HEIGHT + 0.5))), (0,0,200))
		
		pygame.gfxdraw.aapolygon(self.window.grid_area, (
			(0, 1.5 * HEXAGON_SIZE), 
			(GRID_WIDTH * HEXAGON_WIDTH, 0.5 * HEXAGON_SIZE), 
			(HEXAGON_WIDTH * (GRID_WIDTH) + HEXAGON_WIDTH/2 * (GRID_HEIGHT - 1), HEXAGON_SIZE * (1.5 * GRID_HEIGHT - 1)), 
			(HEXAGON_WIDTH/2 * (GRID_HEIGHT - 1), HEXAGON_SIZE * (1.5 * GRID_HEIGHT))), (200,0,0))
		
		pygame.gfxdraw.filled_polygon(self.window.grid_area, (
			(0, 1.5 * HEXAGON_SIZE), 
			(GRID_WIDTH * HEXAGON_WIDTH, 0.5 * HEXAGON_SIZE), 
			(HEXAGON_WIDTH * (GRID_WIDTH) + HEXAGON_WIDTH/2 * (GRID_HEIGHT - 1), HEXAGON_SIZE * (1.5 * GRID_HEIGHT - 1)), 
			(HEXAGON_WIDTH/2 * (GRID_HEIGHT - 1), HEXAGON_SIZE * (1.5 * GRID_HEIGHT))), (200,0,0))
	
		for i in self.hexagons:
			for j in i:
				j.drawHexagon(self.window.grid_area)
		
		self.hexagons[self.hexagon_selected[0]][self.hexagon_selected[1]].drawSelected(self.window.grid_area)
		
		self.window.root.blit(self.window.grid_area, (PADDING_X, PADDING_Y))
		self.window.root.blit(self.window.text_area, ((SCREEN_WIDTH - self.window.text_area.get_rect().width)/2, (PADDING_Y - self.window.text_area.get_rect().height)/2))
		pygame.display.flip()
		
game = Game()
game.run()
