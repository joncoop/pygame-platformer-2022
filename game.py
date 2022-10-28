# Imports
import json
import pygame

from editor import *
from settings import *
from utilities import *
from entities import *
from overlays import *


pygame.mixer.pre_init() # Does this actually help? I can't hear a difference.
pygame.init()

# Constants (Should any of this move to settings?)
''' stages/scenes '''
START = 0
PLAYING = 1
PAUSE = 2
LEVEL_COMPLETE = 3
WIN = 4
LOSE = 5
EDIT = 6

''' layers (doesn't work yet) '''
BACKGROUND_LAYER = 0  # Decorative tiles that entities pass in front of
ACTIVE_LAYER = 1      # Contains entities that can interact
FOREGROUND_LAYER = 2  # Decorative tiles that entities pass behind

''' Change to test new levels '''
STARTING_LEVEL = 1

# Main game class 
class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.running = True
        self.mute = False

        self.load_assets()
        self.new_game()

        self.title_screen = TitleScreen(self)
        self.win_screen = WinScreen(self)
        self.lose_screen = LoseScreen(self)
        self.level_complete_screen = LevelCompleteScreen(self)
        self.pause_screen = PauseScreen(self)
        self.hud = HUD(self)

        # for editor, move to separate editor class
        self.grid = Grid(self)
        self.tile_index = 0 
        self.tile_images = [None, self.block_img, self.grass_dirt_img]

    def load_assets(self):
        #self.bg_img = Image(BACKGROUND_IMG)

        # make animated entities dict based?
        self.hero_imgs_idle_rt = [Image(img_path) for img_path in HERO_IMGS_IDLE_RT]
        self.hero_imgs_walk_rt = [Image(img_path) for img_path in HERO_IMGS_WALK_RT]
        self.hero_imgs_jump_rt = [Image(img_path) for img_path in HERO_IMGS_JUMP_RT]
        self.hero_imgs_idle_lt = [img.flip_x() for img in self.hero_imgs_idle_rt]
        self.hero_imgs_walk_lt = [img.flip_x() for img in self.hero_imgs_walk_rt]
        self.hero_imgs_jump_lt = [img.flip_x() for img in self.hero_imgs_jump_rt]

        self.grass_dirt_img = Image(GRASS_IMG)
        self.block_img = Image(BLOCK_IMG)

        self.gem_img = Image(GEM_IMG)
        self.heart_img = Image(HEART_IMG)
        self.key_img = Image(KEY_IMG)

        self.door_img = Image(DOOR_IMG)
        self.doortop_img = Image(DOORTOP_IMG)
        self.locked_door_img = Image(LOCKED_DOOR_IMG)
        self.locked_doortop_img = Image(LOCKED_DOORTOP_IMG)

        self.sign_img = Image(SIGN_IMG)

        self.flag_img = Image(FLAG_IMG)
        self.flagpole_img = Image(FLAGPOLE_IMG)

        self.spikeball_imgs = [Image(img_path) for img_path in SPIKEBALL_IMGS]
        self.spikeman_imgs_rt = [Image(img_path) for img_path in SPIKEMAN_IMGS]
        self.spikeman_imgs_lt = [img.flip_x() for img in self.spikeman_imgs_rt]
        self.cloud_img = Image(CLOUD_IMG)

        self.robot_imgs_walk_rt = [Image(img_path) for img_path in ROBOT_IMGS_WALK_RT]
        self.robot_imgs_walk_lt = [img.flip_x() for img in self.robot_imgs_walk_rt]
        self.robot_imgs_talk = [Image(img_path) for img_path in ROBOT_IMGS_TALK]
 
        self.audio = Audio()
        self.audio.add_music("title_music", TITLE_MUSIC)
        self.audio.add_music("main_theme", MAIN_THEME)

        self.audio.add_sound('jump', JUMP_SND)
        self.audio.add_sound('gem', GEM_SND)
        self.audio.add_sound('hurt', HURT_SND)
        self.audio.add_sound('powerup', POWERUP_SND)
        self.audio.add_sound('level_up', LEVEL_UP_SND)

        self.title_font = Font(PRIMARY_FONT, 80)
        self.subtitle_font = Font(SECONDARY_FONT, 64)
        self.default_font = Font(SECONDARY_FONT, 32)

    def new_game(self):
        # Make the hero here so it persists across levels
        self.hero = Hero(self, self.hero_imgs_idle_rt)
        
        # Go to first level
        self.stage = START
        self.level = STARTING_LEVEL

        self.sign_message = None # not sure if this is a good place for this

        self.load_level()
        #self.title_music.play()
        self.audio.play_music('title_music')

    def load_level(self):
        # Make sprite groups
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()
        self.infobox = None

        # Load the level data
        with open(LEVELS[self.level - 1]) as f:
            self.data = json.load(f) # self only needed on data to pass to world editor

        # World settings
        self.world_width = self.data['width'] * GRID_SIZE
        self.world_height = self.data['height'] * GRID_SIZE
        self.gravity = self.data['gravity']
        self.terminal_velocity = self.data['terminal_velocity']

        # Load background and music
        self.bg_img = Image(self.data['background'])

        # Position and stop the hero (without stopping, a hero in mid-jump at goal continues at start)
        loc = self.data['start']
        self.hero.move_to(loc)
        self.hero.vx = 0
        self.hero.vy = 0

        # Add the platforms
        if 'grass' in self.data:   
            for loc in self.data['grass']:
                self.platforms.add( Platform(self, self.grass_dirt_img, loc) )

        if 'blocks' in self.data:    
            for loc in self.data['blocks']:
                self.platforms.add( Platform(self, self.block_img, loc) )

        # Add the items
        if 'gems' in self.data:
            for loc in self.data['gems']:
                self.items.add( Gem(self, self.gem_img, loc) )

        if 'hearts' in self.data:
            for loc in self.data['hearts']:
                self.items.add( Heart(self, self.heart_img, loc) )

        if 'keys' in self.data:
            for key in self.data['keys']:
                self.items.add( Key(self, self.key_img, key['loc'], key['code']) )
   
        # Add the enemies
        if 'spikeballs' in self.data:
            for loc in self.data['spikeballs']:
                self.enemies.add( SpikeBall(self, self.spikeball_imgs, loc) )

        if 'spikemen' in self.data:
            for loc in self.data['spikemen']:
                self.enemies.add( SpikeMan(self, self.spikeman_imgs_rt, loc) )

        if 'clouds' in self.data:
            for loc in self.data['clouds']:
                self.enemies.add( Cloud(self, self.cloud_img, loc) )

        # Add Interactables
        if 'doors' in self.data:
            for door in self.data['doors']:
                if 'code' in door:
                    self.interactables.add( Door(self, self.locked_doortop_img, door['loc'], door['dest'], door['code']) )
                else:
                    self.interactables.add( Door(self, self.doortop_img, door['loc'], door['dest']) )

        if 'signs' in self.data:
            for sign in self.data['signs']:
                self.interactables.add( Sign(self, self.sign_img, sign['loc'], sign['message']) )
                                
        if 'npcs' in self.data:
            for npc in self.data['npcs']:
                self.interactables.add( NPC(self, self.robot_imgs_walk_rt, npc['loc'], npc['message']) )

        # Add the goal
        if 'goals' in self.data:
            for i, loc in enumerate(self.data['goals']):
                if i == 0:
                    self.goals.add( Goal(self, self.flag_img, loc) )
                else:
                    self.goals.add( Goal(self, self.flagpole_img, loc) )

        # Make one big sprite group for easy drawing and updating
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_sprites.add(self.hero, self.platforms, self.items, self.enemies, self.goals, self.interactables)
    
    def start(self):
        self.stage = PLAYING
        self.audio.play_music('main_theme')

    def complete_level(self):
        self.stage = LEVEL_COMPLETE
        self.transition_timer = 3 * FPS
        #self.playing_music.stop()
        self.audio.play_sound('level_up')
        self.hero.score += POINTS_PER_LEVEL

    def advance(self):
        self.level += 1
        self.load_level()
        self.start()

    def win(self):
        self.stage = WIN

    def lose(self):
        self.stage = LOSE

    def get_offsets(self):
        if self.hero.rect.centerx < WIDTH // 2:
            offset_x = 0
        elif self.hero.rect.centerx > self.world_width - WIDTH // 2:
            offset_x = self.world_width - WIDTH
        else:
            offset_x = self.hero.rect.centerx - WIDTH // 2

        return offset_x, 0

    def are_close(self, sprite1, sprite2):
        dx = abs(sprite1.rect.centerx - sprite2.rect.centerx)
        dy = abs(sprite1.rect.centery - sprite2.rect.centery)

        return dx < 1.5 * WIDTH and dy < 1.5 * HEIGHT # In video, demo how using 1.0 * HEIGHT doesn't work when hero jumps off top of screen,
                                                      # Also keeps enemies just off screen from freezing immediately

    def process_input(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g: # eventually toggle editor mode with 'e' 
                    self.grid.toggle()
                elif event.key == pygame.K_m:
                    self.audio.toggle_mute()

                # this shouldn't go here?
                if self.stage == EDIT:
                    if event.key == pygame.K_RIGHT:
                        self.tile_index = (self.tile_index + 1) % len(self.tile_images)
                    elif event.key == pygame.K_s:
                        self.save()

                # Actual gameplay
                if self.stage == START:
                    if event.key == pygame.K_SPACE:
                        self.start()

                elif self.stage == PLAYING:
                    if event.key == pygame.K_p:
                        self.stage = PAUSE

                    if event.key == CONTROLS['jump']:
                        self.hero.jump()
                    elif event.key == CONTROLS['interact']:
                        self.hero.interact()
                    elif event.key == CONTROLS['continue']:
                        self.hero.uninteract()

                elif self.stage == PAUSE:
                    if event.key == pygame.K_p:
                        self.stage = PLAYING

                elif self.stage in [WIN, LOSE]:
                    if event.key == pygame.K_r:
                        self.new_game()
                        
            if self.stage == EDIT:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.add_tile()
                
        if self.stage == PLAYING:
            pressed = pygame.key.get_pressed()

            if pressed[CONTROLS['left']]:
                self.hero.go_left()
            elif pressed[CONTROLS['right']]:
                self.hero.go_right()
            else:
                self.hero.stop()
     
    def update(self):
        if self.stage == PLAYING and not self.hero.is_interacting:
            #self.all_sprites.update()

            # only update nearby sprites for better performance
            for sprite in self.all_sprites:
                if (self.are_close(sprite, self.hero)):
                    sprite.update()

            if self.hero.reached_goal():
                self.complete_level()
            elif not self.hero.is_alive():
                self.lose()
                
        elif self.stage == LEVEL_COMPLETE:
            if self.transition_timer > 0:
                self.transition_timer -= 1
            else:
                if self.level < len(LEVELS):
                    self.advance()
                else:
                    self.win()

    def render(self):
        offset_x, offset_y = self.get_offsets()
        bg_offset_x = -1 * (0.5 * offset_x % self.bg_img.get_width()) # 0.5 is 'magic'. not good. make it a variable in the level

        #screen.fill(SKY_BLUE)
        self.screen.blit(self.bg_img, [bg_offset_x, 0])
        self.screen.blit(self.bg_img, [bg_offset_x + self.bg_img.get_width(), 0])

        # will this still handle layers?
        for sprite in self.all_sprites:
            # what about making is_close(sprite) in Entity. Then,
            # if self.hero.is_close(sprite):
            #     blit...
            # it seems better gramatically
            if self.are_close(sprite, self.hero):
                self.screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y - offset_y])

        if self.infobox is not None:
            self.infobox.draw(self.screen)
        
        self.hud.draw(self.screen)

        if self.stage == START:
            self.title_screen.draw(self.screen)
        elif self.stage == LEVEL_COMPLETE:
            self.level_complete_screen.draw(self.screen)
        elif self.stage == WIN:
            self.win_screen.draw(self.screen)
        elif self.stage == LOSE:
            self.lose_screen.draw(self.screen)
        elif self.stage == PAUSE:
            self.pause_screen.draw(self.screen)

        self.grid.draw(self.screen)
        
    def play(self):
        while self.running:
            self.process_input()     
            self.update()     
            self.render()
            
            pygame.display.update()
            self.clock.tick(FPS)


# Let's do this!
if __name__ == "__main__":
   g = Game()
   g.play()
   pygame.quit()   
