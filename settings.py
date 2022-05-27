# Imports
import pygame
from utilities import *


# Window settings
GRID_SIZE = 64
WIDTH = 16 * GRID_SIZE
HEIGHT = 9 * GRID_SIZE
TITLE = "My Awesome Game"
FPS = 60


# Make the game window
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# Limit allowed events
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])


# Define colors
SKY_BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

    
# Fonts
FONT_XL = pygame.font.Font('assets/fonts/Dinomouse-Regular.otf', 96)
FONT_LG = pygame.font.Font(None, 64)
FONT_MD = pygame.font.Font(None, 32)
FONT_SM = pygame.font.Font(None, 24)


# Load images
grass_dirt_img = load_image('assets/images/tiles/grass_dirt.png')
block_img = load_image('assets/images/tiles/block.png')


hero_imgs_idle_rt = [load_image('assets/images/characters/player_idle.png')]
hero_imgs_walk_rt = [load_image('assets/images/characters/player_walk1.png'),
                     load_image('assets/images/characters/player_walk2.png')]
hero_imgs_jump_rt = [load_image('assets/images/characters/player_jump.png')]

hero_imgs_idle_lt = [flip_image_x(img) for img in hero_imgs_idle_rt]
hero_imgs_walk_lt = [flip_image_x(img) for img in hero_imgs_walk_rt]
hero_imgs_jump_lt = [flip_image_x(img) for img in hero_imgs_jump_rt]


flag_img = load_image('assets/images/tiles/flag.png')
flagpole_img = load_image('assets/images/tiles/flagpole.png')
gem_img = load_image('assets/images/items/gem.png')
spikeball_imgs = [load_image('assets/images/characters/spikeBall1.png'),
                 load_image('assets/images/characters/spikeBall2.png')]
cloud_img = load_image('assets/images/characters/cloud.png')
spikeman_imgs_rt = [load_image('assets/images/characters/spikeMan_walk1.png'),
                    load_image('assets/images/characters/spikeMan_walk2.png')]
spikeman_imgs_lt = [flip_image_x(img) for img in spikeman_imgs_rt]


# Load sounds


# Load music


# Levels
levels = ['assets/levels/world-1.json',
          'assets/levels/world-2.json',
          'assets/levels/world-3.json']


# Other constants and settings
START = 0
PLAYING = 1
PAUSED = 2
WIN = 3
LOSE = 4
