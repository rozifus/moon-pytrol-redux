
import pygame
import math
from settings import *


def drawWheel(target):
    rect = target.get_rect()
    target.set_colorkey(COLOR['TCK'])
    target.fill(COLOR['TCK'])
    pygame.draw.circle(target, 
                       COLOR['BG'], 
                       rect.center,
                       rect.centerx )
    pygame.draw.circle(target,
                       COLOR['CAR'],
                       rect.center,
                       rect.centerx,
                       1 )
    pygame.draw.circle(target,
                       COLOR['CAR'],
                       rect.center,
                       rect.centerx / 4 )


def drawCar(target):
    rect = target.get_rect()
    target.set_colorkey(COLOR['TCK'])
    target.fill(COLOR['TCK'])
    x10 = rect.w / 10
    y10 = rect.h / 10
    pygame.draw.lines(target, COLOR['CAR'], True, 
            [ (x10, 9*y10), (10*x10, 9*y10), (9*x10, 7*y10),
              (7*x10, 6*y10), (5*x10, 4*y10), (1*x10, 4*y10),

            
            ] 
    )

class Wheel(pygame.sprite.Sprite):
    def __init__(self, **config):
        """
        Config: 
            car {object}
            rel {rect}
        """
        super(Wheel, self).__init__()
        self.car = config['car']
        # rel is pinned via center, rect is not
        self.rel = config['rel'] 
        assert(self.rel.w % 2 == self.rel.h % 2 == 0)
        self.rect = pygame.Rect(self.rel)
        self.image_base = pygame.Surface(self.rel.size)
        drawWheel(self.image_base)
        self.image = self.image_base.copy()

    def update(self):
        self.rect = self.rel.move(self.car.rect.topleft)
        self.rect.move_ip(-self.rel.w/2, -self.rel.h/2)

class Car(pygame.sprite.Sprite):

    def __init__(self, level, *groups):
        super(Car, self).__init__(*groups)
        self.front = Wheel(car=self, rel=pygame.Rect((30,20), (10,10)))
        self.rear = Wheel(car=self, rel=pygame.Rect((0,20), (10,10)))
        self.level = level
        self._speed = 0
        self.rotation = 0
        self.rect = pygame.Rect((0,200), (40,30))
        self.image_base = pygame.Surface(self.rect.size)
        drawCar(self.image_base)
        self.image = self.image_base.copy()
        self._xspeed = 0 
        self._yspeed = 0
        self._jumping = False

    def change_speed(self, direction):
        self._xspeed += direction * settings.BUGGY_SPEED
        self._xspeed = max(self._xspeed, -settings.BUGGY_SPEED)
        self._xspeed = min(self._xspeed, settings.BUGGY_SPEED)

    def jump(self, force):
        if not self._jumping:
            self._yspeed = -force
            self._jumping = True

    def update(self):
        drawCar(self.image_base)
        self.image_base.blit(self.front.image, self.front.rel)
        self.image_base.blit(self.rear.image, self.rear.rel)
        self.rect.move_ip(self._xspeed, self._yspeed)
        rot = -self.rotation * 180 / math.pi
        self.image = pygame.transform.rotate(self.image_base, rot)
        self.image.get_rect().center = self.image_base.get_rect().center

