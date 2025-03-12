import pygame
from utils import *


class Platform:
    def __init__(self, window, position, size = (72, 10)):
        self.window = window
        
        self.rect = pygame.Rect(position, size)
    
    
    def draw(self, camera_position):
        draw_platform = self.rect.move(-camera_position[0], -camera_position[1])
        pygame.draw.rect(self.window, GRAY, draw_platform)