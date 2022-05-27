# Imports
import json
import pygame

from settings import *
from utilities import *
from entities import *


# Main game class 
class Game:

    def __init__(self):
        self.running = True
        self.grid_on = False
        self.new_game()

    def new_game(self):
        # make the hero here so it persists across levels
        self.player = pygame.sprite.GroupSingle()
        self.hero = Hero(self, hero_imgs_idle_rt)
        self.player.add(self.hero)

        # Go to first level
        self.stage = START
        self.level = 1
        self.start_level()
        
    def start_level(self):
        # Make sprite groups
        self.platforms = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Load the level data
        with open(levels[self.level - 1]) as f:
            data = json.load(f)

        # World settings
        self.world_width = data['width'] * GRID_SIZE
        self.world_height = data['height'] * GRID_SIZE
        self.gravity = data['gravity']
        self.terminal_velocity = data['terminal_velocity']
        
        # Position the hero
        loc = data['start']
        self.hero.move_to(loc)
        
        # Add the platforms
        if 'grass_locs' in data:
            for loc in data['grass_locs']:
                self.platforms.add( Platform(self, grass_dirt_img, loc) )
                
        if 'block_locs' in data:
            for loc in data['block_locs']:
                self.platforms.add( Platform(self, block_img, loc) )

        if 'gem_locs' in data:
            for loc in data['gem_locs']:
                self.items.add( Gem(self, gem_img, loc) )

        if 'spikeball_locs' in data:
            for loc in data['spikeball_locs']:
                self.enemies.add( SpikeBall(self, spikeball_imgs, loc) )

        if 'cloud_locs' in data:
            for loc in data['cloud_locs']:
                self.enemies.add( Cloud(self, cloud_img, loc) )

        if 'spikeman_locs' in data:
            for loc in data['spikeman_locs']:
                self.enemies.add( SpikeMan(self, spikeman_imgs_rt, loc) )

        if 'goal_locs' in data:
            for n, loc in enumerate(data['goal_locs']):
                if n == 0:
                    image = flag_img
                else:
                    image = flagpole_img
                self.goals.add( Goal(self, image, loc) )

        # Make one big sprite group for easy drawing and updating
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player, self.platforms, self.goals, self.items, self.enemies)
        
    def show_title_screen(self):
        text = FONT_XL.render(TITLE, True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 16
        screen.blit(text, rect)
    
        text = FONT_MD.render("Press 'ENTER' to start.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 16
        screen.blit(text, rect)
        
    def show_win_screen(self):
        text = FONT_LG.render("You win!", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 16
        screen.blit(text, rect)
    
        text = FONT_MD.render("Press 'r' key to play again.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 16
        screen.blit(text, rect)
        
    def show_lose_screen(self):
        text = FONT_LG.render("You lose.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 16
        screen.blit(text, rect)
    
        text = FONT_MD.render("Press 'r' key to play again.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 16
        screen.blit(text, rect)
    
    def show_pause_screen(self):
        text = FONT_LG.render("Paused", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 16
        screen.blit(text, rect)
    
        text = FONT_MD.render("Press 'p' key to continue", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 16
        screen.blit(text, rect)
        
    def show_hud(self):
        text = FONT_MD.render('S: ' + str(self.hero.score), True, WHITE)
        rect = text.get_rect()
        rect.top = 16
        rect.left = 16
        screen.blit(text, rect)
    
        text = FONT_MD.render('H: ' + str(self.hero.hearts), True, WHITE)
        rect = text.get_rect()
        rect.top = 48
        rect.left = 16
        screen.blit(text, rect)
    
        text = FONT_MD.render('L: ' + str(self.level), True, WHITE)
        rect = text.get_rect()
        rect.top = 80
        rect.left = 16
        screen.blit(text, rect)
    
    def process_input(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    self.grid_on = not self.grid_on
                    
                if self.stage == START:
                    if event.key == pygame.K_RETURN:
                        self.stage = PLAYING

                elif self.stage == PLAYING:
                    if event.key == pygame.K_p:
                        self.stage = PAUSED
                    elif event.key == pygame.K_SPACE:
                        self.hero.jump()

                elif self.stage == WIN or self.stage == LOSE:
                    if event.key == pygame.K_r:
                        self.new_game()

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_RIGHT]:
            self.hero.move_right()
        elif pressed[pygame.K_LEFT]:
            self.hero.move_left()
        else:
            self.hero.stop()
        
    def update(self):
        if self.stage == PLAYING:
            self.all_sprites.update()

            if self.hero.reached_goal():
                if self.level < len(levels):
                    self.level += 1
                    self.start_level()
                else:
                    self.stage = WIN

            elif not self.hero.is_alive():
                self.stage = LOSE
            
    def get_offsets(self):
        if self.hero.rect.centerx < WIDTH // 2:
            offset_x = 0
        elif self.hero.rect.centerx > self.world_width - WIDTH // 2:
            offset_x = self.world_width - WIDTH
        else:
            offset_x = self.hero.rect.centerx - WIDTH // 2

        return offset_x, 0
    
    def render(self):
        actual_fps = int(clock.get_fps())
        pygame.display.set_caption(TITLE + " " + str(actual_fps))
        
        offset_x, offset_y = self.get_offsets()
        
        screen.fill(SKY_BLUE)

        for sprite in self.all_sprites:
            screen.blit(sprite.image, [sprite.rect.x - offset_x, sprite.rect.y - offset_y])
        
        if self.stage == START:
            self.show_title_screen()
        elif self.stage == WIN:
            self.show_win_screen()
        elif self.stage == LOSE:
            self.show_lose_screen()
        elif self.stage == PAUSED:
            self.show_pause_screen()

        self.show_hud()

        if self.grid_on:
            draw_grid(screen, WIDTH, HEIGHT, GRID_SIZE, offset_x, offset_y)
                                                 
    def play(self):
        while self.running:
            self.process_input()     
            self.update()     
            self.render()
            
            pygame.display.update()
            clock.tick(FPS)


# Let's do this!
if __name__ == "__main__":
   g = Game()
   g.play()
   pygame.quit()   
