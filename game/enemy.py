import pygame 
from pygame.sprite import Sprite

class Enemy(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        # Load original image
        self.original_image = pygame.image.load('images/enemy.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        
        # Start each enemy at the top of the screen
        self.rect.midtop = self.screen_rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Damage tracking
        self.damage = 0

    def update(self):
        self.y += self.settings.enemy_speed
        self.rect.y = self.y

    def draw_enemy(self):
        self.screen.blit(self.image, self.rect)
    
    def got_hit(self):
        self.damage += 1
        # Make the enemy flash red when hit
        self.image = self.original_image.copy()
        if self.damage < 4:  # Only flash if not destroyed
            # Create a red overlay
            overlay = self.image.copy()
            overlay.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
            self.image.blit(overlay, (0, 0))
    
    def is_destroyed(self):
        return self.damage >= 3  # Destroy after 3 hits
        