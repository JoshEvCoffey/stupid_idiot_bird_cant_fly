import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math

WHITE = (255,255,255)
BIRD_WIDTH = 47.0
BIRD_HEIGHT = 30.0

class Bird(pygame.sprite.Sprite):
	"""
	Represents the bird
	Derived from Sprite class in pygame
	"""

	def __init__(self, h_scale = 1.0, v_scale = 1.0):
		super().__init__()
		
		self.image = pygame.image.load("resources/stupid_bird.png").convert()
		self.image = pygame.transform.scale(self.image, (int(BIRD_WIDTH * h_scale), int(BIRD_HEIGHT * h_scale)))
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()

	def moveTo(self, x, y):
		self.rect.x = x
		self.rect.y = y