import pygame

from game import *
from settings import Settings


pygame.init()
pygame.mixer.init()


def go_menu(player_count, User):
    start_menu = Menu(player_count, User)
    start_menu.run()


def go_game(count, User):
    run_game = Game(count, User, go_menu)
    run_game.run()


def go_settings(other):
    run_settings = Settings()
    run_settings.run(other)


class Beautiful_Fon(pygame.sprite.Sprite):
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
    def __init__(self, player_count, User):
        self.player_count = player_count
        self.username = User
        pygame.display.set_caption('Menu')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.fon_sprite = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()
        fon_image = pygame.image.load('data//Poker_menu_2.png')
        self.fon = Beautiful_Fon(fon_image)
        self.all_sprites.add(self.fon)
        self.fon_sprite.add(self.fon)
        buttons_width = 400
        buttons_height = buttons_width * 0.37
        promezh = 5
        self.buttons = [Button('Новая Игра', ((WIDTH - buttons_width * KOEF) // 2,
                                              (HEIGHT - buttons_height * KOEF * 3 - promezh * KOEF * 2) // 2),
                               (buttons_width, buttons_height), 70, lambda: go_game(player_count, User)),
                    Button('Настройки', ((WIDTH - buttons_width * KOEF) // 2,
                                         (HEIGHT - buttons_height * KOEF * 3 - promezh * KOEF * 2) // 2 + (promezh + buttons_height) * KOEF),
                           (buttons_width, buttons_height), 70, lambda: go_settings(self)),
                    Button('Выход', ((WIDTH - buttons_width * KOEF) // 2,
                                     (HEIGHT - buttons_height * KOEF * 3 - promezh * KOEF * 2) // 2 + (promezh + buttons_height) * 2 * KOEF),
                           (buttons_width, buttons_height), 70, lambda: termit(self.player_count, self.username))]
        self.all_sprites.add(self.buttons)
        self.button_sprites.add(self.buttons)

        self.info = Count_info(player_count, (1000, 20, 1000, 100), 100)
        self.all_sprites.add(self.info)

        self.timer = Count_info_timer(self.username, (700, 850, 1150, 100), 100, self)
        self.all_sprites.add(self.timer)

    def run(self):
        pygame.mixer.music.load('data//music//M. Shubin - Drive (demo).mp3')
        pygame.mixer.music.play(-1)
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.button_sprites.update()
            self.all_sprites.draw(self.screen)
            self.all_sprites.update()
            pygame.display.flip()
            self.clock.tick(FPS)
