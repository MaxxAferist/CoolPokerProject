from functions import *
import pygame


pygame.init()


class Mini_menu():
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.btn_sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        fon_image = pygame.Surface((WIDTH * 0.2, HEIGHT))
        fon_image.fill(pygame.Color(132, 66, 0))
        self.fon.image = fon_image
        self.fon.rect = self.fon.image.get_rect()
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self, other):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.fon.rect.collidepoint(event.pos):
                        self.running = False
                self.all_sprites.update()
            other.all_sprites.draw(other.screen)
            self.all_sprites.draw(other.screen)
            pygame.display.flip()
            self.clock.tick(FPS)
