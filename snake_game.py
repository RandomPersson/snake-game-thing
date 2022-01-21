import pygame
import time
import random
import math

pygame.init()

game_fps = 60
game_tps = 20

game_field_size = (8, 8)
grid_line_size = 2
pixel_size = 80
grid_size = pixel_size + grid_line_size
window_size = (
	grid_size * game_field_size[0] + grid_line_size,
	grid_size * game_field_size[1] + grid_line_size
)
display = pygame.display.set_mode((window_size[0], window_size[1]))
pygame.display.update()

pygame.display.set_caption('Snake thing')

color_apple = (200,0,0)
color_snake = (0,150,200)
color_grid = (150,150,150)
color_background = (42,42,42)

game_over = False

class Snake:
	def __init__(self, apple):
		self.body = [[0, 0]]
		self.apple = apple
		self.last_move = [1, 0]
		self.board = [[0 for x in range(game_field_size[0])] for y in range(game_field_size[1])]
	
	def grow(self):
		self.body = [self.body[-1]] + self.body
	
	def shrink(self):
		del self.body[0]
		self.board[self.body[0][0]][self.body[0][1]] -= 1
	
	def teleport(self, pos):
		self.body.append(pos)
		self.board[pos[0]][pos[1]] += 1
		self.shrink()
	
	def move(self, pos):
		self.teleport([self.body[-1][0] + pos[0], self.body[-1][1] + pos[1]])
	
	def moveAndCheckApple(self, pos):
		pos = [self.body[-1][0] + pos[0], self.body[-1][1] + pos[1]]
		if pos == self.apple:
			self.grow()
			randomizeApple(self, self.apple)
		self.teleport(pos)
	
	def moveAndCheckAppleAndDeath(self, pos):
		pos = [self.body[-1][0] + pos[0], self.body[-1][1] + pos[1]]
		if pos == self.apple:# apple collision
			print("apple collision")
			self.grow()
			randomizeApple(self, self.apple)
			print("in-snek apple check:", self.apple)
		if pos[0] < 0 or pos[0] >= game_field_size[0] or pos[1] < 0 or pos[1] >= game_field_size[1]:# wall collision
			print("wall collision")
			return True
		if self.board[pos[0]][pos[1]] == 1:# snake collision
			print("snek collision")
			return True
		self.teleport(pos)
		return False
	

class SquareWalkRel:
	def __init__(self):
		self.step = -1
		self.x = (
			[ 1 for x in range(game_field_size[0] - 1)] +
			[ 0 for x in range(game_field_size[1] - 1)] +
			[-1 for x in range(game_field_size[0] - 1)] +
			[ 0 for x in range(game_field_size[1] - 1)]
		)
		self.y = (
			[ 0 for y in range(game_field_size[0] - 1)] +
			[ 1 for y in range(game_field_size[1] - 1)] +
			[ 0 for y in range(game_field_size[0] - 1)] +
			[-1 for y in range(game_field_size[1] - 1)]
		)
	
	def next(self):
		self.step = (self.step+1) % (2*game_field_size[0] + 2*game_field_size[1] - 4)
		return [self.x[self.step], self.y[self.step]]



def getSquareCoordinates(x, y):
	return [x * grid_size + grid_line_size, (game_field_size[1] - 1 - y) * grid_size + grid_line_size]

def drawSnakePixel(x, y):
	pygame.draw.rect(display, color_snake, getSquareCoordinates(x, y) + [pixel_size, pixel_size])

def drawSnake(snake):
	for snake_pixel in snake.body:
		drawSnakePixel(snake_pixel[0], snake_pixel[1])

def drawApple(apple):
	pygame.draw.rect(display, color_apple, getSquareCoordinates(apple[0], apple[1]) + [pixel_size, pixel_size])

def drawGrid():
	for i in range(game_field_size[0] + 1):
		pygame.draw.rect(display, color_grid, [i * grid_size, 0, grid_line_size, window_size[1]])
	for i in range(game_field_size[1] + 1):
		pygame.draw.rect(display, color_grid, [0, i * grid_size, window_size[0], grid_line_size])

def drawEverything(snake, apple):
	display.fill(color_background)
	drawSnake(snake)
	drawApple(apple)
	drawGrid()
	pygame.display.update()

def randomizeApple(snake, apple):
	apple_pos = random.randrange(game_field_size[0]*game_field_size[1] - len(snake.body))
	
	pos_counter = 0
	non_snek_counter = 0
	try:
		while non_snek_counter != apple_pos:
			if snake.board[pos_counter % game_field_size[0]][math.floor(pos_counter / game_field_size[0])] == 0:
				non_snek_counter += 1
			pos_counter += 1
		
		apple[0] = pos_counter % game_field_size[0]
		apple[1] = math.floor(pos_counter / game_field_size[0])
	
	except IndexError:
		print("#### IndexError", [pos_counter % game_field_size[0], math.floor(pos_counter / game_field_size[0])])
		apple[0] = 0
		apple[1] = 0
	
	print("new apple:", [apple[0], apple[1]])

def getNextMoveFromKeyboard(keyboard):
	if keyboard[pygame.K_UP] or keyboard[pygame.K_w]:
		return [0, 1]
	if keyboard[pygame.K_DOWN] or keyboard[pygame.K_s]:
		return [0, -1]
	if keyboard[pygame.K_LEFT] or keyboard[pygame.K_a]:
		return [-1, 0]
	if keyboard[pygame.K_RIGHT] or keyboard[pygame.K_d]:
		return [1, 0]
	return [0, 0]

def gameLoop():
	apple = [0, 0]
	snake = Snake(apple)
	randomizeApple(snake, apple)
	
	drawEverything(snake, apple)
	
	game_tick = 1
	next_move = [0, 0]
	# snake.grow()# start with size 2
	
	while True:
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				return
			
			if event.type == pygame.KEYDOWN:
				keyboard = pygame.key.get_pressed()
				
				if keyboard[pygame.K_ESCAPE]:
					return
				
				potential_next_move = getNextMoveFromKeyboard(keyboard)
				
				if (potential_next_move != [0, 0]):
					next_move = potential_next_move
		
		if game_tick % game_tps == 0:
			if next_move == [0, 0]:
				next_move = snake.last_move
			else:
				snake.last_move = next_move
			
			if snake.moveAndCheckAppleAndDeath(next_move):
				print("snek ded")
				return
			drawEverything(snake, apple)
		
		game_tick += 1
		time.sleep(1/game_fps)

gameLoop()
pygame.quit()
