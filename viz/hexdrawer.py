import itertools
import pygame
import math
import json

class HexDrawer:
    def __init__(self, sim_fname: str, screen_w: int, screen_h: int):

        with open(sim_fname, 'r') as f:
            self.hex_info = json.load(f)

        xmax = max(h['x'] for h in self.hex_info)
        xmin = min(h['x'] for h in self.hex_info)
        ymax = max(h['y'] for h in self.hex_info)
        ymin = min(h['y'] for h in self.hex_info)

        # size calculations
        screen_w = screen_w / 0.85
        screen_h = screen_h * 0.8
        self.x_offset = xmin
        self.y_offset = ymin
        self.hex_w = screen_w / (xmax-xmin)
        self.hex_h = screen_h // (ymax-ymin)
        self.x_displace = self.hex_w * 0.75
        self.y_displace = self.hex_h

        # load images and scale them
        self.img_red = self.load_and_scale('images/hexagon_small_lava.png')
        self.img_blue = self.load_and_scale('images/hexagon_water.png')
        self.img_green = self.load_and_scale('images/hexagon_grassey.png')

        #font = pygame.font.Font('freesansbold.ttf', 32)
        #text = font.render('GeeksForGeeks', True, green, blue)

    def load_and_scale(self, img_fname: str):
        img = pygame.image.load(img_fname)
        return pygame.transform.scale(img, (self.hex_w, self.hex_h))

    def map_coords(self, x: int, y: int):
        '''Map original map coordinates to the top left of their coords.'''
        x_coord = (x - self.x_offset)
        y_coord = (y - self.y_offset)
        screen_x = x_coord * self.x_displace
        screen_y = y_coord * self.y_displace + self.y_displace / 2 * (x_coord & 1)
        return screen_x, screen_y

    def draw(self, screen):
        #for x,y in itertools.product(list(range(self.)))
        for hi in self.hex_info:
            pos = self.map_coords(hi['x'], hi['y'])
            
            #print(f'drawing at {pos}')
            if hi['blocked']:
                screen.blit(self.img_red, pos)
            elif hi['passed']:
                screen.blit(self.img_green, pos)
            else:
                screen.blit(self.img_blue, pos)

