import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import math

WHITE = (255,255,255)
PIPE_HEIGHT = 860

class Top_pipe(pygame.sprite.Sprite):
	"""
	Represents the top pipe
	Derived from Sprite class in pygame
	"""

	def __init__(self, bottom_pipe, scorezone_height = 200):
		super().__init__()

		self.image = pygame.image.load("resources/top_pipe.png").convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = bottom_pipe.rect.x
		self.rect.y = bottom_pipe.rect.y - (PIPE_HEIGHT + scorezone_height)

	def update(self):
		self.rect.x -= 5
		if self.rect.right <= 0:
			self.kill()

class Bottom_pipe(pygame.sprite.Sprite):
	"""
	Represents the bottom pipe
	Derived from Sprite class in pygame
	"""

	def __init__(self, scorezone_height = 200):
		super().__init__()

		self.image = pygame.image.load("resources/bottom_pipe.png").convert()
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		
		SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
		MAGIC_HEIGHT_NUM = math.ceil((SCREEN_HEIGHT - 500) / 2)
		self.rect.x = SCREEN_WIDTH + 1
		self.rect.y = random.randint(scorezone_height + MAGIC_HEIGHT_NUM, SCREEN_HEIGHT - MAGIC_HEIGHT_NUM)

	def update(self):
		self.rect.x -= 5
		if self.rect.right <= 0:
			self.kill()

class Between_pipe(pygame.sprite.DirtySprite):

	def __init__(self, bottom_pipe, scorezone_height = 200):
		super().__init__()

		self.image = pygame.Surface([75, scorezone_height])
		self.rect = self.image.get_rect()
		self.rect.x = bottom_pipe.rect.x
		self.rect.y = bottom_pipe.rect.y - scorezone_height
		self.visible = 0

	def update(self):
		self.rect.x -= 5
		if self.rect.right <= 0:
			self.kill()
