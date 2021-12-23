import pygame
import sys
import os


def termit():
    pygame.quit()
    sys.exit()


def load_image(name):
    filename = os.path.join('data', name)
    if not os.path.isfile(filename):
        print(f'Image is not found: {filename}')
        sys.exit()
    image = pygame.image.load(filename)
    return image


class Buttons(pygame.sprite.Sprite):
    def __init__(self, name, pos):
        super().__init__(all_sprites, button_sprites)
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        f = pygame.font.Font(None, 36)
        self.text = f.render(self.name, True,
                             (0, 0, 0))
        self.image = pygame.Surface((300, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image.blit(self.text, (150 - self.text.get_rect()[2] / 2, 15))


    def aimed(self, flag):
        if flag:
            self.image.fill((200, 200, 200))
            self.image.blit(self.text, (150 - self.text.get_rect()[2] / 2, 15))
        else:
            self.image.fill((255, 255, 255))
            self.image.blit(self.text, (150 - self.text.get_rect()[2] / 2, 15))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Menu')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    button_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    running = True
    FPS = 60
    fon = pygame.sprite.Sprite(all_sprites)
    fon_image = pygame.transform.scale(load_image('Poker_table.jpg'), (width, height))
    fon.image = fon_image
    fon.rect = fon_image.get_rect()
    lst = [Buttons('Новая Игра', (105, 50)), Buttons('DSD', (105, 120)),
           Buttons('Правила', (105, 190)), Buttons('Настройки', (105, 260)),
           Buttons('Выход', (105, 330))]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                termit()
            for i in lst:
                if i.rect.collidepoint(pygame.mouse.get_pos()):
                    i.aimed(True)
                else:
                    i.aimed(False)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
