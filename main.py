import random
import asyncio

import pygame
pygame.init()


# - - - - - - - - - - - - - - - - - SETUP - - - - - - - - - - - - - - - - - #
window = pygame.display.set_mode((240, 320))
window_center = (window.get_width() / 2, window.get_height() / 2)
pygame.display.set_caption('Sling Fling Tower')
clock = pygame.time.Clock()
FPS = 75




# - - - - - - - - - - - - - - - - - UTILS - - - - - - - - - - - - - - - - - #
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIGHT_RED = (255, 128, 128)
GREEN = (0, 255, 0)
LIGHT_GREEN = (128, 255, 128)
BLUE = (0, 0, 255)
LIGHT_BLUE = (128, 128, 255)
YELLOW = (255, 255, 0)
WARM_YELLOW = (255, 200, 0)
PINK = (255, 0, 255)
PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)


def draw_text(position, text, font_size, color = WHITE, anti_alias = False, center = True):
    font = pygame.font.Font(None, font_size)
    font_rendered = font.render(text, anti_alias, color)
    if center:
        rect = font_rendered.get_rect(center = position)
        window.blit(font_rendered, rect)
    else:
        window.blit(font_rendered, position)


class Timer:
    def __init__(self, time, step = 1, repeats = False, overflow = False):
        self.time = time
        self.step = step
        
        self.repeats = repeats
        self.overflow = overflow
        
        self.current_time = 0
    
    
    def update(self):
        self.current_time += self.step
        if self.current_time == self.time and not self.overflow:
            if self.repeats:
                self.current_time = 0
            return True
        if self.current_time >= self.time and self.overflow:
            if self.repeats:
                self.current_time = 0
            return True
    
    
    def check(self):
        if self.current_time == self.time and not self.overflow:
            return True
        if self.current_time >= self.time and self.overflow:
            return True


class Button:
    def __init__(self, position, text, font_size, text_color, color = WHITE):
        self.position = position
        
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        
        self.button_rect = pygame.Rect((0, 0), (64, 32))
        self.button_rect.center = position
        
        self.original_color = color
        self.highlight_color = (color[0] - 100, color[1] - 100, color[2] - 100)
        self.color = self.original_color
    
    
    def draw(self):
        # window.blit(self.current_image, self.image_rect)
        pygame.draw.rect(window, self.color, self.button_rect, border_radius = 100)
        draw_text((self.position[0], self.position[1]), self.text, self.font_size, self.text_color)
    
    
    def check_click(self, events):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.color = self.highlight_color
                    return False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    return True
        else:
            self.color = self.original_color
            return False




# - - - - - - - - - - - - - - - - - PLAYER - - - - - - - - - - - - - - - - - #
class Player:
    def __init__(self, position):
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.gravity = 400
        
        self.is_grounded = False
        
        self.player_rect = pygame.Rect((0, 0), (16, 24))
        self.player_rect.center = self.position
        
        self.aiming = False
        self.can_aim = True
        self.multi_fling = False
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
                self.aiming = False
                self.velocity = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(self.position) + pygame.Vector2(camera_position)
        
        if self.aiming:
            aim_start = pygame.Vector2(self.position) - camera_position
            aim_end = pygame.mouse.get_pos()
            pygame.draw.line(window, WHITE, aim_start, aim_end, 6)
            pygame.draw.circle(window, WHITE, aim_end, 6)
            pygame.draw.circle(window, GRAY, aim_end, 4)
    
    
    def draw(self, camera_position):
        self.left_eye_rect.center = (self.position[0] - 2, self.position[1] - 3)
        self.left_eye_rect.move_ip(-camera_position[0], -camera_position[1])
        self.right_eye_rect.center = (self.position[0] + 2, self.position[1] - 3)
        self.right_eye_rect.move_ip(-camera_position[0], -camera_position[1])
        
        # Idle
        draw_player_rect = self.player_rect.move(-camera_position[0], -camera_position[1])
        pygame.draw.rect(window, WHITE, draw_player_rect, border_radius = 3)
        pygame.draw.rect(window, BLACK, self.left_eye_rect)
        pygame.draw.rect(window, BLACK, self.right_eye_rect)
    
    
    def movement(self, delta_time, platforms):
        if not self.is_grounded:
            self.velocity.y += self.gravity * delta_time
        
        self.position[0] += self.velocity.x * self.multiplier * delta_time
        self.player_rect.centerx = self.position[0]
        
        for platform in platforms:
            if self.player_rect.colliderect(platform):
                if self.velocity.x < 0:
                    self.position[0] = platform.right + (self.player_rect.width / 2)
                elif self.velocity.x > 0:
                    self.position[0] = platform.left - (self.player_rect.width / 2)
                self.velocity.x *= -0.75
                self.player_rect.centerx = self.position[0]
                break
        
        self.position[1] += self.velocity.y * self.multiplier * delta_time
        self.player_rect.centery = self.position[1]
        
        for platform in platforms:
            if self.player_rect.colliderect(platform):
                if self.velocity.y > 0:
                    self.position[1] = platform.top - (self.player_rect.height / 2)
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
        if self.can_aim or self.multi_fling:
            self.aim(events, camera_position)
        self.draw(camera_position)




