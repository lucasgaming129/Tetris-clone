import pygame as pg
import glm

colors = [
    'blue',
    'green',
    'orange',
    'purple',
    'red',
    'yellow'
]

types = dict(
    o = dict(rotations = [[(0, 1), (-1, 1), (-1, 2), (0, 2)]], color = 'yellow'),
    i = dict(rotations = [[(0, 0), (0, 1), (0, 2), (0, -1)], [(0, 0), (-1, 0), (-2, 0), (1, 0)]], color = 'light_blue'),
    s = dict(rotations = [[(0, 0), (0, 1), (-1, 1), (-1, 2)], [(-1, 0), (-2, 0), (-1, 1), (0, 1)]], color = 'green'),
    z = dict(rotations = [[(-1, 0), (-1, 1), (0, 1), (0, 2)], [(0, 0), (1, 0), (0, 1), (-1, 1)]], color = 'red'),
    j = dict(rotations = [[(0, 0), (-1, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (-1, 0), (-1, 1)], [(0, 2), (-1, 0), (-1, 1), (-1, 2)], [(0, 1), (1, 1), (-1, 1), (1, 0)]], color = 'blue'),
    l = dict(rotations = [[(0, 0), (-1, 0), (-1, 1), (-1, 2)], [(-1, 0), (-1, 1), (0, 1), (1, 1)], [(-1, 2), (0, 0), (0, 1), (0, 2)], [(1, 1), (-1, 0), (0, 0), (1, 0)]], color = 'orange'),
    t = dict(rotations = [[(-1, 1), (-2, 1), (-1, 2), (0, 1)], [(-1, 0), (-1, 1), (-1, 2), (0, 1)], [(-1, 0), (-1, 1), (-2, 1), (0, 1)], [(-1, 0), (-1, 1), (-2, 1), (-1, 2)]], color = 'purple')
)

type_names = list(types.keys())

text_size = 100
title_size = 110
caption_size = 50

tile_size = 60
grid_width, grid_height = grid_size = (10, 20)

info_size = 10
info_width = tile_size*info_size

screen_width, screen_height = screen_res = ((grid_width*tile_size + info_width), (grid_height*tile_size))

fps = 144

normal_drop_rate = fps // 2
soft_drop_rate = fps // 10