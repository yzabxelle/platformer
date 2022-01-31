import pygame , sys 
from pygame.locals import *

clock = pygame.time.Clock()

def main():
    pygame.init()
    pygame.display.set_caption('Platformer')
 
    WINDOW_SIZE = (500,400)
    
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32,) # initiate the window

    while True: # game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)
main()