# - - - - - - - - - - - - - - - - - POWERUPS - - - - - - - - - - - - - - - - - #
class Rocket:
    def __init__(self, player, position):
        self.player = player
        self.rect = pygame.Rect((0, 0), (12, 12))
        self.rect.center = position
    
    
    def draw(self, camera_position):
        draw_rect = self.rect.move(-camera_position[0], -camera_position[1])
        pygame.draw.rect(window, RED, draw_rect, border_radius = 20)
    
    
    def update(self, camera_position):
        self.draw(camera_position)
        
        if self.rect.colliderect(self.player.player_rect):
            self.player.velocity.y = -300


class MultiFling:
    def __init__(self, player, position):
        self.player = player
        self.rect = pygame.Rect((0, 0), (12, 12))
        self.rect.center = position
        
        self.activated = False
        self.timer = Timer(300)
    
    
    def draw(self, camera_position):
        draw_rect = self.rect.move(-camera_position[0], -camera_position[1])
        pygame.draw.rect(window, GREEN, draw_rect, border_radius = 20)
        
        if self.activated:
            draw_text((window_center[0], window.get_height() - 30), 'Multi-Fling', 24, GREEN, center = True)
    
    
    def update(self, camera_position):
        self.draw(camera_position)
        
        if self.rect.colliderect(self.player.player_rect):
            self.activated = True
        
        if self.activated:
            if self.timer.update():
                self.activated = False
                self.player.multi_fling = False
                return
            self.player.multi_fling = True


class Feather:
    def __init__(self, player, position):
        self.player = player
        self.rect = pygame.Rect((0, 0), (12, 12))
        self.rect.center = position
        
        self.activated = False
        self.timer = Timer(300)
    
    
    def draw(self, camera_position):
        draw_rect = self.rect.move(-camera_position[0], -camera_position[1])
        pygame.draw.rect(window, PURPLE, draw_rect, border_radius = 20)
        
        if self.activated:
            draw_text((window_center[0] - 100, window.get_height() - 30), 'Feather', 24, PURPLE, center = False)
    
    
    def update(self, camera_position):
        self.draw(camera_position)
        
        if self.rect.colliderect(self.player.player_rect):
            self.activated = True
        
        if self.activated:
            if self.timer.update():
                self.activated = False
                self.player.gravity = 400
                return
            self.player.gravity = 200




# - - - - - - - - - - - - - - - - - GAME - - - - - - - - - - - - - - - - - #
class GameState:
    GAME_RUNNING = 0
    MENU = 1


class Menu():
    def __init__(self):
        self.play_button = Button(window_center, 'Play', 18, LIGHT_GREEN)
    
    
    def update(self, events, delta_time):
        window.fill(BLACK)
        
        # Menu Logic Here
        draw_text((window_center[0], window_center[1] - 45), 'Sling Fling', 24, WARM_YELLOW)
        draw_text((window_center[0], window_center[1] - 30), 'Tower', 24, WARM_YELLOW)
        
        self.play_button.draw()
        if self.play_button.check_click(events):
            change_scene(GameState.GAME_RUNNING)


class Game():
    def __init__(self):
        self.player = Player(list(window_center))
        
        self.platforms = [
            pygame.Rect((-5, window_center[1] - 200), (10, 400)),
            pygame.Rect((window.get_width() - 5, window_center[1] - 200), (10, 400)),
            pygame.Rect((window_center[0] - 36, window_center[1] + 40), (72, 10)),
        ]
        self.powerups = []
        
        self.generate_platforms(100, 100)
        
        self.camera_position = [0, 0]
    
    
    def update_camera(self):
        self.camera_position[1] = self.player.position[1] - window_center[1] + self.player.player_rect.height / 2
        
        self.platforms[0].top = self.player.position[1] - window_center[1]
        self.platforms[1].top = self.player.position[1] - window_center[1]
    
    
    def generate_platforms(self, interval_height, iterations):
        for i in range(iterations):
            x_position = window_center[0] - random.randint(1, 33) * 5
            x_position_center = x_position + 36
            y_position = window_center[1] - 60 - interval_height * i
            random_platform = pygame.Rect((x_position, y_position), (72, 10))
            self.platforms.append(random_platform)
            
            random_number = random.randint(0, 20)
            if random_number == 0:
                self.powerups.append(Rocket(self.player, (x_position_center, y_position - 20)))
            elif random_number == 1:
                self.powerups.append(MultiFling(self.player, (x_position_center, y_position - 20)))
            elif random_number == 2:
                self.powerups.append(Feather(self.player, (x_position_center, y_position - 20)))
    
    
    def draw_platforms(self):
        for platform in self.platforms:
            draw_platform = platform.move(-self.camera_position[0], -self.camera_position[1])
            pygame.draw.rect(window, GRAY, draw_platform)
    
    
    def update(self, events, delta_time):
        window.fill(BLACK)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                pass
        
        # Game Logic Here
        self.update_camera()
        self.draw_platforms()
        self.player.update(events, delta_time, self.camera_position, self.platforms)
        
        if self.player.position[1] >= 500:
            change_scene(GameState.MENU)
        
        draw_text((10, 10), 'Altitude: ' + str(-(int(self.player.position[1]) - window_center[1] - self.player.player_rect.height)), 24, center = False)
        
        for powerup in self.powerups:
            powerup.update(self.camera_position)


current_scene = Menu()


def change_scene(game_state):
    global current_scene
    if game_state == GameState.MENU:
        current_scene = Menu()
    elif game_state == GameState.GAME_RUNNING:
        current_scene = Game()


async def main():
    global run
    run = True
    while run:
        delta_time = min(clock.tick(FPS) / 1000, 1 / FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        
        current_scene.update(events, delta_time)
        
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())