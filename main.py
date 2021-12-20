import pygame
import sys


def termit():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Poker')
    size = 0, 0
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                termit()
        screen.fill(pygame.Color('darkslategray'))
        pygame.display.flip()