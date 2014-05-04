
import pygame
from pygame.transform import scale2x, scale
from pygame.image import load

import settings


class Background(object):

    def __init__(self, images, rect, scrollspeed, randomize=False):
        if not isinstance(images, list):images = [images]

        self._scrollspeed = scrollspeed
        self._randomize = randomize
        self._maxx = rect.right
        self._maxy = rect.bottom
        self._images = images
        # image map is list of [image_index, image_location]
        self._image_map = [[0,0],] 
        self._y = rect.top

    def render(self, screen):

        # move all images left and blit
        for im in self._image_map:
            im[1] -= self._scrollspeed
            x, y = im[1], self._y
            img = self._images[im[0]]
            width, height = img.get_size()
            if x < 0:
                sub_xstart = -x
                width += x
                x = 0
            else: 
                sub_xstart = 0

            maxy = self._maxy
            if (y + height) > maxy:
                height = maxy - y

            subsurf = img.subsurface(pygame.Rect(sub_xstart, 0, width, height))

            screen.blit(subsurf, (x,self._y))

        # while there are not enough images on screen
        while(self._image_map[-1][1] < self._maxx):
            # get info for the last image
            last = self._image_map[-1]
            # if we're going random pick a random new image
            if self._randomize: 
                next_image = random.choice(self._images)

            # otherwise get the next image in our _images list
            else: next_image = (last[0]+1) % len(self._images)
            # place the next image at the end of the last image
            self._image_map.append(
                    [ next_image, 
                      last[1]+self._images[last[0]].get_size()[0] ] )
        # if the first image has moved off screen, pop it!
        if self._image_map[0][1] + \
           self._images[self._image_map[0][0]].get_size()[0] < 0:
                self._image_map.pop(0)


