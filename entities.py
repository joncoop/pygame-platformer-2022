# Imports
import pygame
from settings import *


# Base classes
class Entity(pygame.sprite.Sprite):

    def __init__(self, game, image, loc=[0, 0]):
        super().__init__()

        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.move_to(loc)

    def move_to(self, loc):
        self.rect.centerx = loc[0] * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = loc[1] * GRID_SIZE + GRID_SIZE // 2

    def apply_gravity(self):
        ##self.vy += GRAVITY
        self.vy += self.game.gravity
        self.vy = min(self.vy, self.game.terminal_velocity)
    
    def reverse(self):
        self.vx *= -1

    def on_platform(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2

        return len(hits) > 0

    def move_x(self):
        self.rect.x += self.vx

    def check_platforms_x(self):
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

        for platform in hits:
            if self.vx < 0:
                self.rect.left = platform.rect.right
            elif self.vx > 0:
                self.rect.right = platform.rect.left

        if hits:
            self.reverse()

    def move_y(self):
        self.rect.y += self.vy

    def check_platforms_y(self):
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

        for platform in hits:
            if self.vy < 0:
                self.rect.top = platform.rect.bottom
            elif self.vy > 0:
                self.rect.bottom = platform.rect.top
        
        if hits:
            self.vy = 0

    def check_world_edges(self):
        at_edge = False

        if self.rect.left < 0:
            self.rect.left = 0
            at_edge = True
        elif self.rect.right > self.game.world_width:
            self.rect.right = self.game.world_width
            at_edge = True

        if at_edge:
            self.reverse()

        if self.rect.top > self.game.world_height:
            self.kill()

    def check_platform_edges(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2

        at_edge = True

        for platform in hits:
            if self.vx > 0:
                if platform.rect.right >= self.rect.right:
                    at_edge = False
            if self.vx < 0:
                if platform.rect.left <= self.rect.left:
                    at_edge = False

        if at_edge:
            self.reverse()


class AnimatedEntity(Entity):
    
    def __init__(self, game, images, loc=[0, 0]):
        super().__init__(game, images[0], loc)

        self.images = images
        self.image_index = 0
        self.ticks = 0
        self.frame_rate = 10

    def set_image_list(self):
        self.images = self.images

    def animate(self):
        self.set_image_list()
        
        self.ticks += 1
        
        if self.ticks % self.frame_rate == 0:
            if self.image_index >= len(self.images):
                self.image_index = 0
                
            self.image = self.images[self.image_index]
            self.image_index += 1
        
    def update(self):
        self.animate()
        

# Tiles
class Platform(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)


# Player character
class Hero(AnimatedEntity):

    def __init__(self, game, images):
        super().__init__(game, images)

        self.vx = 0
        self.vy = 0
        self.speed = HERO_SPEED
        self.jump_power = HERO_JUMP_POWER
        self.facing_right = True

        self.score = 0
        self.gems = 0
        self.hearts = 5
        self.max_hearts = 5
        self.escape_time = 0
        self.keys = []
        self.is_interacting = False

    def go_left(self):
        self.vx = -1 * self.speed
        self.facing_right = False
        self.is_interacting = False
    
    def go_right(self):
        self.vx = self.speed
        self.facing_right = True
        self.is_interacting = False

    def stop(self):
        self.vx = 0
        
    def jump(self):
        if self.on_platform():
            self.vy = -1 * self.jump_power
            self.game.jump_snd.play()
        self.is_interacting = False

    def is_alive(self):
        return self.hearts > 0

    def reached_goal(self):
        hits = pygame.sprite.spritecollide(self, self.game.goals, False)

        return len(hits) > 0

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, self.game.items, False)

        for item in hits:
            item.apply(self)

    def set_image_list(self):
        if self.facing_right:
            if not self.on_platform():
                self.images = self.game.hero_imgs_jump_rt
            elif self.vx > 0:
                self.images = self.game.hero_imgs_walk_rt
            else:
                self.images = self.game.hero_imgs_idle_rt
        else:
            if not self.on_platform():
                self.images = self.game.hero_imgs_jump_lt
            elif self.vx < 0:
                self.images = self.game.hero_imgs_walk_lt
            else:
                self.images = self.game.hero_imgs_idle_lt

    def check_enemies(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

        if self.escape_time == 0:
            for enemy in hits:
                self.hearts -= 1
                self.escape_time = 30
                self.game.hurt_snd.play()

                if self.rect.centerx < enemy.rect.centerx:
                    self.vx = -15
                elif self.rect.centerx > enemy.rect.centerx:
                    self.vx = 15

                if self.rect.centery < enemy.rect.centery:
                    self.vy = -10
                elif self.rect.centery > enemy.rect.centery:
                    self.vy = 10
        else:
            self.escape_time -= 1

    def check_fall_death(self):
        if self.rect.top > self.game.world_height:
            self.hearts = 0

    def interact(self):
        hits = pygame.sprite.spritecollide(self, self.game.interactables, False)

        for interactable in hits:
            interactable.interact()
            self.is_interacting = True

    def update(self):
        self.apply_gravity()
        self.check_enemies() # needs to be before move to override vx and vy from player controls
        self.move_x()
        self.check_platforms_x()
        self.move_y()
        self.check_world_edges()
        self.check_platforms_y()
        #self.check_enemies()
        self.check_fall_death()
        self.check_items()
        self.animate()

# Enemies
class Goal(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)


class SpikeBall(AnimatedEntity):
    
    def __init__(self, game, images, loc):
        super().__init__(game, images, loc)
        self.vx = -1 * SPIKEBALL_SPEED
        self.vy = 0

    def update(self):
        self.apply_gravity()
        self.move_x()
        self.check_platforms_x()
        self.move_y()
        self.check_platforms_y()
        self.check_world_edges()
        self.animate()

        
class Cloud(Entity):
    
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.vx = -1 * CLOUD_SPEED
        self.vy = 0

    def update(self):
        self.move_x()
        self.check_world_edges()


class SpikeMan(AnimatedEntity):
    
    def __init__(self, game, images, loc):
        super().__init__(game, images, loc)
        self.vx = SPIKEMAN_SPEED
        self.vy = 0
    
    def set_image_list(self):
        if self.vx < 0:
            self.images = self.game.spikeman_imgs_lt
        else:
            self.images = self.game.spikeman_imgs_rt

    def update(self):
        self.apply_gravity()
        self.move_x()
        self.check_platforms_x()
        self.move_y()
        self.check_platforms_y()
        self.check_platform_edges()
        self.animate()


# Items
class Gem(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

    def apply(self, character):
        character.score += POINTS_PER_COIN
        character.gems += 1
        self.game.gem_snd.play()
        self.kill()


class Heart(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

    def apply(self, character):
        character.score += POINTS_PER_POWERUP
        #character.hearts += 1
        #character.hearts = min(charcter.hearts + 1, character.max_hearts)
        character.hearts = character.max_hearts
        self.game.powerup_snd.play()
        self.kill()


# Interactables
class Door(Entity):
    
    def __init__(self, x, y, image, destination, code=None):
        super().__init__(x, y, image)
        self.destination= destination
        self.code = code

    def interact(self):
        if self.code is None or self.code in self.game.hero.keys:
            self.game.hero.move_to(self.destination)
        
    
class Key(Entity):
    
    def __init__(self, game, image, loc, code):
        super().__init__(game, image, loc)
        self.code = code

    def apply(self, character):
        character.keys.append(self.code)
        self.game.powerup_snd.play()
        self.kill()


class Sign(Entity):
    
    def __init__(self, game, image, loc, message):
        super().__init__(game, image, loc)
        self.message = message

    def interact(self):
       # print(self.message)
       self.game.sign_message = self.message
