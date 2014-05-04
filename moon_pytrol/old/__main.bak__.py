import sys
import time
import random
import textwrap

import pygame
from pygame.transform import scale2x, scale
from pygame.image import load

from data import filepath
from background import Background
import settings

JUMP = getattr(pygame, settings.JUMP)
SPEEDUP = getattr(pygame, settings.SPEEDUP)
SLOWDOWN = getattr(pygame, settings.SLOWDOWN)
QUIT = getattr(pygame, settings.QUIT)

def offscreen(x, y):
    maxx, maxy = settings.DISPLAY_SIZE
    return x > maxx or x < 0 or y > maxy or y < 0

def checkendgame(gs):
    return gs.lives == 0 or gs.finished()

def startgame(screen):
    """
    Tell user about game. Show the keys.
    """
    pygame.mixer.music.load(filepath('pink-delta_hiscore.mod'))
    pygame.mixer.music.play()

    _starfield = pygame.transform.scale(load(filepath('starfield.png')),
                                        (settings.DISPLAY_SIZE)).convert()
    screen.blit(_starfield, (0, 0))
    font = pygame.font.Font(filepath('amiga4ever.ttf'), 16)

    textsurf = pygame.Surface(settings.DISPLAY_SIZE)
    name = pygame.key.name
    msg = textwrap.dedent("""
    Moon Pytrol
    Press %(left)s to slow down
    Press %(right)s to speed up
    Press %(jump)s to jump AND shoot.

    Avoid the craters, rocks and bombs.
    """) % dict(
        left=name(SLOWDOWN).upper(),
        right=name(SPEEDUP).upper(),
        jump=name(JUMP).upper())

    lines = msg.split('\n')

    blitlines = map(lambda m: font.render(m, False, settings.HUD_TEXT), lines)
    for i, line in enumerate(blitlines):
        textsurf.blit(line, (100, i*50 + 50))
    textsurf.set_colorkey(settings.BLACK)
    screen.blit(textsurf, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    s_to_start = font.render('Press %s to start' % name(JUMP).upper(),
                             False, settings.HUD_TEXT)
    t = time.time()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == QUIT: sys.exit()
                if event.key == pygame.K_q: sys.exit()
                if event.key == JUMP:
                    return True

        clock.tick(60)
        screen.blit(_starfield, (0, 0))
        screen.blit(textsurf, (0, 0))
        if int(time.time() - t) % 2:
            screen.blit(s_to_start, (100, 450))
        pygame.display.flip()


def congrats(screen, gs):
    _starfield = pygame.transform.scale(load(filepath('starfield.png')),
                                        (settings.DISPLAY_SIZE)).convert()
    screen.blit(_starfield, (0, 0))

    font = pygame.font.Font(filepath('amiga4ever.ttf'), 16)
    msg = font.render('CONGRATULATIONS', 
                      False, settings.HUD_TEXT)
    msg2 = font.render('You succeeded where thousands', 
                      False, settings.HUD_TEXT)
    msg2a = font.render('before you failed', 
                      False, settings.HUD_TEXT)
    msg3 = font.render('Press R to restart or Q to quit', 
                      False, settings.HUD_TEXT)
    screen.blit(msg, (50, 100))
    screen.blit(msg2, (50, 150))
    screen.blit(msg2a, (50, 180))
    screen.blit(msg3, (50, 250))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == QUIT: sys.exit()
                if event.key == pygame.K_q: sys.exit()
                if event.key == pygame.K_r:
                    # restart the game.
                    return True

def endgame(screen, gs):
    _starfield = pygame.transform.scale(load(filepath('starfield.png')),
                                        (settings.DISPLAY_SIZE)).convert()
    screen.blit(_starfield, (0, 0))

    font = pygame.font.Font(filepath('amiga4ever.ttf'), 16)
    msg = font.render('So.. looks like its all over then..', 
                      False, settings.HUD_TEXT)
    rstart = font.render('press R to restart', 
                      False, settings.HUD_TEXT)
    screen.blit(msg, (100, 200))
    screen.blit(rstart, (100, 300))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == QUIT: sys.exit()
                if event.key == pygame.K_q: sys.exit()
                if event.key == pygame.K_r:
                    # restart the game.
                    return True

def nearborder(entity, dist, rect=None):
    # returns bool list for near [up, right, down, left]
    near = [False] * 4
    entity_size = entity._image.get_size()
    if rect == None: 
        rect = pygame.Rect(0,0,settings.DISPLAY_SIZE[0],
                               settings.DISPLAY_SIZE[1])
    if entity.rect.right + dist > rect.right:
        near[1] = True
    if entity.rect.x - dist < rect.x:
        near[3] = True
    if entity.rect.bottom + dist > rect.bottom:
        near[2] = True
    if entity.rect.y - dist < rect.y:
        near[0] = True
    return near

def makepothole(*groups):
    if not random.randint(0, 500):
        placepothole(settings.DISPLAY_SIZE[0], *groups)

def placepothole(x, *groups):
    Pothole(x, *groups)

class GameState(object):

    def __init__(self):
        self._initialtime = time.time()
        self.time = 0
        self.points = 0
        self.lives = 3
        self._distance = 0
        self.atmoonbase = False

    def update(self):
        self.time = (time.time() - self._initialtime)

    @property
    def distance(self):
        return self._distance / 100

    def nearmoonbase(self):
        return self.distance >= settings.FINISH_DISTANCE

    def finished(self):
        #return self.distance >= settings.FINISH_DISTANCE
        return self.atmoonbase
    
    def incdist(self):
        self._distance += 1

    def incpoint(self):
        self.points += 1

def makebomb(x, y, *groups):
    if not random.randint(0, settings.UFO_BOMB_CHANCE):
        bomb = Bomb(x, y, *groups)
        bomb._sounds['drop'].play()

def makeenemy(enemies):
    if not random.randint(0, 50):
        width, height = settings.DISPLAY_SIZE
        ufo = Ufo(random.randint(50, 200), 100,
                  pygame.Rect(0,0, width, height - 300),
                  enemies)

def makerock(*groups):
    if not random.randint(0, 50):
        Rock(*groups)

def carefulcollide(left, right):
    if isinstance(right, Car):
        left, right = right, left

    if isinstance(right, Pothole):
        x, y = right.rect.midtop
        return left.rect.contains(pygame.Rect(x, y, 1, 1))
    else:
        return pygame.sprite.collide_mask(left, right)

def makehud(time, points, lives, distance):
    surf = pygame.Surface((450, 90))
    surf.fill((200, 114, 53))
    font = makehud.font
    time = font.render('TIME\t%d' % int(time), False, settings.HUD_TEXT)
    points = font.render('POINT\t%d' % int(points), False, settings.HUD_TEXT)
    lives = font.render('LIVES\t%d' % int(lives), False, settings.HUD_TEXT)
    distance = font.render('DIST\t%s' % ('|'*distance), False, settings.HUD_TEXT)
    surf.blit(time, (5, 10))
    surf.blit(points, (5, 40))
    surf.blit(lives, (5, 70))
    surf.blit(distance, (150, 40))
    return surf

def main():
    """ your app starts here
    """
    pygame.init()

    screen = pygame.display.set_mode(settings.DISPLAY_SIZE)

    while 1:
        startgame(screen)
        gs = game(screen)
        pygame.mixer.music.load(filepath('pink-hawkeye_hiscore.mod'))
        pygame.mixer.music.play(-1)
        if not gs.finished():
            endgame(screen, gs)
        else:
            congrats(screen, gs)

def render_star(screen, back):
    back.render(screen)

def render_terrain(screen, back):
    back.render(screen)

def render_midground(screen, back):
    back.render(screen)

def render_background(screen, back):
    back.render(screen)

def crop(surface, rect):
    newsurf = pygame.Surface(rect.size)
    newsurf.set_colorkey(settings.BLACK)
    newsurf.blit(surface, (0,0))
    return newsurf

def game(screen):
    _starfield = pygame.transform.scale(load(filepath('starfield.png')),
                                        (settings.DISPLAY_SIZE)).convert()
    _bground = load(filepath('mountains2.png')).convert_alpha()
    _terrain00 = scale2x(load(filepath('terrain00.png'))).convert_alpha()
    _terrain01 = scale2x(load(filepath('terrain01.png'))).convert_alpha()
    _midground = scale2x(load(filepath('mountains00.png'))).convert_alpha()
    _car0 = scale2x(load(filepath('buggy00.png'))).convert_alpha()
    _car1 = scale2x(load(filepath('buggy01.png'))).convert_alpha()
    _car2 = scale2x(load(filepath('buggy02.png'))).convert_alpha()
    _car3 = scale2x(load(filepath('buggy03.png'))).convert_alpha()


    allsprites = pygame.sprite.Group()
    car = Car([_car0, _car1, _car2, _car3], settings.GROUND_HEIGHT, allsprites)
    bground = pygame.transform.scale(_bground, settings.DISPLAY_SIZE)
    moonbase = None

    MAXX, MAXY = settings.DISPLAY_SIZE
    GHEIGHT = settings.GROUND_HEIGHT

    _largeterrain = pygame.Surface((MAXX, GHEIGHT))
    _largeterrain.set_colorkey(settings.BLACK)
    _terrains = [_terrain00, _terrain01]
    width = 0
    for i in range(10):
        _largeterrain.blit(_terrains[0], (width, 0))
        width += _terrains[0].get_size()[0]
        _terrains.reverse()

    starfield = Background(_starfield,
                    pygame.Rect(0, 0, MAXX, GHEIGHT-10), 0)
    background = Background(crop(bground,
                                 pygame.Rect(0, 0, MAXX, GHEIGHT-100+5)),
                    pygame.Rect(0, 100, MAXX, GHEIGHT-100+5),
                    settings.SCROLL_SPEED)
    
    ground = Background(crop(_largeterrain,
                             pygame.Rect(0, 0, MAXX, MAXY-GHEIGHT)),
                        pygame.Rect(0, GHEIGHT, MAXX, MAXY-GHEIGHT),
                        settings.GROUND_SPEED)
    midground = Background(crop(_midground,
                                pygame.Rect(0, 0, MAXX, GHEIGHT-200+5)),
                        pygame.Rect(0, 200, MAXX, GHEIGHT-200+5),
                        settings.SCROLL_SPEED + 1)

    clock = pygame.time.Clock()

    # groups
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    badthings = pygame.sprite.Group()
    ufos = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    potholes = pygame.sprite.Group()
    moonbases = pygame.sprite.Group()
    bgrounds = [starfield, background, midground, ground]

    _font = pygame.font.Font(filepath('amiga4ever.ttf'), 16)
    makehud.font = _font

    gs = GameState()

    pygame.mixer.music.load(filepath('pink-summertime.mod'))
    pygame.mixer.music.play(-1)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == QUIT or event.key==pygame.K_q: sys.exit()
                if event.key == SPEEDUP: car.change_speed(1)
                if event.key == SLOWDOWN: car.change_speed(-1)
                if event.key == JUMP: 
                    car.jump()
                    rect = car.rect
                    Bullet(rect.left+5, rect.top, 0, 10, bullets)
                    Bullet(rect.right-10, rect.centery-5, 10, 0, bullets)
                if event.key == pygame.K_p:
                    import pdb;pdb.set_trace()

        clock.tick(60)

        makeenemy(enemies)

        if gs.nearmoonbase():
            if not moonbase:
                moonbase = Moonbase(settings.DISPLAY_SIZE[0], moonbases)

        # only if there is below a certain threshold on screen.
        badstuff = sum(map(len, [potholes, rocks, bombs]))
        if badstuff < settings.MAX_BAD_STUFF:
            makepothole(potholes, badthings)
            makerock(rocks, badthings)

        for ufo in enemies:
            badstuff = sum(map(len, [potholes, rocks, bombs]))
            if badstuff < settings.MAX_BAD_STUFF:
                makebomb(
                    ufo.rect.centerx,
                    ufo.rect.bottom,
                    bombs, badthings)

        # blit first bit.
        render_star(screen, bgrounds[0])
        render_background(screen, bgrounds[1])
        render_midground(screen, bgrounds[2])
        render_terrain(screen, bgrounds[3])
        #[b.render(screen) for b in bgrounds]

        gs.update();gs.incdist()
        enemies.update()
        potholes.update()
        bombs.update()
        allsprites.update()
        bullets.update()
        rocks.update()
        moonbases.update()

        allsprites.draw(screen)
        enemies.draw(screen)
        bullets.draw(screen)
        potholes.draw(screen)
        bombs.draw(screen)
        rocks.draw(screen)
        moonbases.draw(screen)


        if moonbase:
            ratio_collide = pygame.sprite.collide_rect_ratio(0.9)
            if ratio_collide(moonbase, car):
                gs.atmoonbase = True


        # check player dead conditions.
        collided = pygame.sprite.spritecollide(car, badthings, False)
        if collided:
            # ok player collided with a bad thing should be dead... but 
            reallyhit = pygame.sprite.spritecollide(
                            car, collided, False, carefulcollide)
            if reallyhit:
                potholes.empty()
                enemies.empty()
                bullets.empty()
                bombs.empty()
                rocks.empty()
                badthings.empty()
                car.reset()
                car._sounds['dead'].play()
                gs.lives -= 1
                gs._distance = 0

        # check enemy dead conditions.
        collided = pygame.sprite.groupcollide(
                        bullets, enemies, True, True)

        for ufo_colls in collided.values():
            for ufo in ufo_colls:
                ufo._sounds['dead'].play()
                gs.incpoint()

        # check for killed bombs.
        collided = pygame.sprite.groupcollide(
                        bullets, bombs, True, True)

        for bomb_colls in collided.values():
            for bomb in bomb_colls:
                bomb._sounds['dead'].play()
                bomb.kill()
                gs.incpoint()

        pygame.sprite.groupcollide(potholes, rocks, False, True)

        # check for killed rocks.
        collided = pygame.sprite.groupcollide(
                        bullets, rocks, True, True)

        for rock_colls in collided.values():
            for rock in rock_colls:
                rock._sounds['dead'].play()
                rock.kill()
                gs.incpoint()


        for bomb in bombs:
            if bomb.rect.bottom - 5 > settings.GROUND_HEIGHT:
                placepothole(bomb.rect.centerx, potholes, badthings)
                bomb.kill()
                bomb._sounds['dead'].play()

        # HUD display.
        hud = makehud(
            time=gs.time,
            points=gs.points,
            lives=gs.lives,
            distance=gs.distance)

        screen.blit(hud, (100, 500))

        pygame.display.flip()

        if checkendgame(gs):
            break

    return gs

