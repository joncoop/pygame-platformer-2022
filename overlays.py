from settings import *
from utilities import *

class TitleScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = Font(PRIMARY_FONT, 80)
        self.subtitle_font = Font(SECONDARY_FONT, 64)
        self.default_font = Font(SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.title_font.render(TITLE, True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.default_font.render("Press 'SPACE' to start.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 8
        surface.blit(text, rect)


class WinScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = Font(PRIMARY_FONT, 80)
        self.subtitle_font = Font(SECONDARY_FONT, 64)
        self.default_font = Font(SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.subtitle_font.render("You win!", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.default_font.render("Press 'r' to play again.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 8
        surface.blit(text, rect)


class LoseScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = Font(PRIMARY_FONT, 80)
        self.subtitle_font = Font(SECONDARY_FONT, 64)
        self.default_font = Font(SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.subtitle_font.render("You lose!", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.default_font.render("Press 'r' to play again.", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 8
        surface.blit(text, rect)


class LevelCompleteScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = Font(PRIMARY_FONT, 80)
        self.subtitle_font = Font(SECONDARY_FONT, 64)
        self.default_font = Font(SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.subtitle_font.render("Level Complete!", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        surface.blit(text, rect)


class PauseScreen:

    def __init__(self, game):
        self.game = game

        self.title_font = Font(PRIMARY_FONT, 80)
        self.subtitle_font = Font(SECONDARY_FONT, 64)
        self.default_font = Font(SECONDARY_FONT, 32)
        
    def update(self):
        pass

    def draw(self, surface):
        text = self.subtitle_font.render("Paused", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.bottom = HEIGHT // 2 - 8
        surface.blit(text, rect)
    
        text = self.default_font.render("Press 'p' to continue", True, WHITE)
        rect = text.get_rect()
        rect.centerx = WIDTH // 2
        rect.top = HEIGHT // 2 + 8
        surface.blit(text, rect)


class HUD:

    def __init__(self, game):
        self.game = game

        self.title_font = Font(PRIMARY_FONT, 80)
        self.subtitle_font = Font(SECONDARY_FONT, 64)
        self.default_font = Font(SECONDARY_FONT, 32)

        self.gem_img = Image(GEM_IMG)
        self.heart_img = Image(HEART_IMG)
        
    def update(self):
        pass

    def draw(self, surface):
        ##text = self.default_font.render('S: ' + str(self.game.hero.score), True, WHITE)
        ##rect = text.get_rect()
        ##rect.top = 16
        ##rect.left = 16
        #surface.blit(text, rect)
    
        ##text = self.default_font.render('H: ' + str(self.game.hero.hearts), True, WHITE)
        ##rect = text.get_rect()
        ##rect.top = 48
        ##rect.left = 16
        ##surface.blit(text, rect)
    
        ##text = self.default_font.render('L: ' + str(self.game.level), True, WHITE)
        ##rect = text.get_rect()
        ##rect.top = 80
        ##rect.left = 16
        ##surface.blit(text, rect)

        text = self.default_font.render(str(self.game.hero.score), True, WHITE)
        rect = text.get_rect()
        rect.midtop = WIDTH // 2, 16
        surface.blit(text, rect)

        surface.blit(self.gem_img, [WIDTH - 100, 16])
        text = self.default_font.render('x' + str(self.game.hero.gems), True, WHITE)
        rect = text.get_rect()
        rect.topleft = WIDTH - 60, 24
        surface.blit(text, rect)

        for i in range(self.game.hero.hearts):
            x = i * 36 + 16
            y = 16
            surface.blit(self.heart_img, [x, y])



