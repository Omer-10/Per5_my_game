# This file was created by: Omer Sultan

import pygame as pg
from pygame.sprite import Sprite
from settings import *
from random import randint
import sys
import random

vec = pg.math.Vector2


# create the player class with a superclass of Sprite

from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        self.image = pg.Surface((32, 32))  # Size of the player
        self.image.fill((255, 0, 0))  # Color red for visibility
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Movement properties
        self.vx = 5  # Constant horizontal velocity
        self.vy = 0  # Vertical velocity
        self.jumping = False
        self.gravity = 0.5  # Gravity effect

    def update(self):
        self.handle_input()  # Handle player input
        self.apply_gravity()  # Apply gravity
        self.rect.x += self.vx  # Move the player sideways
        # Handle wall collisions
        self.collide_with_walls('x')
        # Apply vertical movement
        self.rect.y += self.vy
        # Handle vertical wall collisions
        self.collide_with_walls('y')

    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and not self.jumping:
            self.jump()

    def apply_gravity(self):
        if self.jumping:
            self.vy += self.gravity
            self.rect.y += self.vy

            if self.rect.bottom >= pg.display.get_surface().get_height():  # Prevent falling through ground
                self.rect.bottom = pg.display.get_surface().get_height()
                self.jumping = False
                self.vy = 0

    def jump(self):
        self.vy = -10  # Upward velocity
        self.jumping = True

    def collide_with_walls(self, axis):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        for wall in hits:
            if axis == 'x':
                if self.vx > 0:  # Moving right
                    self.rect.right = wall.rect.left  # Snap to the left side of the wall
                elif self.vx < 0:  # Moving left
                    self.rect.left = wall.rect.right  # Snap to the right side of the wall

            elif axis == 'y':
                if self.vy > 0:  # Falling down
                    self.rect.bottom = wall.rect.top  # Snap to the top of the wall
                    self.jumping = False  # Reset jump state
                    self.vy = 0  # Reset vertical velocity
                elif self.vy < 0:  # Moving up
                    self.rect.top = wall.rect.bottom  # Snap to the bottom of the wall

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
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
    

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

