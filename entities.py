import pygame
from settings import *

'''
I should document this really well, with type hinting.
'''

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

        return len(hits) > 0

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

        if self.rect.top > self.game.world_height: # should this move into enemy class?
            self.kill()

        return at_edge

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

        return at_edge


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


# to add...
class Tile(Entity): # Or should it be AnimatedEntity? Should everything? Should this even be a base class?
    pass

class Item:
    pass

class Interactable:
    pass