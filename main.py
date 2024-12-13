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
https://stackoverflow.com/questions/61412616/i-do-not-know-how-to-end-game-when-specific-block-is-touched-in-pygame 
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



'''

# create a game class that carries all the properties of the game and methods
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Omer's Coolest Game Ever...")
        self.playing = True
        self.game_over = False  # Track game over state
        self.camera_x = 0  # Initialize the camera offset
    
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
            self.dt = self.clock.tick(FPS) / 1000  # Get the time
            self.events()  # Handle events

        if not self.game_over:
            self.all_sprites.update()  # This should correctly call update on each sprite including the Player
            self.draw()  # Draw the updated screen

    pg.quit()  

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
    def run(self):

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()

        if not self.game_over:
            self.update()

        else:
            self.display_game_over()  # May not be needed if quitting directly on spike hit
            self.draw()
            pg.quit()  

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False

# Chat gpt spike 
    def update(self):
        self.get_keys()  # Handle player movement
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        # Ensure the player stays within the screen bounds
        if self.rect.x > WIDTH:
            self.x = 0  # You may want to wrap the player back to the start

        elif self.rect.x < 0:
            self.x = WIDTH - TILESIZE  # Wrap to the other side if going off the left edge
            self.rect.x = self.x
            self.collide_with_walls('x')  # Handle wall collisions
            self.rect.y = self.y
            self.collide_with_walls('y')  # Handle vertical wall collisions
    
        # Check for collisions with coins and spikes
        self.collide_with_stuff(self.game.all_coins, True) 
        self.collide_with_stuff(self.game.all_spikes, False)

    def draw(self):
        self.screen.fill(BLACK)  # Clear the screen
        # Draw all sprites considering the camera offset
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y))
        ''' self.draw_text(self.screen, str(pg.time.get_ticks()), 24, WHITE, WIDTH/30, HEIGHT/30)
        self.draw_text(self.screen, "High Score: " + str(self.highscore), 24, BLACK, WIDTH/2, HEIGHT/24)
        self.draw_text(self.screen, "Current Score: " + str(self.score), 24, BLACK, WIDTH/2, HEIGHT/24)'''
        pg.display.flip()  # Update the display

# chat gpt: I asked for the spike to stop being weird by acting like a wall and told it to make it where ehn player touches the spike the game will end
def collide_with_stuff(self, group, kill):
    hits = pg.sprite.spritecollide(self, group, kill)
    if hits:
        if str(hits[0].__class__.__name__) == "Coin":
            self.coin_count += 1  # Increment the coin count when collecting a coin
            print("Collected a coin! Total coins:", self.coin_count)  

        elif str(hits[0].__class__.__name__) == "Spike":
            print("Game Over! You hit a spike!") 
            pg.quit()  # Quit the game if the player hits a spike

if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()

    #not moving forward after certain point in game
    #when jumping player would get stuck in ground or get flung back
    #hitting wall made player move backward
    #collide with spike wasnt working but i put in spike class instead of player