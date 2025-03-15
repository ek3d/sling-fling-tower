import pygame
from utils import *


class Platform:
    def __init__(self, window, position, size = (72, 10), one_way = True):
        self.window = window
        
        self.rect = pygame.FRect(position, size)
        
        self.one_way = one_way
    
    
    def draw(self, camera_position, color):
        draw_platform = self.rect.move(-camera_position[0], -camera_position[1])
        pygame.draw.rect(self.window, color, draw_platform)
    
    
    def update(self, camera_position, delta_time):
        self.draw(camera_position, GRAY)


class MovingPlatform(Platform):
    def __init__(self, window, position, size = (72, 10), one_way = True):
        super().__init__(window, position, size)
        
        self.speed = 100
        self.real_speed = 1
    
    
    def update(self, camera_position, delta_time):
        if self.rect.left <= 20 or self.rect.right >= self.window.get_width() - 20:
            self.speed *= -1
        self.real_speed = self.speed * delta_time
        self.rect.x += self.real_speed
        self.draw(camera_position, GRAY)


class IcePlatform(Platform):
    def __init__(self, window, position, size = (72, 10), one_way = True):
        super().__init__(window, position, size)
    
    
    def update(self, camera_position, delta_time):
        self.draw(camera_position, LIGHT_BLUE)


class CrackedPlatform(Platform):
    def __init__(self, window, position, size = (72, 10), one_way = True):
        super().__init__(window, position, size)
        
        self.crack_timer = Timer(60, overflow = True)
        self.activated = False
        self.falling = False
        self.gravity = 400
    
    
    def update(self, camera_position, delta_time):
        self.draw(camera_position, BROWN)
        if self.activated:
            if self.crack_timer.update():
                self.rect.centery += self.gravity * delta_time
