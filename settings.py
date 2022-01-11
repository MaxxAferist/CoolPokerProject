from menu import *
import pygame
from functions import Slider, Slider_Ball


class Settings_Rect(pygame.sprite.Sprite):
    def __init__(self, image):
        super(Settings_Rect, self).__init__()
        self.image = pygame.transform.scale(image, (700, 444))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - 350
        self.rect.y = HEIGHT // 2 - 200
        f = pygame.font.Font(None, int(48 * KOEF))
        self.music = f.render('Музыка', True,
                              (255, 255, 255))
        self.sound = f.render('Звуки', True,
                              (255, 255, 255))
        self.lst_sl = [Slider(980, 646), Slider(980, 846)]
        self.lst_sl_bl = [Slider_Ball(980, 631), Slider_Ball(980, 831)]

        self.image.blit(self.music, ((700 * KOEF // 2 - self.music.get_rect()[2] / 2 - 100), 20 * KOEF))
        self.image.blit(self.sound, ((700 * KOEF // 2 - self.music.get_rect()[2] / 2 - 100), 20 * KOEF + 200))


class Settings():
    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.slider_sprites = pygame.sprite.Group()
        fon = pygame.image.load('data//buttons//set_button.png')
        self.setting_rect = Settings_Rect(fon)
        self.all_sprites.add(self.setting_rect)
        self.slider_sprites.add(self.setting_rect.lst_sl)
        self.slider_sprites.add(self.setting_rect.lst_sl_bl)
        self.lst_sl = self.setting_rect.lst_sl
        self.lst_sl_bl = self.setting_rect.lst_sl_bl
        self.num = 0
        self.moving = False
        self.all_sprites.add(self.slider_sprites)

    def run(self):
        self.running = True
        offset_x = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(len(self.lst_sl)):
                        pos = event.pos
                        if self.lst_sl_bl[i].clicked(pos):
                            self.num = i
                            self.moving = True
                            offset_x = self.lst_sl_bl[self.num].rect.x - pos[0]

                if event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    if self.moving:
                        if 980 > pos[0] + offset_x:
                            offset_x = 980 - pos[0]
                        elif 1560 < pos[0] + offset_x:
                            offset_x = 1560 - pos[0]
                        self.lst_sl_bl[self.num].rect.x = pos[0] + offset_x
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.moving = False
            self.all_sprites.draw(self.screen)
            self.all_sprites.update()
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    settings = Settings()
    settings.run()
