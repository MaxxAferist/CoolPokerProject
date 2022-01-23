import pygame
from functions import *


pygame.mixer.init()

class Settings():
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.stack_sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        fon = load_image('buttons//settings.png')
        self.fon.image = pygame.transform.scale(fon, (WIDTH // 3, HEIGHT // 3))
        self.fon.rect = fon.get_rect()
        self.fon.rect.x = (WIDTH - self.fon.rect.w) // 2
        self.fon.rect.y = (HEIGHT - self.fon.rect.h) // 2

        f = pygame.font.Font(None, int(48 * KOEF))
        self.music = f.render('Музыка', True,
                              (255, 255, 255))
        self.fon.image.blit(self.music, (((self.fon.rect.w - self.music.get_rect()[2]) // 2 - 30 * KOEF),
                                         (self.fon.rect.h - self.music.get_rect()[3]) * 0.25))
        self.music_slider = Slider((self.fon.rect.w - self.music.get_rect()[2]) // 2 - 100 * KOEF,
                                   (self.fon.rect.h - self.music.get_rect()[3]) * 0.37,
                                   'gorizontal', 300 * KOEF, self, pygame.mixer.music.get_volume())

        self.sound = f.render('Звуки', True,
                              (255, 255, 255))
        self.fon.image.blit(self.sound, (((self.fon.rect.w - self.music.get_rect()[2]) // 2 - 30 * KOEF),
                                         (self.fon.rect.h - self.music.get_rect()[3]) * 0.6))
        self.sound_slider = Slider((self.fon.rect.w - self.music.get_rect()[2]) // 2 - 100 * KOEF,
                                   (self.fon.rect.h - self.music.get_rect()[3]) * 0.72,
                                   'gorizontal', 300 * KOEF, self, SOUNDS[0].get_volume())
        self.all_sprites.add(self.music_slider.line, self.music_slider, self.sound_slider.line, self.sound_slider)
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
            other.all_sprites.draw(other.screen)
            other.fon_sprite.update()
            if other.timer:
                other.timer.update()
                other.info.update()
            self.all_sprites.draw(other.screen)
            self.all_sprites.update()
            self.stack_sprites.draw(other.screen)
            self.stack_sprites.update()
            pygame.display.flip()
            self.clock.tick(FPS)
            other.screen.fill(pygame.Color(0, 0, 0))
            music_volume = self.music_slider.value
            pygame.mixer.music.set_volume(music_volume)
            sound_volume = self.sound_slider.value
            for sound in SOUNDS:
                sound.set_volume(sound_volume)