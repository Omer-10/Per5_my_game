# This file was created by: Omer Sultan
import pygame as pg
from pygame.sprite import Sprite
from settings import *
import random

coinct = 0

vec = pg.math.Vector2

class Player(Sprite):
    # this initializes the properties of the player class including the x y location, and the game parameter so that the the player can interact logically with
    # other elements in the game...
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        self.image = self.standing_image
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 20
        self.coin_count = coinct

    def load_images(self):
        self.standing_image = self.spritesheet.get_image(0,0,32,32)

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.vy -= self.speed
            # print(self.vy)
        if keys[pg.K_a]:
            self.vx -= self.speed
        if keys[pg.K_s]:
            self.vy += self.speed
        if keys[pg.K_d]:
            self.vx += self.speed
        if keys[pg.K_r]:
            self.x = WIDTH/2
            self.y = HEIGHT/2
            print("respawn")

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - TILESIZE
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - TILESIZE
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
                # print("Collided on x axis")
        #     else:
        #         print("not working...for hits")
        # # else:
        #     print("not working for dir check")

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        global coinct
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                self.speed += 20
                # print("I've gotten a powerup!")
            if str(hits[0].__class__.__name__) == "Coin":
                print("I got a coin!!!")
                self.coin_count += 1
                coinct += 1
            # if str(hits[0].__class__.__name__) == "Portal":
            #     self.game.load_level("level2.txt")

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt

        if self.rect.x > WIDTH:
            self.x = 0
        elif self.rect.x < 0:
            self.x = WIDTH - TILESIZE

        self.rect.x = self.x
        self.collide_with_walls('x')

        self.rect.y = self.y
        self.collide_with_walls('y')

        self.collect_coins()
        
        # teleport the player to the other side of the screen
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_portals, False)

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.image.load(self.game.brick_img)
        # self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        # self.image.fill(BLUE)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(GOLD)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Spike(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE