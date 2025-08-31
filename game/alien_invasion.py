import sys
from types import new_class
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from enemy import Enemy

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bg_color = self.settings.bg_color     
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
           
    def run_game(self):
        while True:
            if len(self.enemies) == 0:
                self._add_enemies()
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self.enemies.update()
            self._update_screen()
    
    def _add_enemies(self):
        enemy = Enemy(self)
        enemy_width = enemy.rect.width
        available_space = self.settings.screen_width - (2 * enemy_width)
        enemy_spacing = available_space // (self.settings.number_enemies + 1)
        
        for enemy_number in range(self.settings.number_enemies):
            enemy = Enemy(self)
            enemy.x = enemy_width + enemy_number * (enemy_width + enemy_spacing)
            enemy.rect.x = enemy.x
            self.enemies.add(enemy)
    
    def _check_bullet_enemy_collisions(self):
        for bullet in self.bullets.copy():
            collided_enemy = pygame.sprite.spritecollideany(bullet, self.enemies)
            if collided_enemy:
                collided_enemy.got_hit()
                if collided_enemy.is_destroyed():
                    collided_enemy.kill()
                bullet.kill()
            elif bullet.rect.bottom > self.screen_rect.bottom:
                bullet.kill()
    
    def _check_enemy_bottom(self):
        for enemy in self.enemies:
            if enemy.rect.bottom >= self.screen_rect.bottom:
                enemy.kill()
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
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for enemy in self.enemies.sprites():
            enemy.draw_enemy()
        self._check_bullet_enemy_collisions()
        self._check_enemy_bottom()
        pygame.display.flip()
    
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()