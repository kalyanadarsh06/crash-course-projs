class Settings:
    def __init__(self):
        '''Store game settings.'''
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 53)
        self.ship_speed_x = 0.75
        self.ship_speed_y = 0.75
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (41, 230, 255)
        self.enemy_speed = 0.25
        self.number_enemies = 5
    
    