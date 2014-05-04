class Rock(pygame.sprite.Sprite):

    _image = scale2x(load(filepath('rock00.png')))

    def __init__(self, *groups):
        super(Rock, self).__init__(*groups)
        self.image = self._image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(
            (settings.DISPLAY_SIZE[0], 
             settings.GROUND_HEIGHT - self.image.get_size()[1]),
            self.image.get_size())
        self._sounds = {
            'dead': pygame.mixer.Sound(filepath('explosion.wav'))}
        self._new = True


    def update(self):
        self.rect.move_ip(-settings.GROUND_SPEED, 0)
        if offscreen(*self.rect.center) and not self._new:
            self.kill()
        elif not offscreen(*self.rect.center):
            self._new = False

