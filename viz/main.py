import sys, pygame
import time
from hexdrawer import HexDrawer
pygame.init()


screen_w, screen_h = 720, 720


#print('setting config')
screen = pygame.display.set_mode((screen_w, screen_h))
hd = HexDrawer('sims/example_sim.json', screen_w, screen_h)


while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill((0, 0, 0))
    hd.draw(screen)
    pygame.display.flip()