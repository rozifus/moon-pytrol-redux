
import pygame
from pygame.transform import scale2x, scale
from pygame.image import load
from curve import Bezier

from settings import *

class Section:
    def __init__(self, function, rect):
        self.rect = rect
        self.surface = pygame.Surface(rect.size)
        self.surface.fill(COLOR['BG'])
        self.surface.lock()
        points = [(0,300), (200,175), (300,275), (600,300)]
        bez = Bezier(points)
        float_width = float(rect.width)
        self.heightmap = {} 
        self.slopemap = {}
        for x in range(rect.width):
            t = x/float_width
            bt = bez(t)
            self.heightmap[x] = int(bt[1])
            bts = bez.slope2(t)
            self.slopemap[x] = bts[1]/bts[0]
            self.surface.set_at((int(bt[0]), int(bt[1])), COLOR['PIXEL'])
        self.surface.unlock()


class Terrain:
    def __init__(self, section_data, rect):

        self.rect = rect
        self._sections = [] 
        for data in section_data:
          section = Section(*data)
          self._sections.append(section)
        # image map is list of [image_index, image_location]
        self._y = rect.top

    def y(self ,x):
        for section in self._sections:
            if section.rect.collidepoint((x,1)):
                return section.heightmap[x]

    def render(self, level, screen):
        screen.blit(self._sections[0].surface, (0-level.rect.x,0-level.rect.y))

    def slope(self, x):
        for section in self._sections:
            if section.rect.collidepoint((x,1)):
                return section.slopemap[x]
        

