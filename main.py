import numpy as np #np.array([1, 0, 1], dtype=bool)

from settings import *

from tetromino import Tetromino
from tile import Tile

class Game:
    def load_sound(self, file_name):
        return pg.mixer.Sound(f'assets/sounds/{file_name}')

    def create_fonts(self):
        pg.font.init()

        self.font = pg.font.Font('assets/font/game_font.ttf', text_size)
        self.title_font = pg.font.Font('assets/font/game_font.ttf', title_size)
        self.caption_font = pg.font.Font('assets/font/game_font.ttf', caption_size)

        self.score_text = self.font.render('SCORE: ' + str(self.score), True, 'white')
        self.line_text = self.font.render('LINES: ' + str(self.lines), True, 'white')
        self.high_text = self.title_font.render('HIGH', True, 'white')
        self.high2_text = self.title_font.render('SCORE: ' + str(self.high_score), True, 'white')

        self.game_over_text = self.font.render('GAME OVER', True, 'white')
        self.end_score_text = self.caption_font.render(f'SCORE: 0!', True, 'white')

    def create_sounds(self):
        pg.mixer.init()

        self.tetris_theme = pg.mixer.music.load('assets/sounds/soundtrack.mp3')

        self.tetris_sound = self.load_sound('tetris.mp3')
        self.clear_sound = self.load_sound('clear.mp3')
        self.game_over_sound = self.load_sound('game_over.mp3')

        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)

    def setup_pygame(self):
        self.screen = pg.display.set_mode(screen_res)

        self.clock = pg.time.Clock()
        self.time = 0
    
    def get_highscore(self):
        with open('assets/hs.txt', 'r') as highscore:
            score = highscore.read()
            return int(score)

    def __init__(self):
        pg.init()

        self.setup_pygame()

        self.current_bag = type_names.copy()

        self.background_tiles = []
        self.side_tiles = []
        self.locked_tiles = []

        self.current_tetromino = Tetromino(self, glm.vec2(grid_width // 2, grid_height-3))

        self.last_dir = 0
        self.current_drop_rate = 30

        self.high_score = self.get_highscore()
        self.score = 0
        self.lines = 0

        self.create_sounds()
        self.create_fonts()

        for x in range(grid_width):
            for y in range(grid_height):
                self.background_tiles.append(Tile(self, 'black2', glm.vec2(x, y)))
        
        for y in range(grid_height):
            self.side_tiles.append(Tile(self, 'bg', glm.vec2(grid_width, y)))

    def game_over(self):
        self.is_running = False

        if self.score > self.high_score:
            self.high_score = self.score

            with open('assets/hs.txt', 'w') as highscore:
                highscore.write(str(self.high_score))
                highscore.close()
            
            self.end_score_text = self.caption_font.render(f'NEW HIGH SCORE: {self.score}!', True, 'white')
        else:
            self.end_score_text = self.caption_font.render(f'SCORE: {self.score}!', True, 'white')
        
        self.screen.blit(self.game_over_text, (screen_width/2 - self.game_over_text.get_width()/2, screen_height/2 - self.game_over_text.get_height()/2))
        self.screen.blit(self.end_score_text, (screen_width/2 - self.end_score_text.get_width()/2, screen_height/2 - self.end_score_text.get_height()/2 + 50))

        pg.display.update()

        pg.mixer.music.pause()
        self.game_over_sound.play()
        pg.time.wait(5000)

        new_game = Game()
        new_game.run()
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
                self.leave = True
            if event.type == pg.KEYDOWN:
                self.check_input(event.key)

    def check_input(self, input):
        if input == pg.K_LEFT:
            self.current_tetromino.move(1)
        if input == pg.K_RIGHT:
            self.current_tetromino.move(2)
        if input == pg.K_SPACE:
            is_collide = False
            while is_collide == False and self.current_tetromino:
                if self.current_tetromino.check_collision(3):
                    self.current_tetromino.move(3)
                else:
                    is_collide = True
            self.current_tetromino.move(3)
        if input == pg.K_UP:
            self.current_tetromino.rotate()
    
    def key_press(self):
        keys_pressed = pg.key.get_pressed()
        
        if keys_pressed[pg.K_DOWN]:
            self.current_drop_rate = soft_drop_rate
        else:
            self.current_drop_rate = normal_drop_rate

    def draw(self):
        if self.is_running:
            self.screen.fill((40, 40, 40))

            # draw background
            for tile in self.background_tiles:
                tile.draw()
            
            # draw locked tiles
            for tile in self.locked_tiles:
                tile.draw()

            # draw side tiles
            for tile in self.side_tiles:
                tile.draw()

            # draw score and lines
            self.screen.blit(self.high_text, (grid_width*tile_size + tile_size + info_width/2 - (self.high_text.get_width()/2) - 20, 10))
            self.screen.blit(self.high2_text, (grid_width*tile_size + tile_size + info_width/2 - (self.high2_text.get_width()/2) - 20, 100))

            self.screen.blit(self.score_text, (grid_width*tile_size + tile_size + info_width/2 - (self.score_text.get_width()/2), 220))
            self.screen.blit(self.line_text, (grid_width*tile_size + tile_size + info_width/2 - (self.line_text.get_width()/2), 380))
            
            self.current_tetromino.draw()

            pg.display.update()
    
    def read_line(self, y):
        tiles = 0
        for x in range(grid_width):
            for tile in self.locked_tiles:
                if tile.pos == glm.vec2(x, y):
                    tiles += 1
            if tiles == grid_width:
                new_tiles = []
                for tile in self.locked_tiles:
                    if not tile.pos == glm.vec2(tile.pos.x, y):
                        if tile.pos.y > y:
                            tile.pos.y -= 1
                        new_tiles.append(tile)
                self.locked_tiles = new_tiles
 
                return True
        return False
    
    def check_lines(self):
        cleared_lines = 0
        for y in range(grid_height):
            if self.read_line(y):
                cleared_lines += 1 
                if self.read_line(y):
                    cleared_lines += 1
                    if self.read_line(y):
                        cleared_lines += 1 
                        if self.read_line(y):
                            cleared_lines += 1 
            
        score = 0
        if cleared_lines == 1:
            self.clear_sound.play()
            score = 100
        if cleared_lines == 2:
            score = 300
            self.clear_sound.play()
        if cleared_lines == 3:
            score = 500
            self.clear_sound.play()
        if cleared_lines == 4:
            score = 800
            self.tetris_sound.play()
        
        self.score += score
        self.score_text = self.font.render('SCORE: ' + str(self.score), True, 'white')
        
        self.lines += cleared_lines
        self.line_text = self.font.render('LINES: ' + str(self.lines), True, 'white')
    
    def update(self):
        self.clock.tick(fps)
        self.time += 1

        self.key_press()
        
        if self.time/self.current_drop_rate == round(self.time/self.current_drop_rate):
            if self.current_tetromino.is_drop:
                self.current_tetromino.move(3)
            else:
                self.check_lines()
                new_tetromino = Tetromino(self, glm.vec2(grid_width // 2, grid_height-3))
                self.current_tetromino = new_tetromino

        pg.display.set_caption(str(self.clock.get_fps()))
    
    def run(self):
        self.leave = False
        self.is_running = True
        while self.is_running:
            self.check_events()
            self.update()
            self.draw()
        
        if self.leave:
            pg.quit()


if __name__ == '__main__':
    game = Game()
    game.run()