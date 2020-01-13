import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import math
import ctypes

WHITE = (255,255,255)
PIPE_HEIGHT = 860.0
PIPE_WIDTH = 75.0

class Top_pipe(pygame.sprite.Sprite):
	"""
	Represents the top pipe
	Derived from Sprite class in pygame
	"""

	def __init__(self, bottom_pipe, image, scorezone_height = 200, h_scale = 1, v_scale = 1):
		super().__init__()

		self.h_scale = h_scale
		
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = bottom_pipe.rect.x
		self.rect.y = bottom_pipe.rect.y - ((PIPE_HEIGHT + scorezone_height) * v_scale)

	def update(self):
		self.rect.x -= int(5 * self.h_scale)
		if self.rect.right <= 0:
			self.kill()

class Bottom_pipe(pygame.sprite.Sprite):
	"""
	Represents the bottom pipe
	Derived from Sprite class in pygame
	"""

	def __init__(self, image, scorezone_height = 200, horiz_scale = 1.0, verti_scale = 1.0, SCREEN_WIDTH = 1280, SCREEN_HEIGHT = 720):
		super().__init__()
		
		self.h_scale = horiz_scale
		self.v_scale = verti_scale

		self.image = image
		self.rect = self.image.get_rect()
		
		MAGIC_HEIGHT_NUM = math.ceil((SCREEN_HEIGHT - (600 * self.v_scale)) / 2)
		self.rect.x = SCREEN_WIDTH + 1
		self.rect.y = random.randint(math.ceil(scorezone_height * self.v_scale + MAGIC_HEIGHT_NUM), math.ceil(SCREEN_HEIGHT - MAGIC_HEIGHT_NUM))

	def update(self):
		self.rect.x -= int(5 * self.h_scale)
		if self.rect.right <= 0:
			self.kill()

class Between_pipe(pygame.sprite.DirtySprite):

	def __init__(self, bottom_pipe, scorezone_height = 200, horiz_scale = 1.0, verti_scale = 1.0):
		super().__init__()

		self.h_scale = horiz_scale
		self.v_scale = verti_scale
		
		self.image = pygame.Surface([PIPE_WIDTH * self.h_scale, scorezone_height * self.v_scale])
		self.rect = self.image.get_rect()
		self.rect.x = bottom_pipe.rect.x
		self.rect.y = bottom_pipe.rect.y - int(scorezone_height * self.v_scale)
		self.visible = 0

	def update(self):
		self.rect.x -= int(5 * self.h_scale)
		if self.rect.right <= 0:
			self.kill()
