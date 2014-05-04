
class Pothole(pygame.sprite.Sprite):

    _pothole00 = scale2x(load(filepath('pothole00.png')))
    _pothole01 = scale2x(load(filepath('pothole01.png')))
    _potholes = [_pothole00,_pothole01]

    def __init__(self, x, *groups, **kwargs):
        super(Pothole, self).__init__(*groups)
        self.image = self._potholes[random.randint(0,len(self._potholes)-1)]
        self.rect = pygame.Rect( (x, settings.GROUND_HEIGHT-1), 
                                 self.image.get_size() )
        self._new = True

    def update(self):
        self.rect.move_ip(-settings.GROUND_SPEED, 0)
        if offscreen(*self.rect.bottomright) and not self._new:
            self.kill()
        elif not offscreen(*self.rect.bottomright):
            self._new = False

