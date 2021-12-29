from game import *
import pygame


pygame.init()


def go_game():
    run_game = Game()
    run_game.run()


class Menu():
    def __init__(self):
        pygame.display.set_caption('Menu')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        fon_image = pygame.transform.scale(load_image('Poker_menu.jpg'), (WIDTH, HEIGHT))
        self.fon.image = fon_image
        self.fon.rect = fon_image.get_rect()
        self.buttons = [Button('Новая Игра', (105, 50), go_game),
                    Button('DSD', (105, 120)),
                    Button('Правила', (105, 190)),
                    Button('Настройки', (105, 260)),
                    Button('Выход', (105, 330), termit)]
        self.all_sprites.add(self.buttons)
        self.button_sprites.add(self.buttons)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                for btn in self.buttons:
                    btn.draw()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == '__main__':
    menu = Menu()
    menu.run()
