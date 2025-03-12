import pygame
from utils import *


class Player:
    def __init__(self, window, position, volume):
        self.window = window
        self.volume = volume
        
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 400
        
        self.is_grounded = False
        
        self.player_rect = pygame.Rect((0, 0), (16, 24))
        self.player_rect.center = self.position
        
        self.aiming = False
        self.can_aim = True
        self.multi_sling = False
        self.multiplier = 7
        
        # Eyes
        self.left_eye_rect = pygame.Rect((0, 0), (2, 6))
        self.left_eye_rect.center = (self.position[0] - 2, self.position[1] - 3)
        
        self.right_eye_rect = pygame.Rect((0, 0), (2, 6))
        self.right_eye_rect.center = (self.position[0] + 2, self.position[1] - 3)
    
    
    def aim(self, events, camera_position):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.aiming = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.gravity < 400:
                    play_sound('assets/audio/sfx/feather.ogg', self.volume)
                elif self.multi_sling:
                    play_sound('assets/audio/sfx/multi_sling.ogg', self.volume)
                else:
                    play_sound('assets/audio/sfx/jump.ogg', self.volume * 0.25)
                self.aiming = False
                self.velocity = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(self.position) + pygame.Vector2(camera_position)
                self.velocity.y = min(self.velocity.y, -20)
        
        if self.aiming:
            aim_start = pygame.Vector2(self.position) - camera_position
            aim_end = pygame.mouse.get_pos()
            pygame.draw.line(self.window, WHITE, aim_start, aim_end, 6)
            pygame.draw.circle(self.window, WHITE, aim_end, 6)
            pygame.draw.circle(self.window, GRAY, aim_end, 4)
    
    
    def draw(self, camera_position):
        self.left_eye_rect.center = (self.position[0] - 2 + sign(self.velocity.x) * 3, self.position[1] - 3 + min(sign(self.velocity.y), 0) * 5)
        self.left_eye_rect.move_ip(-camera_position[0], -camera_position[1])
        self.right_eye_rect.center = (self.position[0] + 2+ sign(self.velocity.x) * 3, self.position[1] - 3 + min(sign(self.velocity.y), 0) * 5)
        self.right_eye_rect.move_ip(-camera_position[0], -camera_position[1])
        
        draw_player_rect = self.player_rect.move(-camera_position[0], -camera_position[1])
        pygame.draw.rect(self.window, WHITE, draw_player_rect, border_radius = 3)
        pygame.draw.rect(self.window, BLACK, self.left_eye_rect)
        pygame.draw.rect(self.window, BLACK, self.right_eye_rect)
    
    
    def movement(self, delta_time, platforms):
        if not self.is_grounded:
            self.velocity.y += self.gravity * delta_time
        
        self.position[0] += self.velocity.x * self.multiplier * delta_time
        self.player_rect.centerx = self.position[0]
        
        for platform in platforms:
            if self.player_rect.colliderect(platform.rect):
                if self.velocity.x < 0:
                    self.position[0] = platform.rect.right + (self.player_rect.width / 2)
                    play_sound('assets/audio/sfx/wall_bounce.ogg', self.volume)
                elif self.velocity.x > 0:
                    self.position[0] = platform.rect.left - (self.player_rect.width / 2)
                    play_sound('assets/audio/sfx/wall_bounce.ogg', self.volume)
                self.velocity.x *= -0.75
                self.player_rect.centerx = self.position[0]
                break
        
        self.position[1] += self.velocity.y * self.multiplier * delta_time
        self.player_rect.centery = self.position[1]
        
        for platform in platforms:
            if self.player_rect.colliderect(platform.rect):
                if self.velocity.y > 0:
                    self.position[1] = platform.rect.top - (self.player_rect.height / 2)
                self.velocity.x = 0
                self.player_rect.centery = self.position[1]
                self.can_aim = True
                self.is_grounded = True
                break
            else:
                self.can_aim = False
                self.is_grounded = False
    
    
    def update(self, events, delta_time, camera_position, platforms):
        self.movement(delta_time, platforms)
        if self.can_aim or self.multi_sling:
            self.aim(events, camera_position)
        self.draw(camera_position)