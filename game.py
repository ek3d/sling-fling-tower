import pygame
import random

from utils import *
from player import *
from powerups import *
from platforms import *

pygame.init()


# - - - - - - - - - - - - - - - - - SETUP - - - - - - - - - - - - - - - - - #
window = pygame.display.set_mode((240, 320), pygame.SCALED, vsync=1)
window_middle = (window.get_width() / 2, window.get_height() / 2)
pygame.display.set_caption('Sling Fling Tower')
clock = pygame.time.Clock()
FPS = 60

volume = 1
pygame.mixer.set_num_channels(8)

background_music = pygame.mixer.Channel(5)
music = pygame.mixer.Sound('assets/audio/music/song.ogg')
music.set_volume(volume)
background_music.play(music, -1)

highest_altitude = 0
time = 1800
player_color = WHITE


# - - - - - - - - - - - - - - - - - GAME - - - - - - - - - - - - - - - - - #
class Menu:
    def __init__(self):
        self.play_button = Button(window, (window_middle[0], window_middle[1] - 45), 'Play', 18)
        self.player_color_button = Button(window, window_middle, 'Color', 18)
        self.settings_button = Button(window, (window_middle[0], window_middle[1] + 45), 'Settings', 18)
        
        if not background_music.get_busy():
            background_music.play(music, -1)
    
    
    def update(self, events, delta_time):
        window.fill(BLACK)
        
        draw_text(window, (window_middle[0], window_middle[1] - 75), 'Sling Fling Tower', 24, WARM_YELLOW)
        
        self.play_button.draw()
        if self.play_button.check_click(events, volume):
            change_scene(GamemodeSelect)
        
        self.player_color_button.draw()
        if self.player_color_button.check_click(events, volume):
            change_scene(PlayerColorSelect)
        
        self.settings_button.draw()
        if self.settings_button.check_click(events, volume):
            change_scene(Settings)


class Settings:
    def __init__(self):
        self.menu_button = Button(window, (window_middle[0], window_middle[1] + 100), 'Menu', 18, LIGHT_GREEN)
        
        self.volume_slider = Slider(window, (window_middle[0], window_middle[1] - 50), WHITE, GRAY, (100, 10), 1)
        self.fps_slider = Slider(window, window_middle, WHITE, GRAY, (100, 10), 0.5)
    
    
    def update(self, events, delta_time):
        global volume
        global FPS
        window.fill(BLACK)
        
        draw_text(window, (window_middle[0], window_middle[1] - 100), 'Settings', 24, WARM_YELLOW)
        
        self.menu_button.draw()
        if self.menu_button.check_click(events, volume):
            change_scene(Menu)
        
        self.volume_slider.update(events)
        self.volume_slider.draw()
        volume = self.volume_slider.slider_percentage
        music.set_volume(volume)
        draw_text(window, (window_middle[0], window_middle[1] - 25), 'Volume: ' + str(volume), 24)
        
        self.fps_slider.update(events)
        self.fps_slider.draw()
        FPS = max(round(self.fps_slider.slider_percentage * 120), 1)
        draw_text(window, (window_middle[0], window_middle[1] + 25), 'FPS: ' + str(FPS), 24)


class GamemodeSelect:
    def __init__(self):
        self.play_button = Button(window, (window_middle[0], window_middle[1] + 100), 'Play', 18, LIGHT_GREEN, toggle = False)
        self.classic_button = Button(window, (window_middle[0] - 60, window_middle[1] - 50), 'Classic', 18, LIGHT_GREEN, toggle = True)
        self.time_trial_button = Button(window, (window_middle[0] - 60, window_middle[1]), 'Time Trial', 18, LIGHT_GREEN, toggle = True)
        
        self.time_slider = Slider(window, (window_middle[0] + 50, window_middle[1] - 5), WHITE, GRAY, (100, 10), 1)
        
        self.error = False
    
    
    def update(self, events, delta_time):
        global time
        window.fill(BLACK)
        
        draw_text(window, (window_middle[0], window_middle[1] - 100), 'Select Gamemode', 24, WARM_YELLOW)
        
        self.play_button.draw()
        if self.play_button.check_click(events, volume):
            if self.classic_button.toggled:
                change_scene(GameClassic)
            elif self.time_trial_button.toggled:
                change_scene(GameTimeTrial)
            else:
                self.error = True
        
        if self.error:
            draw_text(window, (window_middle[0], window_middle[1] + 75), 'No gamemode selected!', 24, WARM_YELLOW)
        
        self.classic_button.draw()
        if self.classic_button.check_click(events, volume):
            self.time_trial_button.toggled = False
        
        self.time_trial_button.draw()
        if self.time_trial_button.check_click(events, volume):
            self.classic_button.toggled = False
        
        if self.time_trial_button.toggled:
            self.time_slider.update(events)
            self.time_slider.draw()
            time = max(self.time_slider.slider_percentage * 1800, 60)
            print(time)
            draw_text(window, (window_middle[0] + 50, window_middle[1] + 10), 'Time: ' + str(round(time / FPS, 1)) + ' Seconds', 18)


