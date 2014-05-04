class Bullet(pygame.sprite.Sprite):

    WIDTH = 3

    def __init__(self, x, y, speedx, speedy, *groups):
        super(Bullet, self).__init__(*groups)
        width, height = speedx or self.WIDTH, speedy or self.WIDTH
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        pygame.draw.line(
            self.image,
            settings.BULLET_COLOUR,
            (0, 0), (speedx, speedy), self.WIDTH)
        self._speedx = speedx
        self._speedy = speedy
        self._distancex = 0

    def update(self):
        self.rect.move_ip(self._speedx, -self._speedy)
        self._distancex += self._speedx
        outofrange = self._distancex > settings.BUGGY_BULLET_RANGE
        if offscreen(*self.rect.topleft) or outofrange:
            self.kill()

