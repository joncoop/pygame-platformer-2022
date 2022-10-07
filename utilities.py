# Imports
import pygame
pygame.init() # Needed for loading a font. Don't know why.


class Image(pygame.surface.Surface):
    def __init__(self, path):
        image = pygame.image.load(path).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        super().__init__([width, height], pygame.SRCALPHA, 32)
        self.blit(image, [0, 0])
    
    def get_flipped_x(self):
        return pygame.transform.flip(self, True, False)

    def get_flipped_y(self):
        return pygame.transform.flip(self, False, True)


class Sound(pygame.mixer.Sound):

    def __init__(self, path, volume=1.0):
        super().__init__(path)
        self.set_volume(volume)
        self.on = True

    def play(self):
        if self.on:
            super().play()
    
    def mute(self):
        self.on = False

    def unmute(self):
        self.on = True


class Music():

    def __init__(self, path, volume=1.0, loops=-1):
        self.path = path
        self.volume = volume
        self.loops = loops
        self.on = True
            
    def play(self):
        pygame.mixer.music.load(self.path)

        if self.on:
            self.unmute()
        else:
            self.mute()
        
        pygame.mixer.music.play(self.loops) 

    def stop(self, fadeout_time=0):
        pygame.mixer.music.fadeout(fadeout_time)

    def pause(self):
        pygame.mixer.music.pause()

    def restart(self):
        pygame.mixer.music.rewind()
    
    def mute(self):
        pygame.mixer.music.set_volume(0)
        self.on = False

    def unmute(self):
        pygame.mixer.music.set_volume(self.volume)
        self.on = True


class Font(pygame.font.Font):
    def __init__(self, path, size):
        super().__init__(path, size)


# Helper functions to simplify pygame syntax
def draw_text(surface, text, font, color, loc, anchor='topleft', antialias=True):
    text = str(text)
    text = font.render(text, antialias, color)
    rect = text.get_rect()

    if   anchor == 'topleft'     : rect.topleft = loc
    elif anchor == 'bottomleft'  : rect.bottomleft = loc
    elif anchor == 'topright'    : rect.topright = loc
    elif anchor == 'bottomright' : rect.bottomright = loc
    elif anchor == 'midtop'      : rect.midtop = loc
    elif anchor == 'midleft'     : rect.midleft = loc
    elif anchor == 'midbottom'   : rect.midbottom = loc
    elif anchor == 'midright'    : rect.midright = loc
    elif anchor == 'center'      : rect.center = loc
    
    surface.blit(text, rect)


# Draw a grid to help with level design (move this to editor module)
def draw_grid(surface, grid_size, offset_x=0, offset_y=0, color=(125, 125, 125), font=Font(None, 16)):
    width = surface.get_width()
    height = surface.get_height()

    for x in range(0, width + grid_size, grid_size):
        adj_x = x - offset_x % grid_size
        pygame.draw.line(surface, color, [adj_x, 0], [adj_x, height], 1)

    for y in range(0, height + grid_size, grid_size):
        adj_y = y - offset_y % grid_size
        pygame.draw.line(surface, color, [0, adj_y], [width, adj_y], 1)

    for x in range(0, width + grid_size, grid_size):
        for y in range(0, height + grid_size, grid_size):
            adj_x = x - offset_x % grid_size + 4
            adj_y = y - offset_y % grid_size + 4
            disp_x = x // grid_size + offset_x // grid_size
            disp_y = y // grid_size + offset_y // grid_size
            
            point = f'({disp_x}, {disp_y})'
            text = font.render(point, True, color)
            surface.blit(text, [adj_x, adj_y])
