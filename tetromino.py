from random import choice

from settings import *

from tile import Tile

class Tetromino:
    def game_over_check(self):
        for tile in self.tiles:
            for locked_tile in self.app.locked_tiles:
                if tile.pos == locked_tile.pos:
                    self.draw()
                    pg.display.update()
                    self.app.game_over()
                    return False
        return True

    def __init__(self, app, pos):
        self.app = app
        self.pos = pos
        self.rot = 0

        if len(app.current_bag) == 0:
            app.current_bag = type_names.copy()

        self.type_name = choice(app.current_bag)
        app.current_bag.remove(self.type_name)

        self.type = types[self.type_name]

        self.color = self.type['color']

        # create tiles
        self.tiles = []
        for tile_pos in self.type['rotations'][0]:
            new_tile = Tile(app, self.color, glm.vec2(tile_pos[0] + self.pos.x, tile_pos[1] + self.pos.y))
            self.tiles.append(new_tile)
        
        self.game_over_check()
        
        self.is_drop = True
    
    def rotate(self):
        new_rot = self.rot + 1
        
        if new_rot + 1 > len(self.type['rotations']):
            new_rot = 0

        if self.check_rotation_collision(new_rot):
            new_positions = self.type['rotations'][new_rot]

            self.tiles = []
            for tile_pos in self.type['rotations'][new_rot]:
                new_tile = Tile(self.app, self.color, glm.vec2(tile_pos[0] + self.pos.x, tile_pos[1] + self.pos.y))
                self.tiles.append(new_tile)
            self.rot = new_rot
    
    def check_rotation_collision(self, new_rotation):
        tiles = self.type['rotations'][new_rotation]

        for tile in tiles:
            t_pos = glm.vec2(tile[0] + self.pos.x, tile[1] + self.pos.y)
            if t_pos.x > (grid_width - 1) or t_pos.x < 0 or t_pos.y < 0:
                return False
            for locked_tile in self.app.locked_tiles:
                if locked_tile.pos == t_pos:
                    return False
        return True
    
    def check_collision(self, dir):
        if dir == 1:
            for tile in self.tiles:
                moved_pos = glm.vec2(tile.pos.x - 1, tile.pos.y)
                if moved_pos.x < 0:
                    return False
                for locked_tile in self.app.locked_tiles:
                    if locked_tile.pos == moved_pos:
                        return False 
        if dir == 2:
            for tile in self.tiles:
                moved_pos = glm.vec2(tile.pos.x + 1, tile.pos.y)
                if moved_pos.x > (grid_width - 1):
                    return False
                for locked_tile in self.app.locked_tiles:
                    if locked_tile.pos == moved_pos:
                        return False 
        if dir == 3:
            for tile in self.tiles:
                moved_pos = glm.vec2(tile.pos.x, tile.pos.y - 1)
                if moved_pos.y < 0:
                    return False
                for locked_tile in self.app.locked_tiles:
                    if locked_tile.pos == moved_pos:
                        return False 
        return True
    
    def move(self, dir):
        # 1: left, 2: right, 3: down
        if dir == 1 and self.check_collision(1):
            for tile in self.tiles:
                tile.pos.x -= 1
            self.pos.x -= 1
        if dir == 2 and self.check_collision(2):
            for tile in self.tiles:
                tile.pos.x += 1
            self.pos.x += 1
        if dir == 3:
            is_collide = self.check_collision(3)
            if is_collide:
                for tile in self.tiles:
                    tile.pos.y -= 1
                self.pos.y -= 1
            else:
                for tile in self.tiles:
                    self.app.locked_tiles.append(tile)
                self.is_drop = False
                
    
    def draw(self):
        for tile in self.tiles:
            tile.draw()