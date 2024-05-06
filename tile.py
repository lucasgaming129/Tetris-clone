from settings import *

class Tile:
    def __init__(self, app, color, pos):
        self.app = app
        self.screen = app.screen

        self.pos = pos

        self.color = color

        self.sprite_name = f'assets/sprites/tile_{color}.png'
        self.sprite = pg.transform.scale(pg.image.load(self.sprite_name), (tile_size, tile_size))

    def draw(self):
        tile_x = self.pos.x * tile_size
        tile_y = self.pos.y * tile_size

        self.screen.blit(self.sprite, (tile_x, -tile_y + (tile_size*(grid_height-1))))
        