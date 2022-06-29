import sys, pygame
import time
from hexdrawer import HexDrawer
pygame.init()


screen_w, screen_h = 1000, 1000


#print('setting config')
screen = pygame.display.set_mode((screen_w, screen_h))
hd = HexDrawer('sims/walk_2.json', screen_w, screen_h, draw_text=False)


while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0, 0, 0))
    hd.draw(screen)
    pygame.display.flip()


