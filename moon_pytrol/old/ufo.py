class Ufo(pygame.sprite.Sprite):

    _image = scale(load(filepath('ufo.png')), (60,24))

    def __init__(self, x, y, container, *groups):
        super(Ufo, self).__init__(*groups)
        width, height = self._image.get_size()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = self._image 
        self.container = container
        self._accelx = 0.1 
        self._accely = 0.1 
        self._speedx = 2  
        self._speedy = 2
        self._sounds = {
            'dead': pygame.mixer.Sound(filepath('explosion.wav'))}

    def update(self):
        self.rect.move_ip(self._speedx, -self._speedy)

        near = nearborder(self, 80, self.container)
        if near[0]: 
            self._speedy -= self._accely
        if near[2]:
            self._speedy += self._accely
        if near[1]:
            self._speedx -= self._accelx
        if near[3]: 
            self._speedx += self._accelx
        if offscreen(*self.rect.topleft):
            self.kill()

