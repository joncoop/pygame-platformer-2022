# Imports
import json
import pygame

from settings import *
from utilities import *
from entities import *


# Constants
''' stages '''
START = 0
PLAYING = 1
PAUSE = 2
LEVEL_COMPLETE = 3
WIN = 4
LOSE = 5
EDIT = 6

''' layers '''
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
        self.grid_on = False
        self.mute = False

        self.load_assets()
        self.new_game()

        # for editor, move to separate editor class
        self.tile_index = 0 
        self.tile_images = [None, self.block_img, self.grass_dirt_img]

    def load_assets(self):
        ##self.bg_img = Image(BACKGROUND_IMG)

        self.hero_imgs_idle_rt = [Image(img_path) for img_path in HERO_IMGS_IDLE_RT]
        self.hero_imgs_walk_rt = [Image(img_path) for img_path in HERO_IMGS_WALK_RT]
        self.hero_imgs_jump_rt = [Image(img_path) for img_path in HERO_IMGS_JUMP_RT]
        self.hero_imgs_idle_lt = [img.get_flipped_x() for img in self.hero_imgs_idle_rt]
        self.hero_imgs_walk_lt = [img.get_flipped_x() for img in self.hero_imgs_walk_rt]
        self.hero_imgs_jump_lt = [img.get_flipped_x() for img in self.hero_imgs_jump_rt]

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
        self.spikeman_imgs_lt = [img.get_flipped_x() for img in self.spikeman_imgs_rt]
        self.cloud_img = Image(CLOUD_IMG)

        self.jump_snd = Sound(JUMP_SND, 0.5)
        self.gem_snd = Sound(GEM_SND)
        self.hurt_snd = Sound(HURT_SND)
        self.powerup_snd = Sound(POWERUP_SND)
        self.level_up_snd = Sound(LEVEL_UP_SND)
        self.all_sounds = [self.jump_snd, self.gem_snd, self.hurt_snd, self.powerup_snd]

        self.title_music = Music(TITLE_MUSIC)
        self.playing_music = Music(PLAYING_MUSIC, 0.6)
        self.all_music = [self.title_music, self.playing_music]

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
        self.title_music.play()

    def load_level(self):
        # Make sprite groups
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.interactables = pygame.sprite.Group()

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

        if 'doors' in self.data:
            for door in self.data['doors']:
                if 'code' in door:
                    self.interactables.add( Door(self, self.locked_doortop_img, door['loc'], door['dest'], door['code']) )
                else:
                    self.interactables.add( Door(self, self.doortop_img, door['loc'], door['dest']) )
                
        if 'signs' in self.data:
            for sign in self.data['signs']:
                self.informables.add( Sign(self, self.sign_img, sign['loc'], sign['message']) )
                                
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
        self.playing_music.play()

    def complete_level(self):
        self.stage = LEVEL_COMPLETE
        self.transition_timer = 3 * FPS
        self.playing_music.stop()
        self.level_up_snd.play()
        self.hero.score += POINTS_PER_LEVEL

    def advance(self):
        self.level += 1
        self.load_level()
        self.start()

    def win(self):
        self.stage = WIN

    def lose(self):
        self.stage = LOSE

    def show_title_screen(self):
        text = self.title_font.render(TITLE, True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        self.screen.blit(text, rect)
    
        text = self.default_font.render("Press 'SPACE' to start.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 8
        self.screen.blit(text, rect)
        
    def show_level_complete_screen(self):
        text = self.subtitle_font.render("Level Complete!", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        self.screen.blit(text, rect)

    def show_win_screen(self):
        text = self.subtitle_font.render("You win!", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        self.screen.blit(text, rect)
    
        text = self.default_font.render("Press 'r' to play again.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 8
        self.screen.blit(text, rect)
        
    def show_lose_screen(self):
        text = self.subtitle_font.render("You lose.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        self.screen.blit(text, rect)
    
        text = self.default_font.render("Press 'r' to play again.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 8
        self.screen.blit(text, rect)
    
    def show_pause_screen(self):
        text = self.subtitle_font.render("Paused", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        self.screen.blit(text, rect)
    
        text = self.default_font.render("Press 'p' to continue", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 8
        self.screen.blit(text, rect)

    def show_hud(self):
        ##text = self.default_font.render('S: ' + str(self.hero.score), True, WHITE)
        ##rect = text.get_rect()
        ##rect.top = 16
        ##rect.left = 16
        #self.screen.blit(text, rect)
    
        ##text = self.default_font.render('H: ' + str(self.hero.hearts), True, WHITE)
        ##rect = text.get_rect()
        ##rect.top = 48
        ##rect.left = 16
        ##self.screen.blit(text, rect)
    
        ##text = self.default_font.render('L: ' + str(self.level), True, WHITE)
        ##rect = text.get_rect()
        ##rect.top = 80
        ##rect.left = 16
        ##self.screen.blit(text, rect)

        text = self.default_font.render(str(self.hero.score), True, WHITE)
        rect = text.get_rect()
        rect.midtop = WIDTH // 2, 16
        self.screen.blit(text, rect)

        self.screen.blit(self.gem_img, [WIDTH - 100, 16])
        text = self.default_font.render('x' + str(self.hero.gems), True, WHITE)
        rect = text.get_rect()
        rect.topleft = WIDTH - 60, 24
        self.screen.blit(text, rect)

        for i in range(self.hero.hearts):
            x = i * 36 + 16
            y = 16
            self.screen.blit(self.heart_img, [x, y])

    # Not sure if I like this here. Should more be in the Sign class?
    def show_message(self):
        text = self.default_font.render(self.sign_message, True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2

        outline = [rect.left - 40, rect.top - 40, rect.width + 80, rect.height + 80]

        pygame.draw.rect(self.screen, BROWN, outline, 0, 6)
        pygame.draw.rect(self.screen, BLACK, outline, 2, 6)
        self.screen.blit(text, rect)

    def toggle_mute(self):
        if self.mute:
            for sound in self.all_sounds:
                sound.unmute()

            for music in self.all_music:
                music.unmute()
        else:
            for sound in self.all_sounds:
                sound.mute()

            for music in self.all_music:
                music.mute()

        self.mute = not self.mute

    def toggle_edit_mode(self):
        if self.stage == EDIT:
            self.stage = self.last_stage
            self.grid_on = False
        else:
            self.last_stage = self.stage
            self.grid_on = True
            self.stage = EDIT

    def show_edit_screen(self):
        tile_names = ['erase', 'block', 'grass']

        text = self.default_font.render(tile_names[self.tile_index], True, WHITE)
        rect = text.get_rect()
        rect.x = 16
        rect.bottom = HEIGHT - 16
        self.screen.blit(text, rect)
 
    def add_tile(self):
        x, y = pygame.mouse.get_pos()
        offset_x, offset_y = self.get_offsets()
        
        loc = [(x + offset_x) // GRID_SIZE, (y + offset_y) // GRID_SIZE]

        for tile in self.platforms:
            existing_tile_loc = [tile.rect.x // 64, tile.rect.y // 64]
            if existing_tile_loc == loc:
                tile.kill()
                if loc in self.data['blocks']:
                    self.data['blocks'].remove(loc)
                if loc in self.data['grass']:
                    self.data['grass'].remove(loc)

        if self.tile_index > 0:
            self.current_img = self.tile_images[self.tile_index]
            tile = Platform(self, self.current_img, loc)
            self.platforms.add(tile)
            self.all_sprites.add(tile) 

            if self.tile_index == 1:
                if not loc in self.data['blocks']:
                    self.data['blocks'].append(loc) 
            elif self.tile_index == 2:
                if not loc in self.data['grass']:
                    self.data['grass'].append(loc)

    def save(self):
        path = LEVELS[self.level - 1] # Remember zero indexing!
        print(path)
        
        with open(path, 'w') as f:
            json.dump(self.data, f) # messy way, but works for now

            # cleaner way (still not that nice)
            tab = '    '
            text = '{\n'
            text += tab + str(self.data['width']) + ',\n'
            text += tab + str(self.data['height']) + ',\n'
            text += tab + str(self.data['gravity']) + ',\n'
            text += tab + str(self.data['terminal_velocity']) + ',\n'
            text += tab + str(self.data['background']) + ',\n'
            text += tab + str(self.data['start']) + ',\n'
            text += tab + str(self.data['grass']) + ',\n'
            text += tab + str(self.data['blocks']) + ',\n'
            text += tab + str(self.data['gems']) + ',\n'
            text += tab + str(self.data['hearts']) + ',\n'
            text += tab + str(self.data['goals']) + ',\n'
            text += tab + str(self.data['spikeballs']) + ',\n'
            text += tab + str(self.data['clouds']) + ',\n'
            text += tab + str(self.data['spikemen']) + '\n'
            text += '}'

            #f.write(text) # I only wrote values, not keys above
        
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
                if event.key == pygame.K_g: 
                    self.grid_on = not self.grid_on
                elif event.key == pygame.K_m:
                    self.toggle_mute()
                elif event.key == pygame.K_e:
                    self.toggle_edit_mode()

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
                    elif event.key == CONTROLS['uninteract']:
                        self.hero.is_interacting = False

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
        offset_x, offset_y = self.get_offsets()
        bg_offset_x = -1 * (0.5 * offset_x % self.bg_img.get_width())

        #screen.fill(SKY_BLUE)
        self.screen.blit(self.bg_img, [bg_offset_x, 0])
        self.screen.blit(self.bg_img, [bg_offset_x + self.bg_img.get_width(), 0])

        # will this still handle layers?
        for sprite in self.all_sprites:
            if self.are_close(sprite, self.hero):
                self.screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y - offset_y])
        
        self.show_hud()

        # this messes up door
        if self.hero.is_interacting:
            self.show_message()

        if self.stage == START:
            self.show_title_screen()
        elif self.stage == LEVEL_COMPLETE:
            self.show_level_complete_screen()
        elif self.stage == WIN:
            self.show_win_screen()
        elif self.stage == LOSE:
            self.show_lose_screen()
        elif self.stage == PAUSE:
            self.show_pause_screen()
        elif self.stage == EDIT:
            self.show_edit_screen()

        if self.grid_on:
            draw_grid(self.screen, GRID_SIZE, offset_x, offset_y)
        
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
