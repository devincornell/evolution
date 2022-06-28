import itertools
import pygame
import math

class HexDrawer:
    def __init__(self, xmin: int, xmax: int, ymin: int, ymax: int, screen_w: int, screen_h: int):
        #self.x = x
        #self.y = y
        #self.width = width
        #self.height = height
        #self.hex_x = hex_x
        #self.hex_y = hex_y
        self.x_offset = xmin
        self.y_offset = ymin
        self.hex_w = screen_w / (xmax-xmin) / 1.5
        self.hex_h = screen_h / (ymax-ymin)

        # load image and scale it
        self.img_red = self.load_and_scale('images/hexagon_red.png')
        self.img_blue = self.load_and_scale('images/hexagon_blue.png')
        self.img_green = self.load_and_scale('images/hexagon_green.png')
        #self.hex_img = pygame.transform.scale(self.hex_img, (self.hex_w, self.hex_h))
        #self.hex_rect = self.hex_img.get_rect()

    def load_and_scale(self, img_fname: str):
        img = pygame.image.load(img_fname)
        return pygame.transform.scale(img, (self.hex_w, self.hex_h)) 
    
    def draw(self, screen, hex_info: list):
        #for x,y in itertools.product(list(range(self.)))
        for hi in hex_info:
            pos = (
                math.fabs((hi['x'] + self.x_offset) * self.hex_w),
                math.fabs((hi['y'] + self.y_offset) * self.hex_h) - self.hex_h//2 * ((hi['y'] + self.y_offset) & 1),
            )
            print(f'drawing at {pos}')
            if hi['blocked']:
                screen.blit(self.img_red, pos)
            elif hi['passed']:
                screen.blit(self.img_green, pos)
            else:
                screen.blit(self.img_blue, pos)
        #win.blit(self.sprite, (self.x, self.y))
        #if hitboxes == True:
        #    pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

