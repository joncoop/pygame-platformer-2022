from entities import *

# Player character
class Hero(AnimatedEntity):

    def __init__(self, game, images):
        super().__init__(game, images)

        self.vx = 0
        self.vy = 0
        self.speed = HERO_SPEED
        self.jump_power = HERO_JUMP_POWER
        self.facing_right = True
        self.reached_goal = False

        self.score = 0
        self.gems = 0
        self.hearts = 5
        self.max_hearts = 5
        self.escape_time = 0
        self.keys = []
        self.is_interacting = False # move this to game (only pause/freeze during sign interactions)

    def go_left(self):
        self.vx = -1 * self.speed
        self.facing_right = False
        self.uninteract()
    
    def go_right(self):
        self.vx = self.speed
        self.facing_right = True
        self.uninteract()

    def stop(self):
        self.vx = 0
        
    def jump(self):
        if self.on_platform():
            self.vy = -1 * self.jump_power
            self.game.audio.play_sound('jump')
        self.uninteract()

    def is_alive(self):
        return self.hearts > 0

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
                self.game.audio.play_sound('hurt')

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
            interactable.interact(self)

    def uninteract(self):
        self.is_interacting = False
        self.game.infobox = None

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
