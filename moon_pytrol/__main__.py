import sys
import time
import random
import textwrap

import pygame
from pygame.transform import scale2x, scale
from pygame.image import load

from data import filepath
from level import Level
import settings

def offscreen(x, y):
    maxx, maxy = settings.DISPLAY_SIZE
    return x > maxx or x < 0 or y > maxy or y < 0

def main():
    """ your app starts here
    """
    pygame.init()

    screen = pygame.display.set_mode(settings.DISPLAY_SIZE)

    gs = game(screen)

def game(screen):

    clock = pygame.time.Clock()

    level = Level(None)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.QUIT or event.key==pygame.K_q: 
                    pygame.quit()
                    sys.exit()

        screen.fill((0,0,0))
        level.update()
        level.render(screen)

        pygame.display.flip()

        # purge events
        pygame.event.get()

        clock.tick(60)

    return gs

