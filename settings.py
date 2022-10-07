# Imports
import pygame
from utilities import *


# Window settings
GRID_SIZE = 64
WIDTH = 16 * GRID_SIZE
HEIGHT = 9 * GRID_SIZE
TITLE = "My Awesome Game"
FPS = 60


# Define colors
SKY_BLUE = (135, 200, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (93, 67, 62)
    
# Fonts
PRIMARY_FONT = 'assets/fonts/Dinomouse-Regular.otf'
SECONDARY_FONT = 'assets/fonts/Dinomouse-Regular.otf'


# Images
##''' background '''
##BACKGROUND_IMG = 'assets/images/backgrounds/final_day.png'

''' tiles '''
GRASS_IMG = 'assets/images/tiles/grass_dirt.png'
BLOCK_IMG = 'assets/images/tiles/block.png'

''' hero '''
HERO_IMGS_IDLE_RT = ['assets/images/characters/player_idle.png']
HERO_IMGS_WALK_RT = ['assets/images/characters/player_walk1.png',
                     'assets/images/characters/player_walk2.png']
HERO_IMGS_JUMP_RT = ['assets/images/characters/player_jump.png']

''' items '''
GEM_IMG = 'assets/images/items/diamond.png'
HEART_IMG = 'assets/images/items/heart.png'
KEY_IMG = 'assets/images/items/key.png'

''' doors '''
DOORTOP_IMG = 'assets/images/tiles/door_top.png'
DOOR_IMG = 'assets/images/tiles/door.png'
LOCKED_DOORTOP_IMG = 'assets/images/tiles/locked_door_top.png'
LOCKED_DOOR_IMG = 'assets/images/tiles/locked_door.png'

'sign'
SIGN_IMG = 'assets/images/tiles/sign.png'

''' goals '''
FLAG_IMG = 'assets/images/tiles/flag.png'
FLAGPOLE_IMG = 'assets/images/tiles/flagpole.png'

''' enemies '''
SPIKEBALL_IMGS = ['assets/images/characters/spikeball1.png',
                 'assets/images/characters/spikeball2.png']

SPIKEMAN_IMGS = ['assets/images/characters/spikeman_walk1.png',
                'assets/images/characters/spikeman_walk2.png']

CLOUD_IMG = 'assets/images/characters/cloud.png'

''' npcs '''
ROBOT_IMGS_WALK_RT = ['assets/images/characters/robot_walk1.png',
                      'assets/images/characters/robot_walk1.png',
                       'assets/images/characters/robot_walk1.png',
                       'assets/images/characters/robot_walk1.png',
                       'assets/images/characters/robot_walk1.png',
                       'assets/images/characters/robot_walk1.png']
ROBOT_IMGS_TALK = ['assets/images/characters/robot_talk.png']


# Sounds
JUMP_SND = 'assets/sounds/jump.wav'
GEM_SND = 'assets/sounds/collect_point.wav'
HURT_SND = 'assets/sounds/hurt.ogg'
LEVEL_UP_SND = 'assets/sounds/level_up.wav'
POWERUP_SND = 'assets/sounds/pickup_item.wav'

# Music
TITLE_MUSIC = 'assets/music/calm_happy.ogg'
PLAYING_MUSIC = 'assets/music/cooking_mania.wav'


# Levels
LEVELS = ['assets/levels/world-1.json',
          'assets/levels/world-2.json',
          'assets/levels/world-3.json',
          'assets/levels/world-4.json']

# Controls
CONTROLS = {'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'jump': pygame.K_SPACE,
            'interact': pygame.K_UP,
            'continue': pygame.K_DOWN}


# Physics settings
##GRAVITY = 1.0
##TERMINAL_VELOCITY = 32


# Other settings
HERO_SPEED = 5
HERO_JUMP_POWER = 22

SPIKEBALL_SPEED = 2
SPIKEMAN_SPEED = 2
CLOUD_SPEED = 2

NPC_SPEED = 1

# Scoring
POINTS_PER_LEVEL = 100
POINTS_PER_COIN = 10
POINTS_PER_POWERUP = 25
