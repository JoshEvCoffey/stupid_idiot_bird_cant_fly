import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math

WHITE = (255,255,255)
BIRD_WIDTH = 47.0
BIRD_HEIGHT = 30.0
BIRD_HITBOX_HEIGHT = 30.0
BIRD_HITBOX_WIDTH = 25.0

class Bird(pygame.sprite.Sprite):
	"""
	Represents the bird
	Derived from Sprite class in pygame
	"""

	def __init__(self, h_scale = 1.0, v_scale = 1.0):
		super().__init__()
		self.h_scale = h_scale
		self.v_scale = v_scale
		self.orig_image = pygame.image.load(os.path.join(os.path.dirname(__file__), "resources/stupid_bird.png")).convert_alpha()
		self.orig_image = pygame.transform.scale(self.orig_image, (int(BIRD_WIDTH * h_scale), int(BIRD_HEIGHT * v_scale)))
		self.image = self.orig_image
		self.rect = self.image.get_rect()
		self.hitbox = self.rect.copy()
		self.hitbox.w = BIRD_HITBOX_WIDTH * self.h_scale
		self.hitbox.h = BIRD_HITBOX_HEIGHT * self.v_scale
		self.hitbox.center = self.rect.center
		self.angle = 0

	def moveTo(self, x, y):
		self.rect.center = (x, y)
		self.hitbox.center = self.rect.center
		
	def rot_center(self, angle):
		center = self.rect.center
		self.angle += angle % 360
		self.image = pygame.transform.rotate(self.orig_image, self.angle)
		self.rect = self.image.get_rect(center = center)
		self.hitbox = self.rect.copy()
		self.hitbox.w = BIRD_HITBOX_WIDTH * self.h_scale
		self.hitbox.h = BIRD_HITBOX_HEIGHT * self.v_scale
		self.hitbox.center = self.rect.center