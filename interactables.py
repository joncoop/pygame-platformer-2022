from entities import *

# Interactables - Objects that alter the state of the world
class Door(Entity):
    
    def __init__(self, x, y, image, destination, code=None):
        super().__init__(x, y, image)
        self.destination= destination
        self.code = code

    def interact(self, character):
        if self.code is None or self.code in character.keys:
            character.move_to(self.destination)


# Some Interactables pause the game so the hero can get information
class Sign(Entity):
    
    def __init__(self, game, image, loc, message):
        super().__init__(game, image, loc)
        self.message = message
        self.active = False

    def interact(self, character):
        character.is_interacting = True
        self.game.infobox = SignPopup(self.game, self.message)

        
class NPC(AnimatedEntity):
    def __init__(self, game, images, loc, message):
        super().__init__(game, images, loc)
        self.message = message

        self.vx = NPC_SPEED
        self.vy = 0

    def interact(self, character):
        character.is_interacting = True
        self.game.infobox = SpeechBubble(self.game, self.message)

    def set_image_list(self):
        if self.vx < 0:
            self.images = self.game.robot_imgs_walk_lt
        else:
            self.images = self.game.robot_imgs_walk_rt

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


# Readables
class SignPopup:

    def __init__(self, game, message):
        self.game = game
        self.message = message

    def draw(self, surface):
        text = self.game.default_font.render(self.message, True, WHITE)
        text_rect = text.get_rect()
        text_rect.centerx = WIDTH // 2
        text_rect.centery = HEIGHT // 2

        background_rect = text_rect.copy()
        background_rect.width = background_rect.width + GRID_SIZE // 2
        background_rect.height = background_rect.height + GRID_SIZE // 2
        background_rect.center = text_rect.center

        pygame.draw.rect(surface, BROWN, background_rect, 0, 6)
        pygame.draw.rect(surface, BLACK, background_rect, 2, 6)
        surface.blit(text, text_rect)


# figure out how to make this advance through messages. what key to use? still down?
class SpeechBubble:
    def __init__(self, game, message):
        self.game = game
        self.message = message

    def draw(self, surface):
        # this is gross. make it more like sign
        text = self.game.default_font.render(self.message, True, BLACK)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.centery = HEIGHT // 2

        outline = [rect.left - GRID_SIZE / 2, rect.top - GRID_SIZE / 2, rect.width + GRID_SIZE, rect.height + GRID_SIZE]

        pygame.draw.rect(surface, WHITE, outline, 0, 6)
        pygame.draw.rect(surface, BLACK, outline, 2, 6)
        pygame.draw.polygon(surface, WHITE, [[rect.centerx - 40, rect.bottom - 2 + GRID_SIZE / 2], [rect.centerx + 40, rect.bottom - 5 + GRID_SIZE / 2], [rect.centerx, rect.bottom + 3 * GRID_SIZE // 2]])
        pygame.draw.line(surface, BLACK, [rect.centerx - 40, rect.bottom - 2 + GRID_SIZE / 2], [rect.centerx, rect.bottom + 3 * GRID_SIZE // 2], 2)
        pygame.draw.line(surface, BLACK, [rect.centerx + 40, rect.bottom - 2 + GRID_SIZE / 2], [rect.centerx, rect.bottom + 3 * GRID_SIZE // 2], 2)

        surface.blit(text, rect)
