import pygame
from utils import *


class Rocket:
    def __init__(self, window, player, position, powerups, volume):
        self.window = window
        self.volume = volume
        
        self.player = player
        self.rect = pygame.Rect((0, 0), (12, 12))
        self.rect.center = position
        
        self.powerups = powerups
    
    
    def draw(self, camera_position):
        draw_rect = self.rect.move(-camera_position[0], -camera_position[1])
        pygame.draw.rect(self.window, RED, draw_rect, border_radius = 20)
    
    
    def update(self, camera_position):
        self.draw(camera_position)
        
        if self.rect.colliderect(self.player.player_rect):
            play_sound('assets/audio/sfx/rocket.ogg', self.volume)
            self.player.velocity.y = -1000
            self.powerups.remove(self)


class MultiSling:
    def __init__(self, window, player, position, powerups, volume):
        self.window = window
        self.window_middle = (window.get_width() / 2, window.get_height() / 2)
        self.volume = volume
        
        self.player = player
        self.rect = pygame.Rect((0, 0), (12, 12))
        self.rect.center = position
        
        self.activated = False
        self.can_touch = True
        self.timer = Timer(300)
        
        self.powerups = powerups
    
    
    def draw(self, camera_position):
        draw_rect = self.rect.move(-camera_position[0], -camera_position[1])
        if self.can_touch:
            pygame.draw.rect(self.window, GREEN, draw_rect, border_radius = 20)
        
        if self.activated:
            draw_text(self.window, (self.window_middle[0], self.window.get_height() - 30), 'Multi-Sling', 24, GREEN)
    
    
    def update(self, camera_position):
        self.draw(camera_position)
        
        if self.rect.colliderect(self.player.player_rect) and self.can_touch:
            play_sound('assets/audio/sfx/multi_sling.ogg', self.volume)
            self.activated = True
            self.can_touch = False
        
        if self.activated:
            if self.timer.update():
                self.activated = False
                self.player.multi_sling = False
                self.powerups.remove(self)
                return
            self.player.multi_sling = True


class Feather:
    def __init__(self, window, player, position, powerups, volume):
        self.window = window
        self.window_middle = (window.get_width() / 2, window.get_height() / 2)
        self.volume = volume
        
        self.player = player
        self.rect = pygame.Rect((0, 0), (12, 12))
        self.rect.center = position
        
        self.activated = False
        self.can_touch = True
        self.timer = Timer(300)
        
        self.powerups = powerups
    
    
    def draw(self, camera_position):
        draw_rect = self.rect.move(-camera_position[0], -camera_position[1])
        if self.can_touch:
            pygame.draw.rect(self.window, PURPLE, draw_rect, border_radius = 20)
        
        if self.activated:
            draw_text(self.window, (self.window_middle[0] - 75, self.window.get_height() - 30), 'Feather', 24, PURPLE)
    
    
    def update(self, camera_position):
        self.draw(camera_position)
        
        if self.rect.colliderect(self.player.player_rect) and self.can_touch:
            play_sound('assets/audio/sfx/feather.ogg', self.volume)
            self.activated = True
            self.can_touch = False
        
        if self.activated:
            if self.timer.update():
                self.activated = False
                self.player.gravity = 400
                self.powerups.remove(self)
                return
            self.player.gravity = 200