class PlayerColorSelect:
    def __init__(self):
        self.white_button = Button(window, (window_middle[0] - 60, window_middle[1] + 100), 'White', 18, WHITE, GRAY)
        self.red_button = Button(window, (window_middle[0] - 60, window_middle[1] + 60), 'Red', 18, RED, GRAY)
        self.yellow_button = Button(window, (window_middle[0] - 60, window_middle[1] + 20), 'Yellow', 18, WARM_YELLOW, GRAY)
        self.green_button = Button(window, (window_middle[0] - 60, window_middle[1] - 20), 'Green', 18, LIGHT_GREEN, GRAY)
        self.blue_button = Button(window, (window_middle[0] - 60, window_middle[1] - 60), 'Blue', 18, LIGHT_BLUE, GRAY)
        self.pink_button = Button(window, (window_middle[0] - 60, window_middle[1] - 100), 'Pink', 18, PINK, GRAY)
        
        self.back_button = Button(window, (window_middle[0] + 45, window_middle[1] + 60), 'Back', 18)
        
        self.player_rect = pygame.Rect((0, 0), (16, 24))
        self.player_rect.center = (window_middle[0] + 45, window_middle[1])
        self.left_eye_rect = pygame.Rect((0, 0), (2, 6))
        self.left_eye_rect.center = (window_middle[0] + 43, window_middle[1] - 3)
        self.right_eye_rect = pygame.Rect((0, 0), (2, 6))
        self.right_eye_rect.center = (window_middle[0] + 47, window_middle[1] - 3)
    
    
    def update(self, events, delta_time):
        global player_color
        window.fill(BLACK)
        
        draw_text(window, (window_middle[0] + 45, window_middle[1] - 50), 'Player Color', 24, WARM_YELLOW)
        
        self.back_button.draw()
        if self.back_button.check_click(events, volume):
            change_scene(Menu)
        
        self.white_button.draw()
        if self.white_button.check_click(events, volume):
            player_color = WHITE
        
        self.red_button.draw()
        if self.red_button.check_click(events, volume):
            player_color = RED
        
        self.yellow_button.draw()
        if self.yellow_button.check_click(events, volume):
            player_color = WARM_YELLOW
        
        self.green_button.draw()
        if self.green_button.check_click(events, volume):
            player_color = LIGHT_GREEN
        
        self.blue_button.draw()
        if self.blue_button.check_click(events, volume):
            player_color = LIGHT_BLUE
        
        self.pink_button.draw()
        if self.pink_button.check_click(events, volume):
            player_color = PINK
        
        pygame.draw.rect(window, player_color, self.player_rect, border_radius=3)
        pygame.draw.rect(window, BLACK, self.left_eye_rect)
        pygame.draw.rect(window, BLACK, self.right_eye_rect)


class GameOver:
    def __init__(self):
        self.menu_button = Button(window, (window_middle[0] - 45, window_middle[1]), 'Menu', 18, RED)
        self.play_button = Button(window, (window_middle[0] + 45, window_middle[1]), 'Play Again', 18, RED)
        background_music.stop()
        play_sound('assets/audio/sfx/game_over.ogg', volume)
    
    
    def update(self, events, delta_time):
        global highest_altitude
        window.fill(BLACK)
        
        draw_text(window, (window_middle[0], window_middle[1] - 45), 'Game', 24, RED)
        draw_text(window, (window_middle[0], window_middle[1] - 30), 'Over', 24, RED)
        
        self.menu_button.draw()
        if self.menu_button.check_click(events, volume):
            change_scene(Menu)
            highest_altitude = 0
        
        self.play_button.draw()
        if self.play_button.check_click(events, volume):
            change_scene(GameClassic)
            highest_altitude = 0
        
        draw_text(window, (window_middle[0], window_middle[1] + 45), 'Highest Altitude: ' + str(highest_altitude) + 'm', 24, LIGHT_GREEN)


