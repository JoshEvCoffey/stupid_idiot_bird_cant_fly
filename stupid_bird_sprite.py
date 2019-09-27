import pygame

WHITE = (255,255,255)

class Bird(pygame.sprite.Sprite):
    """
    Represents the bird
    Derived from Sprite class in pygame
    """
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load("stupid_bird.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        
    def moveTo(self, x, y):
        self.rect.x = x
        self.rect.y = y