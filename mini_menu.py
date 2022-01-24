from functions import *
from settings import Settings
import pygame


def go_settings(other):
    run_settings = Settings()
    run_settings.run(other)

class Mini_menu():
    def __init__(self, other):
        self.all_sprites = pygame.sprite.Group()
        self.btn_sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        fon_image = pygame.Surface((WIDTH * 0.2, HEIGHT))
        fon_image.fill(pygame.Color(132, 66, 0))
        self.fon.image = fon_image
        self.fon.rect = self.fon.image.get_rect()
        self.clock = pygame.time.Clock()
        self.add_buttons(other)
        self.running = True

    def add_buttons(self, other):
        left_top = 30 * KOEF
        up_top = 20 * KOEF
        w_btn = (self.fon.rect.w - left_top * 2) / KOEF
        h_btn = w_btn * 0.37
        self.buttons = [Button('Продолжить', (left_top, up_top), (w_btn, h_btn), 43, self.close),
                        Button('Настройки', (left_top, up_top + h_btn + 20 * KOEF), (w_btn, h_btn), 43, lambda: go_settings(other)),
                        Button('Выйти', (left_top, up_top + h_btn * 2 + 40 * KOEF), (w_btn, h_btn), 43, lambda: other.go_menu(other.player.money, other.user))]
        self.btn_sprites.add(self.buttons)

    def close(self):
        self.running = False

    def run(self, other):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.fon.rect.collidepoint(event.pos):
                        self.running = False
                self.all_sprites.update()
                self.btn_sprites.update()
            other.all_sprites.draw(other.screen)
            self.all_sprites.draw(other.screen)
            self.btn_sprites.draw(other.screen)
            pygame.display.flip()
            self.clock.tick(FPS)