class Game:
    def __init__(self):
        self.player = Player(window, list(window_middle), volume, player_color)
        
        self.platforms = [
            Platform(window, (-5, window_middle[1] - 200), (10, 400), False),
            Platform(window, (window.get_width() - 5, window_middle[1] - 200), (10, 400), False),
            Platform(window, (window_middle[0] - 36, window_middle[1])),
        ]
        self.highest_platform_y = 0
        
        self.powerups = []
        
        self.generate_platforms(100, 10, -100)
        
        self.camera_position = [0, 0]
        
        if not background_music.get_busy():
            background_music.play(music, -1)
    
    
    def update_camera(self):
        target_y = self.player.position[1] - window_middle[1] + self.player.player_rect.height / 2 - 20
        smoothing_factor = 0.075
        self.camera_position[1] += int((target_y - self.camera_position[1]) * smoothing_factor)
        
        self.platforms[0].rect.top = self.camera_position[1]
        self.platforms[1].rect.top = self.camera_position[1]
    
    
    def generate_platforms(self, interval_height, iterations, offset):
        for i in range(iterations):
            position = (random.randint(4, 38) * 4, window_middle[1] + offset - interval_height * i)
            powerup_position = (position[0] + 36, position[1] - 20)
            
            random_platform = random.randint(0, 20)
            if random_platform == 0:
                self.platforms.append(MovingPlatform(window, position))
            elif random_platform == 1:
                self.platforms.append(IcePlatform(window, position))
            elif random_platform == 2:
                self.platforms.append(CrackedPlatform(window, position))
            else:
                self.platforms.append(Platform(window, position))
            
            random_powerup = random.randint(0, 20)
            if random_powerup == 0:
                self.powerups.append(Rocket(window, self.player, powerup_position, self.powerups, volume))
            elif random_powerup == 1:
                self.powerups.append(MultiSling(window, self.player, powerup_position, self.powerups, volume))
            elif random_powerup == 2:
                self.powerups.append(Feather(window, self.player, powerup_position, self.powerups, volume))
            
            if i == iterations - 1:
                self.highest_platform_y = position[1]
    
    
    def check_platforms(self):
        if self.player.position[1] <= self.highest_platform_y + 300:
            self.generate_platforms(100, 10, self.highest_platform_y - 260)
    
    
    def update_game(self, events, delta_time):
        global highest_altitude
        # Game Logic Here
        self.check_platforms()
        self.update_camera()
        self.player.update(events, delta_time, self.camera_position, self.platforms)
        
        for platform in self.platforms:
            platform.update(self.camera_position, delta_time)
        
        for powerup in self.powerups:
            powerup.update(self.camera_position)
        
        if self.player.position[1] >= 500:
            change_scene(GameOver)
        
        altitude = -(int(self.player.position[1]) - window_middle[1] - self.player.player_rect.height)
        if altitude > highest_altitude:
            highest_altitude = altitude
        draw_text(window, (10, 10), 'Altitude: ' + str(altitude) + 'm', 24, WARM_YELLOW, center = False)
        draw_text(window, (10, 30), 'FPS: ' + str(round(clock.get_fps())), 18, center = False)
    
    def update(self, events, delta_time):
        window.fill(BLACK)
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                pass
        
        self.update_game(events, delta_time)


class GameClassic(Game):
    def __init__(self):
        super().__init__()
    
    
    def update(self, events, delta_time):
        window.fill(BLACK)
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                pass
        
        self.update_game(events, delta_time)


class GameTimeTrial(Game):
    def __init__(self):
        super().__init__()
        
        self.timer = Timer(time)
    
    
    def update(self, events, delta_time):
        window.fill(BLACK)
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                pass
        
        self.update_game(events, delta_time)
        
        draw_text(window, (10, 40), 'Time: ' + str(round((time - self.timer.current_time) / FPS, 1)), 18, center = False)
        
        if self.timer.update():
            change_scene(GameOver)


current_scene = Menu()


def change_scene(game_state):
    global current_scene
    current_scene = game_state()


def main():
    run = True
    while run:
        delta_time = clock.tick(FPS) / 1000
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
        
        current_scene.update(events, delta_time)
        
        pygame.display.update()

main()
