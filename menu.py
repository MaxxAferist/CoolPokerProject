from game import *
import pygame
from settings import *

pygame.init()


def go_game():
    run_game = Game()
    run_game.run()

def go_settings():
    run_settings = Settings()
    run_settings.run()


class Beautiful_fon(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (int(WIDTH * 1.3), int(HEIGHT * 1.3)))
        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH - self.rect.w) // 2
        self.rect.y = (HEIGHT - self.rect.h) // 2
        self.v = 0
        self.go = 1
        self.dx = -1
        self.dy = -1

    def update(self, *args):
        if self.v > self.go:
            if self.rect.x + self.dx > 0 or self.rect.x + self.dx + self.rect.w < WIDTH:
                self.dx = -self.dx
            self.rect.x += self.dx
            if self.rect.y + self.dy > 0 or self.rect.y + self.dy + self.rect.h < HEIGHT:
                self.dy = -self.dy
            self.rect.y += self.dy
            self.v = 0
        self.v += 1


class Menu():
    def __init__(self):
        pygame.display.set_caption('Menu')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()
        fon_image = pygame.image.load('data//Poker_menu_2.png')
        self.fon = Beautiful_fon(fon_image)
        self.all_sprites.add(self.fon)
        self.buttons = [Button('Новая Игра', ((WIDTH - 450 * KOEF) // 2,
                                              (HEIGHT - 75 * KOEF * 3 - 20 * KOEF * 2) // 2), (450, 75), go_game),
                    Button('Настройки', ((WIDTH - 450 * KOEF) // 2,
                                         (HEIGHT - 75 * KOEF * 3 - 20 * KOEF * 2) // 2 + 95 * KOEF), (450, 75), go_settings),
                    Button('Выход', ((WIDTH - 450 * KOEF) // 2,
                                     (HEIGHT - 75 * KOEF * 3 - 20 * KOEF * 2) // 2 + 190 * KOEF), (450, 75), termit)]
        self.all_sprites.add(self.buttons)
        self.button_sprites.add(self.buttons)

    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                for btn in self.buttons:
                    btn.draw()
            self.all_sprites.draw(self.screen)
            self.all_sprites.update()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    menu = Menu()
    menu.run()
