import itertools
import pygame
import math
import json

class HexDrawer:
    def __init__(self, sim_fname: str, screen_w: int, screen_h: int, draw_text: bool = True):
        self.draw_text = draw_text

        with open(sim_fname, 'r') as f:
            self.hex_info = json.load(f)

        xmax = max(h['x'] for h in self.hex_info)
        xmin = min(h['x'] for h in self.hex_info)
        ymax = max(h['y'] for h in self.hex_info)
        ymin = min(h['y'] for h in self.hex_info)

        # size calculations
        screen_w = screen_w / 0.9
        screen_h = screen_h * 0.95
        self.x_offset = xmin
        self.y_offset = ymin
        self.hex_w = screen_w / (xmax-xmin)
        self.hex_h = screen_h // (ymax-ymin)
        self.x_displace = self.hex_w * 0.75
        self.y_displace = self.hex_h

        # load images and scale them
        self.img_background = self.load_and_scale('images/hexagon_beach.png')
        self.img_blocked = self.load_and_scale('images/hexagon_bigrocks.png')
        
        self.img_route = self.load_and_scale('images/hexagon_valley.png')
        self.img_start = self.load_and_scale('images/hexagon_grassey.png')
        self.img_end = self.load_and_scale('images/hexagon_far_lava.png')

        #font = pygame.font.Font('freesansbold.ttf', 32)
        #text = font.render('GeeksForGeeks', True, green, blue)
        self.font = pygame.font.SysFont(None, 24)

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
            center = pos[0] + self.hex_w/2, pos[1] + self.hex_h/2

            
            #print(f'drawing at {pos}')
            if hi['blocked']:
                screen.blit(self.img_blocked, pos)
            elif hi['start']:
                screen.blit(self.img_start, pos)
            elif hi['end']:
                screen.blit(self.img_end, pos)
            elif hi['passed']:
                screen.blit(self.img_route, pos)
            else:
                screen.blit(self.img_background, pos)

            if self.draw_text:
                text_img = self.font.render(f'{hi["q"]}, {hi["r"]}, {hi["s"]} / {int(hi["x"])}, {int(hi["y"])}', True, (0,0,0))
                text_w = self.hex_w/2

                text_pos = center[0] - text_img.get_width()/2, center[1] - text_img.get_height()/2


                screen.blit(text_img, text_pos)