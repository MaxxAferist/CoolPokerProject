from main import *
import pygame


pygame.init()

class Menu():
    def __init__(self):
        pygame.display.set_caption('Menu')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        fon_image = pygame.transform.scale(load_image('Poker_table.jpg'), (WIDTH, HEIGHT))
        self.fon.image = fon_image
        self.fon.rect = fon_image.get_rect()
        self.lst = [Button('Новая Игра', (105, 50)),
                    Button('DSD', (105, 120)),
                    Button('Правила', (105, 190)),
                    Button('Настройки', (105, 260)),
                    Button('Выход', (105, 330))]
        self.all_sprites.add(self.lst)
        self.button_sprites.add(self.lst)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                for i in self.lst:
                    if i.rect.collidepoint(pygame.mouse.get_pos()):
                        i.aimed(True)
                    else:
                        i.aimed(False)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    menu = Menu()
    menu.run()