# Imports
import pygame

from entities import *
from settings import *

  
# Enemies
class SpikeBall(AnimatedEntity):
    
    def __init__(self, game, images, loc):
        super().__init__(game, images, loc)
        self.vx = -1 * SPIKEBALL_SPEED
        self.vy = 0

    def update(self):
        self.apply_gravity() #does this need to go first?
        self.move_x() # does x movement need to happen before y?
        hit_something = self.check_platforms_x()
        self.move_y()
        self.check_platforms_y()
        at_world_edge = self.check_world_edges()
        if hit_something or at_world_edge:
            self.reverse()
        self.animate()
        
class Cloud(Entity):
    
    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)
        self.vx = -1 * CLOUD_SPEED
        self.vy = 0

    def update(self):
        self.move_x()
        at_world_edge = self.check_world_edges()
        if at_world_edge:
            self.reverse()


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
        self.apply_gravity() #does this need to go first?
        self.move_x() # does x movement need to happen before y?
        hit_something = self.check_platforms_x()
        self.move_y()
        self.check_platforms_y()
        at_platform_edge = self.check_platform_edges() # does this need to be after gravity?
        at_world_edge = self.check_world_edges()
        if hit_something or at_platform_edge or at_world_edge:
            self.reverse()
        self.animate()
