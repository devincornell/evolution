import sys, pygame
import time
from hexdrawer import HexDrawer
pygame.init()


screen_w, screen_h = 720, 720


#print('setting config')
screen = pygame.display.set_mode((screen_w, screen_h))

import pickle
with open('images/tmp_loc_info.pic', 'rb') as f:
    hex_info = pickle.load(f)

xmax = max(h['x'] for h in hex_info)
xmin = min(h['x'] for h in hex_info)
ymax = max(h['y'] for h in hex_info)
ymin = min(h['y'] for h in hex_info)

hd = HexDrawer(xmin, xmax, ymin, ymax, screen_w, screen_h)

print(xmin, xmax, ymin, ymax)

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0, 0, 0))
    hd.draw(screen, hex_info)
    pygame.display.flip()