
class Moonbase(pygame.sprite.Sprite):

    _moonbase00 = scale2x(load(filepath('moonbase00.png')))

    def __init__(self, x, *groups, **kwargs):
        super(Moonbase, self).__init__(*groups)
        self.image = self._moonbase00
        self.rect = pygame.Rect( 
                (x, settings.GROUND_HEIGHT - self.image.get_size()[1]+10), 
                self.image.get_size() 
                )

    def update(self):
        self.rect.move_ip(-settings.GROUND_SPEED, 0)

