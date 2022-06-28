import sys, pygame
import time
from hexdrawer import HexDrawer
pygame.init()


screen_w, screen_h = 640, 480


#print('setting config')
screen = pygame.display.set_mode((screen_w, screen_h))

#hex_info = [
#    {'q': -2, 'r': 4, 's': -2, 'x': 0.0, 'y': 4, 'blocked': False, 'passed': True},
#    {'q': 1, 'r': 2, 's': -3, 'x': 2.0, 'y': 2, 'blocked': False, 'passed': False},
#    {'q': 5, 'r': -4, 's': -1, 'x': 3.0, 'y': -4, 'blocked': False, 'passed': False},
#    {'q': 2, 'r': 3, 's': -5, 'x': 4.0, 'y': 3, 'blocked': False, 'passed': False},
#    {'q': -2, 'r': 2, 's': 0, 'x': -1.0, 'y': 2, 'blocked': True, 'passed': False},
#    {'q': 1, 'r': 1, 's': -2, 'x': 2.0, 'y': 1, 'blocked': False, 'passed': False},
#]

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