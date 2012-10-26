import sys
import time
import math
import random
import textwrap

import pygame
from pygame.locals import *
from pygame.transform import scale2x, scale
from pygame.image import load

from data import filepath
from terrain import Terrain
from car import Car
import settings


import curve


def offscreen(x, y):
    maxx, maxy = settings.DISPLAY_SIZE
    return x > maxx or x < 0 or y > maxy or y < 0

class Level:
    def __init__(self, config):
        self.surface = pygame.Surface(settings.DISPLAY_SIZE)
        self.rect = Rect((0,0), settings.DISPLAY_SIZE)
        self._x = 0
        self._y = 0

        self.terrain = Terrain([(None, Rect(0,0,600,300))], Rect(0,0,300,300))
        self.spritegroups = {} 
        self.spritegroups['player'] = pygame.sprite.Group()
        self.car = Car(self, self.spritegroups['player'])
        self.car._xspeed = 1

    def update(self):
        self.car._yspeed += 1 
        self.car._xspeed += 0.01
        self.spritegroups['player'].update()
        car_terrain_y = self.terrain.y(self.car.rect.bottomright[0])
        self.car.rotation = self.terrain.slope(self.car.rect.midbottom[0])
        if self.car.rect.bottom > car_terrain_y:
            self.car._yspeed = 0
            self.car.rect.bottom = car_terrain_y

    def render(self, screen):
        self.terrain.render(self, screen)
        self.spritegroups['player'].draw(screen)

    
