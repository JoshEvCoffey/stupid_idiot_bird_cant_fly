import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

GREEN = (0, 255, 0)
NUMBER_OF_CLOUDS = 6
CLOUD_WIDTH = 101
CLOUD_HEIGHT = 50

class Cloud(pygame.sprite.Sprite):
	""" Represents a cloud """
	
	def __init__(self, image, horiz_scale = 1.0, SCREEN_WIDTH = 1280, SCREEN_HEIGHT = 720):
		super().__init__()
		self.h_scale = horiz_scale
		self.image = image
		self.rect = self.image.get_rect()
		
		self.rect.x = SCREEN_WIDTH + 1
		self.rect.y = random.randint(50, SCREEN_HEIGHT - 50 - self.image.get_height())
		
	def update(self):
		self.rect.x -= int(3 * self.h_scale)
		if self.rect.right < 0:
			self.kill()
	