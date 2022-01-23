import pygame
from functions import *


pygame.mixer.init()

class WinOrLose():
    def __init__(self, player_type, other):
        self.all_sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        if player_type == 'player':
            fon = load_image('Win_window_image.png')
        else:
            fon = load_image('Lose_window_image.png')
        self.fon.image = fon
        self.fon.rect = fon.get_rect()
        self.fon.rect.x = (WIDTH - self.fon.rect.w) // 2
        self.fon.rect.y = -self.fon.rect.h
        self.btn_ok = Button('Хорошо', ((self.fon.rect.w - 300 * KOEF) // 2 + self.fon.rect.x, self.fon.rect.y + self.fon.rect.h * 0.75),
                             (300 * KOEF, 300 * KOEF * 0.37), 60, lambda: other.go_menu(other.player.money, other.user))
        self.all_sprites.add(self.btn_ok)
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self, other):
        while self.running:
            other.screen.fill(pygame.Color(0, 0, 0))
            for event in pygame.event.get():
                pass
            if self.fon.rect.y + 20 < 0:
                self.fon.rect.y += 20
            self.btn_ok.rect.y = self.fon.rect.y + self.fon.rect.h * 0.75
            other.all_sprites.draw(other.screen)
            other.fon_sprite.update()
            self.all_sprites.draw(other.screen)
            self.all_sprites.update()
            pygame.display.flip()
            self.clock.tick(FPS)
