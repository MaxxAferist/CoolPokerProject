import pygame
import sys
import os
from ctypes import *


def load_image(name):
    filename = os.path.join('data', name)
    if not os.path.isfile(filename):
        print(f'Image is not found: {filename}')
        sys.exit()
    image = transform_image(pygame.image.load(filename))
    return image


def termit():
    pygame.quit()
    sys.exit()


def transform_image(image):
    rect = image.get_rect()
    w = rect.w
    h = rect.h
    koef = width / 1920
    image = pygame.transform.scale(image, (int(w * koef), (h * koef)))
    return image


class Button():
    def __init__(self, x, y, image, scale, func):
        w, h = image.get_width(), image.get_height()
        self.image = pygame.transform.scale(image, (w * scale, h * scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click_flag = False

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_pos) and pressed and not self.click_flag:
            print('click')
            self.click_flag = True
        if not pressed and self.click_flag:
            self.click_flag = False
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Card(pygame.sprite.Sprite):
    def __init__(self, value, suit, pos):
        super().__init__(all_sprites, card_sprites)
        self.value = value
        self.suit = suit
        self.image = load_image(f'cards//{self.value}_{self.suit}.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.motion_go = False

    def update(self, *args):
        if args:
            event = args[0]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
                    self.rect.collidepoint(event.pos):
                self.motion_go = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.motion_go = False
            if event.type == pygame.MOUSEMOTION and self.motion_go:
                self.rect.x += event.rel[0]
                self.rect.y += event.rel[1]


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Poker')
    size = 0, 0
    width, height = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    running = True
    FPS = 60
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    card_sprites = pygame.sprite.Group()
    fon = pygame.sprite.Sprite(all_sprites)
    fon_image = pygame.transform.scale(load_image('Poker_table.jpg'), (width, height))
    fon.image = fon_image
    fon.rect = fon_image.get_rect()
    btn_img = load_image('cards//2_pik.png')
    button = Button(100, 200, btn_img, 1, termit)

    while running:
        event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                termit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                Card('K', 'cherv', event.pos)
            all_sprites.update(event)
        screen.fill(pygame.Color('darkslategray'))
        all_sprites.draw(screen)
        button.draw()
        pygame.display.flip()
        clock.tick(FPS)
