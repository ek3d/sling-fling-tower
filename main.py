import pygame
import random
import asyncio

from utils import *
from player import *
from powerups import *
from platforms import *

import sys
import platform
if sys.platform == "emscripten":
    platform.window.canvas.style.imageRendering = "pixelated"

# pygame.mixer.init(44100, -16, 2, 64)
pygame.init()


# - - - - - - - - - - - - - - - - - SETUP - - - - - - - - - - - - - - - - - #
window = pygame.display.set_mode((240, 320))
window_middle = (window.get_width() / 2, window.get_height() / 2)
pygame.display.set_caption('Sling Fling Tower')
clock = pygame.time.Clock()
FPS = 120

volume = 1
pygame.mixer.set_num_channels(8)

background_music = pygame.mixer.Channel(5)
music = pygame.mixer.Sound('assets/audio/music/song.ogg')
music.set_volume(volume)
background_music.play(music, -1)


# - - - - - - - - - - - - - - - - - GAME - - - - - - - - - - - - - - - - - #
class Menu:
    def __init__(self):
        self.play_button = Button(window, window_middle, 'Play', 18, LIGHT_GREEN)
        self.settings_button = Button(window, (window_middle[0], window_middle[1] + 45), 'Settings', 18, LIGHT_GREEN)
        
        if not background_music.get_busy():
            background_music.play(music, -1)
    
    
    def update(self, events, delta_time):
        window.fill(BLACK)
        
        # Menu Logic Here
        draw_text(window, (window_middle[0], window_middle[1] - 45), 'Sling Fling', 24, WARM_YELLOW)
        draw_text(window, (window_middle[0], window_middle[1] - 30), 'Tower', 24, WARM_YELLOW)
        
        self.play_button.draw()
        if self.play_button.check_click(events, volume):
            change_scene(GameClassic)
        
        self.settings_button.draw()
        if self.settings_button.check_click(events, volume):
            change_scene(Settings)


class Settings:
    def __init__(self):
        self.menu_button = Button(window, (window_middle[0], window_middle[1] + 100), 'Menu', 18, LIGHT_GREEN)
        
        self.volume_slider = Slider(window, (window_middle[0], window_middle[1] - 50), WHITE, GRAY, (100, 10), 1)
        self.fps_slider = Slider(window, window_middle, WHITE, GRAY, (100, 10), 1)
    
    
    def update(self, events, delta_time):
        global volume
        global FPS
        window.fill(BLACK)
        
        # Menu Logic Here
        draw_text(window, (window_middle[0], window_middle[1] - 100), 'Settings', 24, WARM_YELLOW)
        
        self.menu_button.draw()
        if self.menu_button.check_click(events, volume):
            change_scene(Menu)
        
        self.volume_slider.update(events)
        self.volume_slider.draw()
        volume = self.volume_slider.slider_percentage
        background_music.set_volume(volume)
        draw_text(window, (window_middle[0], window_middle[1] - 25), 'Volume: ' + str(volume), 24)
        
        self.fps_slider.update(events)
        self.fps_slider.draw()
        FPS = max(int(self.fps_slider.slider_percentage * 121), 1)
        if FPS == 121:
            draw_text(window, (window_middle[0], window_middle[1] + 25), 'FPS: Unlimited', 24)
        else:
            draw_text(window, (window_middle[0], window_middle[1] + 25), 'FPS: ' + str(FPS), 24)


class GameOver:
    def __init__(self):
        self.menu_button = Button(window, (window_middle[0] - 45, window_middle[1]), 'Menu', 18, RED)
        self.play_button = Button(window, (window_middle[0] + 45, window_middle[1]), 'Play Again', 18, RED)
        background_music.stop()
        play_sound('assets/audio/sfx/game_over.ogg', volume)
    
    
    def update(self, events, delta_time):
        window.fill(BLACK)
        
        # Menu Logic Here
        draw_text(window, (window_middle[0], window_middle[1] - 45), 'Game', 24, RED)
        draw_text(window, (window_middle[0], window_middle[1] - 30), 'Over', 24, RED)
        
        self.menu_button.draw()
        if self.menu_button.check_click(events, volume):
            change_scene(Menu)
        
        self.play_button.draw()
        if self.play_button.check_click(events, volume):
            change_scene(GameClassic)


class GameClassic:
    def __init__(self):
        self.player = Player(window, list(window_middle), volume)
        
        self.platforms = [
            Platform(window, (-5, window_middle[1] - 200), (10, 400)),
            Platform(window, (window.get_width() - 5, window_middle[1] - 200), (10, 400)),
            Platform(window, (window_middle[0] - 36, window_middle[1])),
        ]
        self.highest_platform_y = 0
        
        self.powerups = []
        
        self.generate_platforms(100, 10, -100)
        
        self.camera_position = [0, 0]
        
        if not background_music.get_busy():
            background_music.play(music, -1)
    
    
    def update_camera(self):
        target_y = self.player.position[1] - window_middle[1] + self.player.player_rect.height / 2
        smoothing_factor = 0.075
        self.camera_position[1] += int((target_y - self.camera_position[1]) * smoothing_factor)
        
        self.platforms[0].rect.top = self.camera_position[1]
        self.platforms[1].rect.top = self.camera_position[1]
    
    
    def generate_platforms(self, interval_height, iterations, offset):
        for i in range(iterations):
            position = (window_middle[0] - random.randint(4, 27) * 5, window_middle[1] + offset - interval_height * i)
            powerup_position = (position[0] + 36, position[1] - 20)
            random_platform = Platform(window, position)
            self.platforms.append(random_platform)
            
            random_number = random.randint(0, 20)
            if random_number == 0:
                self.powerups.append(Rocket(window, self.player, powerup_position, self.powerups, volume))
            elif random_number == 1:
                self.powerups.append(MultiSling(window, self.player, powerup_position, self.powerups, volume))
            elif random_number == 2:
                self.powerups.append(Feather(window, self.player, powerup_position, self.powerups, volume))
            
            if i == iterations - 1:
                self.highest_platform_y = position[1]
    
    
    def check_platforms(self):
        if self.player.position[1] <= self.highest_platform_y:
            self.generate_platforms(100, 10, self.highest_platform_y - 260)
    
    
    def update(self, events, delta_time):
        window.fill(BLACK)
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                pass
        
        # Game Logic Here
        self.check_platforms()
        self.update_camera()
        self.player.update(events, delta_time, self.camera_position, self.platforms)
        
        for platform in self.platforms:
            platform.draw(self.camera_position)
        
        for powerup in self.powerups:
            powerup.update(self.camera_position)
        
        if self.player.position[1] >= 500:
            change_scene(GameOver)
        
        draw_text(window, (10, 10), 'Altitude: ' + str(-(int(self.player.position[1]) - window_middle[1] - self.player.player_rect.height)) + 'm', 24, center = False)


current_scene = Menu()


def change_scene(game_state):
    global current_scene
    current_scene = game_state()


async def main():
    global run
    run = True
    while run:
        if FPS == 121:
            delta_time = min(clock.tick() / 1000, 1 / FPS)
        else:
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
