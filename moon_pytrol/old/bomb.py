
class Bomb(pygame.sprite.Sprite):

    _image = scale2x(load(filepath('bomb.png')))

    def __init__(self, x, y, *groups):
        super(Bomb, self).__init__(*groups)
        width, height = self._image.get_size()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = self._image 
        self.mask = pygame.mask.from_surface(self.image)
        self._speedx = 0  
        self._speedy = 0 
        self._sounds = {
            'drop': pygame.mixer.Sound(filepath('bomb-drop.wav')),
            'dead': pygame.mixer.Sound(filepath('explosion.wav'))}

    def update(self):
        self._speedy += settings.GRAVITY
        self.rect.move_ip(self._speedx, self._speedy)

