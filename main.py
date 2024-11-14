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
Elevator pitch: I want to create a game that follows an apprentice mage from the bottom of a tower to the top, leveling up as he climbs to the top to defeat the evil wizard...

GOALS: Sidescroller Parkour Game
RULES: You move forward avoiding spikes and collecting coins along the way until the end
FEEDBACK: Damage meter, powerup interactions 
FREEDOM: Only jump, Sidescrolling

What's the sentence: Avoid the obstacles to acheive Victory...

Alpha goal: to create a sidescroller setup, Spike collision, jump

'''

'''
Sources:
https://www.youtube.com/watch?v=atoGQ9o0ooI - Spike
https://bcpsj-my.sharepoint.com/personal/ccozort_bcp_org/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fccozort%5Fbcp%5Forg%2FDocuments%2FDocuments%2F000%5FCS%5Fprinciples%2F2024%5F2025%5FFall%2Fclass%5Fcode%2Fside%5Fscroller - Sidescroller

'''

# create a game class that carries all the properties of the game and methods
class Game:
  # initializes all the things we need to run the game...includes the game clock which can set the FPS
  def __init__(self):
    pg.init()
    # sound mixer...
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Omer's Coolest Game Ever...")
    self.playing = True
  # this is where the game creates the stuff you see and hear
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.map = Map(path.join(self.game_folder, 'level1.txt'))
  def new(self):
    self.load_data()
    print(self.map.data)
    # create the all sprites group to allow for batch updates and draw methods
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_spikes = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    for row, tiles in enumerate(self.map.data):
      print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'S':
          Spike(self, col, row)
        if tile == 'C':
          Coin(self, col, row)
        if tile == 'M':
          Mob(self, col, row)

        

# this is a method
# methods are like functions that are part of a class
# the run method runs the game loop
  def run(self):
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      # input
      self.events()
      # process
      self.update()
      # output
      self.draw()

    pg.quit()
  # input
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  # process
  # this is where the game updates the game state
  def update(self):
    # update all the sprites...and I MEAN ALL OF THEM
    self.all_sprites.update()
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

  # output
  def draw(self):
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    pg.display.flip()

  def update(self):
    self.all_sprites.update()
        # output
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

  def draw(self):
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    self.draw_text(self.screen, str(pg.time.get_ticks()), 24, BLACK, WIDTH/30, HEIGHT/30)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate
  print("main is running...")
  g = Game()
  print("main is running...")
  g.new()
  g.run()
  