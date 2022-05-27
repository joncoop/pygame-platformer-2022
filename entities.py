import pygame
from settings import *


# Base classes
class Entity(pygame.sprite.Sprite):

    def __init__(self, game, image, loc=[0, 0]):
        super().__init__()

        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.on_platform = False
        
        self.move_to(loc)
        
    def move_to(self, loc):
        self.rect.centerx = loc[0] * GRID_SIZE + GRID_SIZE // 2
        self.rect.centery = loc[1] * GRID_SIZE + GRID_SIZE // 2

    def apply_gravity(self):
        self.vy += self.game.gravity
        self.vy = min(self.vy, self.game.terminal_velocity)

    def reverse(self):
        self.vx *= -1
        
    def move_and_check_platforms(self):
        self.rect.x += self.vx
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

        for platform in hits:
            if self.vx > 0:
                self.rect.right = platform.rect.left
            elif self.vx < 0:
                self.rect.left = platform.rect.right

        if len(hits) > 0:
            self.reverse()

        if 0 < self.vy < 1:
            self.rect.y += 1.0
        else:
            self.rect.y += self.vy
            
        self.on_platform = False
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        
        for platform in hits:
            if self.vy > 0:
                self.rect.bottom = platform.rect.top
                self.on_platform = True
            elif self.vy < 0:
                self.rect.top = platform.rect.bottom

        if len(hits) > 0:
            self.vy = 0
        
    def check_world_edges(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > self.game.world_width:
            self.rect.right = self.game.world_width
            self.reverse()

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
        self.frames_per_update = 10

    def set_image_list(self):
        self.images = self.images

    def animate(self):
        self.set_image_list()
        
        self.ticks += 1
        
        if self.ticks % self.frames_per_update == 0:
            if self.image_index >= len(self.images):
                self.image_index = 0
                
            self.image = self.images[self.image_index]
            self.image_index += 1
        

# Tiles     
class Platform(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)


class Goal(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)


# Player character
class Hero(AnimatedEntity):

    def __init__(self, game, images):
        super().__init__(game, images)

        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.jump_power = 20
        self.facing_right = True

        self.hearts = 5
        self.score = 0
        self.escape_time = 0

    def move_left(self):
        self.vx = -1 * self.speed
        self.facing_right = False
    
    def move_right(self):
        self.vx = self.speed
        self.facing_right = True

    def stop(self):
        self.vx = 0
        
    def jump(self):
        if self.on_platform:
            self.vy = -1 * self.jump_power

    def check_items(self):
        hits = pygame.sprite.spritecollide(self, self.game.items, False)

        for item in hits:
            item.apply(self)

    def check_enemies(self):
        if self.escape_time <= 0:
            hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

            for enemy in hits:
                self.hearts -= 1
                self.escape_time = 30

                if self.rect.centerx < enemy.rect.centerx:
                    self.vx = -20
                elif self.rect.centerx > enemy.rect.centerx:
                    self.vx = 20

                if self.rect.centery < enemy.rect.centery:
                    self.vy = -5
                elif self.rect.centery > enemy.rect.centery:
                    self.vy = 5
        else:
            self.escape_time -= 1
        
    def reached_goal(self):
        hits = pygame.sprite.spritecollide(self, self.game.goals, False)

        return len(hits) > 0

    def is_alive(self):
        return self.hearts > 0
    
    def set_image_list(self):
        if self.facing_right:
            if not self.on_platform:
                self.images = hero_imgs_jump_rt
            elif self.vx > 0:
                self.images = hero_imgs_walk_rt
            else:
                self.images = hero_imgs_idle_rt
        else:
            if not self.on_platform:
                self.images = hero_imgs_jump_lt
            elif self.vx < 0:
                self.images = hero_imgs_walk_lt
            else:
                self.images = hero_imgs_idle_lt
        
    def update(self):
        self.apply_gravity()
        self.check_enemies()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_items()
        self.animate()


# Enemies
class SpikeBall(AnimatedEntity):
    
    def __init__(self, game, images, loc):
        super().__init__(game, images, loc)
        self.vx = -2
        self.vy = 0

    def update(self):
        self.apply_gravity()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.animate()

        
class SpikeMan(AnimatedEntity):
    
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.vx = -2
        self.vy = 0
        self.frames_per_update = 7

    def set_image_list(self):
        if self.vx > 0:
            self.images = spikeman_imgs_rt
        else:
            self.images = spikeman_imgs_lt
        
    def update(self):
        self.apply_gravity()
        self.move_and_check_platforms()
        self.check_world_edges()
        self.check_platform_edges()
        self.animate()

        
class Cloud(Entity):
    
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.vx = -2
        self.vy = 0

    def update(self):
        self.move_and_check_platforms()
        self.check_world_edges()
        
# Items
class Gem(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

    def apply(self, character):
        character.score += 10
        self.kill()

