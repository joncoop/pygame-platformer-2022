# Imports
import pygame
from utilities import *

pygame.init()


# Helper functions to simplify pygame syntax
def load_image(path):
    return pygame.image.load(path).convert_alpha()

def flip_image_x(image):
    return pygame.transform.flip(image, True, False)

def flip_image_y(image):
    return pygame.transform.flip(image, False, True)

def load_font(path, size):
    return pygame.font.Font(path, size)

def load_sound(path, volume=1.0):
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

def play_music(track, volume=1.0, loops=-1):
    pygame.mixer.music.load(track)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops)    

def pause_music():
    pygame.mixer.music.pause()

def unpause_music():
    pygame.mixer.music.unpause()

def restart_music():
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()


# Helper function to draw a grid to help with level design
def draw_grid(surface, width, height, grid_size, offset_x=0, offset_y=0, color = (125, 125, 125)):
    font = pygame.font.Font(None, 16)
    
    for x in range(0, width + grid_size, grid_size):
        adj_x = x - offset_x % grid_size
        pygame.draw.line(surface, color, [adj_x, 0], [adj_x, height], 1)

    for y in range(0, height + grid_size, grid_size):
        adj_y = y - offset_y % grid_size
        pygame.draw.line(surface, color, [0, adj_y], [width, adj_y], 1)

    for x in range(0, width + grid_size, grid_size):
        for y in range(0, height + grid_size, grid_size):
            adj_x = x - offset_x % grid_size + 4
            adj_y = y - offset_y % grid_size + 4
            disp_x = x // grid_size + offset_x // grid_size
            disp_y = y // grid_size + offset_y // grid_size
            
            point = '(' + str(disp_x) + ',' + str(disp_y) + ')'
            text = font.render(point, True, color)
            surface.blit(text, [adj_x, adj_y])
