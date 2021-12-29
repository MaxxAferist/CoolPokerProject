from menu import *
from functions import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Poker')
    size = 0, 0
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    running = True
    FPS = 60
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    card_sprites = pygame.sprite.Group()
    fon = pygame.sprite.Sprite(all_sprites)
    fon_image = pygame.transform.scale(load_image('Poker_menu.jpg'), (WIDTH, HEIGHT))
    fon.image = fon_image
    fon.rect = fon_image.get_rect()
    start_menu = Menu()
    start_menu.run()

    while running:
        event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                termit()
            all_sprites.update(event)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
