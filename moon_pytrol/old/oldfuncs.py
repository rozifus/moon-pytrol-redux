
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

