import pygame


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
BROWN = (191, 104, 67)


def draw_text(window, position, text, font_size, color = WHITE, anti_alias = False, center = True):
    font = pygame.font.Font(None, font_size)
    font_rendered = font.render(text, anti_alias, color)
    if center:
        rect = font_rendered.get_rect(center = position)
        window.blit(font_rendered, rect)
    else:
        window.blit(font_rendered, position)


def sign(number):
    return -1 if number < 0 else (1 if number > 0 else 0)


def play_sound(path, volume, loops = 0):
    music = pygame.mixer.Sound(path)
    music.set_volume(volume)
    music.play(loops)
    return music


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
    def __init__(self, window, position, text, font_size, text_color = BLACK, color = WHITE, toggle = False):
        self.window = window
        self.position = position
        
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        
        self.button_rect = pygame.Rect((0, 0), (64, 32))
        self.button_rect.center = position
        
        self.original_color = color
        self.highlight_color = (color[0] - 100, color[1] - 100, color[2] - 100)
        self.color = self.original_color
        
        self.toggle = toggle
        self.toggled = False
    
    
    def draw(self):
        if self.toggled:
            pygame.draw.rect(self.window, self.highlight_color, self.button_rect, border_radius = 100)
        else:
            pygame.draw.rect(self.window, self.color, self.button_rect, border_radius = 100)
        draw_text(self.window, (self.position[0], self.position[1]), self.text, self.font_size, self.text_color)
    
    
    def check_click(self, events, volume):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.color = self.highlight_color
                    return False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.toggle:
                        self.toggled = not self.toggled
                    play_sound('assets/audio/sfx/button.ogg', volume * 0.5)
                    return True
        else:
            self.color = self.original_color
            return False


class Slider():
    def __init__(self, window, position, back_color, slider_color, size, default_slider_percentage):
        self.window = window
        
        self.position = position
        self.size = size
        self.slider_rect = pygame.Rect(self.position, self.size)
        self.slider_rect.center = self.position
        
        self.slider_percentage = default_slider_percentage
        
        self.holding = False
        
        self.back_color = back_color
        self.slider_color = slider_color
    
    
    def draw(self):
        pygame.draw.rect(self.window, self.back_color, self.slider_rect, border_radius = 25)
        pygame.draw.circle(self.window, self.slider_color, ((self.slider_percentage * self.size[0]) + self.slider_rect.topleft[0], self.position[1]), 10)
    
    
    def slider_update(self):
        mouse_positon = pygame.mouse.get_pos()
        self.slider_percentage = (mouse_positon[0] - self.slider_rect.topleft[0])/self.size[0]
        self.slider_percentage = pygame.math.clamp(self.slider_percentage, 0, 1)
    
    
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.slider_rect.collidepoint(pygame.mouse.get_pos()):
                    self.holding = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.holding = False
        
        if self.holding:
            self.slider_update()
