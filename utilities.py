# Imports
import pygame


class Image(pygame.surface.Surface):
    def __init__(self, path):
        image = pygame.image.load(path).convert_alpha()
        width = image.get_width()
        height = image.get_height()
        super().__init__([width, height], pygame.SRCALPHA, 32)
        self.blit(image, [0, 0])
    
    def flip_x(self):
        return pygame.transform.flip(self, True, False)

    def flip_y(self):
        return pygame.transform.flip(self, False, True)


# What about separate Sounds and Music classes? Then same syntax add/play. Can mute independently.
class Audio():

    def __init__(self):
        self.music = {}
        self.sounds = {}

    def add_music(self, name, path, volume=1.0, loops=-1):
        self.music[name] = Music(path, volume, loops)

    def add_sound(self, name, path, volume=1.0):
        self.sounds[name] = Sound(path, volume)

    def play_music(self, name):
        self.music[name].play()

    def play_sound(self, name):
        self.sounds[name].play()

    def mute(self):
        # better to set all volumes to zero?
        pygame.mixer.stop()

    def unmute(self):
        pass


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
        # stop active sounds or just let them play out?

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

