# this file was created by: Omer Sultan

# this is where we import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from sprites_side_scroller import *
from tilemap import *
from os import path
from random import randint
# we are editing this file after installing git

'''
Elevator pitch: I want to create a game that replicates the original Game Geometry Dash

GOALS: Sidescroller Parkour Game
RULES: You move forward avoiding spikes and collecting coins along the way until the end
FEEDBACK: Damage meter, powerup interactions 
FREEDOM: Only jump, Sidescrolling

What's the sentence: Avoid the obstacles to acheive Victory...

Alpha goal: to create a sidescroller setup, Spike collision, jump

'''

'''
Sources:
Spike - https://www.youtube.com/watch?v=atoGQ9o0ooI
Side Scroller - https://bcpsj-my.sharepoint.com/personal/ccozort_bcp_org/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fccozort%5Fbcp%5Forg%2FDocuments%2FDocuments%2F000%5FCS%5Fprinciples%2F2024%5F2025%5FFall%2Fclass%5Fcode%2Fside%5Fscroller
Collision Detection - https://www.geeksforgeeks.org/collision-detection-in-pygame/
https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection
Player Movement and Mechanics - https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-tutorial-movement
https://www.geeksforgeeks.org/how-to-move-your-game-character-around-in-pygame/
Screen Movement, Side Scroller - https://m.youtube.com/watch?v=u7LPRqrzry8&t=84s
https://m.youtube.com/watch?v=XmSv2V69Y7A&t=58s
https://www.geeksforgeeks.org/creating-a-scrolling-background-in-pygame/
https://www.tutorialspoint.com/pygame/pygame_using_camera_module.htm
https://www.tutorialspoint.com/pygame/pygame_moving_image.htm

Mr. Cozart vertical Side Scroller function where falling down ends game



'''

# create a game class that carries all the properties of the game and methods
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Geometry Dash")
        self.playing = True
        self.game_over = False  # Track game
        self.camera_x = 0  #  camera offset
        self.score = 0  # Initialize score (if needed)
        self.all_sprites = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
 

    def run(self):
        while self.playing:  # Main game loop
            self.handle_events()
            self.all_sprites.update()  # Call the update method for all sprites (including player)
            self.screen.fill((255, 255, 255))  # Fill the screen with white
            self.all_sprites.draw(self.screen)  # Draw all sprites
            pg.display.flip()  # Refresh the display
            self.clock.tick(60)  # Limit frame rate to 60 FPS

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        # with open(path.join(self.game_folder, HS_FILE), 'w') as f:
        #     f.write(str(0))
        '''try:
            with open(path.join(self.game_folder, HS_FILE), 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0
            with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                f.write(str(self.highscore))'''
            
        self.map = Map(path.join(self.game_folder, 'level1.txt'))  # Load the level data


    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_spikes = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':  # Wall
                    Wall(self, col, row)
                if tile == 'S':  # Spike
                    Spike(self, col, row)
                if tile == 'C':  # Coin
                    Coin(self, col, row)
                if tile == 'P':  # Player starting position
                    self.player = Player(self, col, row)

    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.game_over:
                self.update()

            else:
                self.display_game_over()  # Show game over screen
            self.draw()
        pg.quit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False

    def update(self):
        self.all_sprites.update()  # Update player and other sprites
        # Update camera x based on player's position to ensure smooth scrolling
        self.camera_x = self.player.rect.centerx - WIDTH // 2

    def draw(self):
        self.screen.fill(BLACK)  # Clear the screen
        # Draw all sprites considering the camera offset
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y))
        ''' self.draw_text(self.screen, str(pg.time.get_ticks()), 24, WHITE, WIDTH/30, HEIGHT/30)
        self.draw_text(self.screen, "High Score: " + str(self.highscore), 24, BLACK, WIDTH/2, HEIGHT/24)
        self.draw_text(self.screen, "Current Score: " + str(self.score), 24, BLACK, WIDTH/2, HEIGHT/24)'''
        pg.display.flip()  # Update the display

        # chat gpt, to create a way to count the coins and gave main.py
        self.draw_text(f'Coins: {self.player.coin_count}', 24, GOLD, WIDTH / 30, HEIGHT / 30)
        pg.display.flip()

    # chat gpt, to create a way to count the coins and gave main.py
    def draw_text(self, text, size, color, x, y):
        font = pg.font.SysFont('Arial', size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))  # Draw text at specified location


if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()

    #not moving forward after certain point in game
    #when jumping player would get stuck in ground or get flung back
    #hitting wall made player move backward
    #collide with spike wasnt working but i put in spike class instead of player