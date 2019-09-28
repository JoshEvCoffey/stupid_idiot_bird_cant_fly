import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

WHITE = (255,255,255)

class Top_pipe(pygame.sprite.Sprite):
    """
    Represents the top pipe
    Derived from Sprite class in pygame
    """
    
    def __init__(self, bottom_pipe):
        super().__init__()
        
        self.image = pygame.image.load("resources/top_pipe.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = bottom_pipe.rect.x
        self.rect.y = bottom_pipe.rect.y - 1060
        
    def update(self):
        self.rect.x -= 5
        if self.rect.x + 75 < 0:
            self.kill()
        
class Bottom_pipe(pygame.sprite.Sprite):
    """
    Represents the bottom pipe
    Derived from Sprite class in pygame
    """
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load("resources/bottom_pipe.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 1152
        self.rect.y = random.randint(250, 598)
        
    def update(self):
        self.rect.x -= 5
        if self.rect.x + 75 < 0:
            self.kill()
        
class Between_pipe(pygame.sprite.DirtySprite):
        
        def __init__(self, bottom_pipe):
            super().__init__()
            
            self.image = pygame.Surface([75, 200])
            self.rect = self.image.get_rect()
            self.rect.x = bottom_pipe.rect.x
            self.rect.y = bottom_pipe.rect.y - 200
            self.visible = 0
        
        def update(self):
            self.rect.x -= 5
            if self.rect.x + 75 < 0:
                self.kill()
