import json

from settings import *
from utilities import *


class Grid:

    def __init__(self, game, color=(125, 125, 125)):
        self.game = game
        self.on = False

        self.color = color
        self.font = Font(None, 16)

    def toggle(self):
        self.on = not self.on

    def draw(self, surface):
        if self.on:
            width = surface.get_width()
            height = surface.get_height()
            
            offset_x, offset_y = self.game.get_offsets()

            for x in range(0, width + GRID_SIZE, GRID_SIZE):
                adj_x = x - offset_x % GRID_SIZE
                pygame.draw.line(surface, self.color, [adj_x, 0], [adj_x, height], 1)

            for y in range(0, height + GRID_SIZE, GRID_SIZE):
                adj_y = y - offset_y % GRID_SIZE
                pygame.draw.line(surface, self.color, [0, adj_y], [width, adj_y], 1)

            for x in range(0, width + GRID_SIZE, GRID_SIZE):
                for y in range(0, height + GRID_SIZE, GRID_SIZE):
                    adj_x = x - offset_x % GRID_SIZE + 4
                    adj_y = y - offset_y % GRID_SIZE + 4
                    disp_x = x // GRID_SIZE + offset_x // GRID_SIZE
                    disp_y = y // GRID_SIZE + offset_y // GRID_SIZE
                    
                    point = f'({disp_x}, {disp_y})'
                    text = self.font.render(point, True, self.color)
                    surface.blit(text, [adj_x, adj_y])

class Editor:

    def __init__(self, game):
        self.game = game

    def show_grid(self):
        pass

    def save(self):
        pass


# old edit code from Game class
'''    def toggle_edit_mode(self):
        if self.stage == EDIT:
            self.stage = self.last_stage
            self.grid_on = False
        else:
            self.last_stage = self.stage
            self.grid_on = True
            self.stage = EDIT

    def show_edit_screen(self):
        tile_names = ['erase', 'block', 'grass']

        text = self.default_font.render(tile_names[self.tile_index], True, WHITE)
        rect = text.get_rect()
        rect.x = 16
        rect.bottom = HEIGHT - 16
        self.screen.blit(text, rect)
 
    def add_tile(self):
        x, y = pygame.mouse.get_pos()
        offset_x, offset_y = self.get_offsets()
        
        loc = [(x + offset_x) // GRID_SIZE, (y + offset_y) // GRID_SIZE]

        for tile in self.platforms:
            existing_tile_loc = [tile.rect.x // 64, tile.rect.y // 64]
            if existing_tile_loc == loc:
                tile.kill()
                if loc in self.data['blocks']:
                    self.data['blocks'].remove(loc)
                if loc in self.data['grass']:
                    self.data['grass'].remove(loc)

        if self.tile_index > 0:
            self.current_img = self.tile_images[self.tile_index]
            tile = Platform(self, self.current_img, loc)
            self.platforms.add(tile)
            self.all_sprites.add(tile) 

            if self.tile_index == 1:
                if not loc in self.data['blocks']:
                    self.data['blocks'].append(loc) 
            elif self.tile_index == 2:
                if not loc in self.data['grass']:
                    self.data['grass'].append(loc)

    def save(self):
        path = LEVELS[self.level - 1] # Remember zero indexing!
        print(path)
        
        with open(path, 'w') as f:
            json.dump(self.data, f) # messy way, but works for now

            # cleaner way (still not that nice)
            tab = '    '
            text = '{\n'
            text += tab + str(self.data['width']) + ',\n'
            text += tab + str(self.data['height']) + ',\n'
            text += tab + str(self.data['gravity']) + ',\n'
            text += tab + str(self.data['terminal_velocity']) + ',\n'
            text += tab + str(self.data['background']) + ',\n'
            text += tab + str(self.data['start']) + ',\n'
            text += tab + str(self.data['grass']) + ',\n'
            text += tab + str(self.data['blocks']) + ',\n'
            text += tab + str(self.data['gems']) + ',\n'
            text += tab + str(self.data['hearts']) + ',\n'
            text += tab + str(self.data['goals']) + ',\n'
            text += tab + str(self.data['spikeballs']) + ',\n'
            text += tab + str(self.data['clouds']) + ',\n'
            text += tab + str(self.data['spikemen']) + '\n'
            text += '}'

            #f.write(text) # I only wrote values, not keys above

        '''