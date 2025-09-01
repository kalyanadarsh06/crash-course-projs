import sys
from types import new_class
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from enemy import Enemy
from random import randint, random

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")
        self.clock = pygame.time.Clock()
        self.ship = Ship(self)
        self.bg_color = self.settings.bg_color     
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.list_of_enemy_positions = []
        self.explosions = []
           
    def run_game(self):
        while True:
            self.clock.tick(750)
            if len(self.enemies) == 0:
                self._add_enemies()
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self.enemies.update()
            self._update_screen()
    
    def _add_enemies(self):
        
        for enemy_number in range(self.settings.number_enemies):
            enemy = Enemy(self)
            enemy.x = 0
            while enemy.x == 0 or enemy.x in self.list_of_enemy_positions:
                enemy.x = random() * self.settings.screen_width
            self.list_of_enemy_positions.append(enemy.x)
            enemy.rect.x = enemy.x
            enemy.rect.y = -self.settings.screen_height
            self.enemies.add(enemy)
    
    def _check_bullet_enemy_collisions(self):
        for bullet in self.bullets.copy():
            collided_enemy = pygame.sprite.spritecollideany(bullet, self.enemies)
            if collided_enemy:
                collided_enemy.got_hit()
                if collided_enemy.is_destroyed():
                    self.explosion_effect(collided_enemy.rect.x, collided_enemy.rect.y)
                    collided_enemy.kill()
                bullet.kill()
            elif bullet.rect.bottom <= 0:
                bullet.kill()
    
    def _check_enemy_bottom(self):
        for enemy in self.enemies:
            if enemy.rect.bottom >= self.screen_rect.bottom:
                enemy.kill()
                self.ship.loss_life()
                break

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()    
        
    
    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        
        # Draw bullets and enemies
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for enemy in self.enemies.sprites():
            enemy.draw_enemy()
            
        # Update and draw explosions
        current_time = pygame.time.get_ticks()
        explosions_to_remove = []
        
        for i, explosion in enumerate(self.explosions):
            # Remove explosion if animation is complete
            if explosion['frame'] >= len(getattr(self, 'explosion_frames', [])):
                explosions_to_remove.append(i)
                continue
                
            # Draw current frame
            frame = self.explosion_frames[explosion['frame']]
            self.screen.blit(frame, (explosion['x'], explosion['y']))
            
            # Update frame if enough time has passed (50ms per frame)
            if current_time - explosion['last_update'] > 50:
                explosion['frame'] += 1
                explosion['last_update'] = current_time
        
        # Remove completed explosions (in reverse order to avoid index issues)
        for i in sorted(explosions_to_remove, reverse=True):
            if i < len(self.explosions):
                self.explosions.pop(i)
        
        self._check_bullet_enemy_collisions()
        self._check_enemy_bottom()
        if self.ship.lives == 0:
            sys.exit()
        pygame.display.flip()
    
    def explosion_effect(self, x, y):
        # Load explosion frames once and store them
        if not hasattr(self, 'explosion_frames'):
            self.explosion_frames = []
            for i in range(1, 6):
                try:
                    img = pygame.image.load(f'images/exp{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (100, 100))
                    self.explosion_frames.append(img)
                except:
                    # If image loading fails, create a colored rectangle as fallback
                    surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                    pygame.draw.circle(surf, (255, 0, 0, 200), (50, 50), 50)
                    self.explosion_frames.append(surf)
        
        # Add new explosion to the list with its current frame and position
        self.explosions.append({
            'x': x,
            'y': y,
            'frame': 0,
            'last_update': pygame.time.get_ticks()
        })
        
    
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
    