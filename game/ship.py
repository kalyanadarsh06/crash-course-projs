import pygame
import sys
class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        self.image = pygame.image.load('images/spaceship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 189.32))
        self.rect = self.image.get_rect()
        
        self.rect.midbottom = self.screen_rect.midbottom
    
    def blitme(self):
        self.screen.blit(self.image, self.rect)