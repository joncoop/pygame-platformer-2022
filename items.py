from entities import *

# Items - Objects that alter the state of the hero
class Gem(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

    def apply(self, character):
        character.score += POINTS_PER_COIN
        character.gems += 1
        self.game.audio.play_sound('gem')
        self.kill()


class Heart(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

    def apply(self, character):
        character.score += POINTS_PER_POWERUP
        #character.hearts += 1
        #character.hearts = min(charcter.hearts + 1, character.max_hearts)
        character.hearts = character.max_hearts
        self.game.audio.play_sound('powerup')
        self.kill()


class Key(Entity):
    
    def __init__(self, game, image, loc, code):
        super().__init__(game, image, loc)
        self.code = code

    def apply(self, character):
        character.keys.append(self.code)
        self.game.audio.play_sound('powerup')
        self.kill()


class Goal(Entity):

    def __init__(self, game, image, loc):
        super().__init__(game, image, loc)

    def apply(self, character):
        character.reached_goal = True