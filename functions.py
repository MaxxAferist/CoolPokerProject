from ctypes import *
import pygame
import sys
import os
import random

WIDTH = windll.user32.GetSystemMetrics(0)
HEIGHT = windll.user32.GetSystemMetrics(1)
FPS = 60
KOEF = WIDTH / 1920


def load_image(name): #Загрузка картинки
    filename = os.path.join('data', name)
    if not os.path.isfile(filename):
        print(f'Image is not found: {filename}')
        sys.exit()
    image = transform_image(pygame.image.load(filename))
    return image


def termit(): #Выход
    pygame.quit()
    sys.exit()


def transform_image(image): #Трансформация картинки
    rect = image.get_rect()
    w = rect.w
    h = rect.h
    koef = WIDTH / 1920
    image = pygame.transform.scale(image, (int(w * koef), int(h * koef)))
    return image


class Button(pygame.sprite.Sprite): #Класс кнопок
    image = load_image('buttons//button.png')
    def __init__(self, name, pos, size, font_size, action=None):
        super(Button, self).__init__()
        self.w = size[0]
        self.h = size[1]
        self.name = name
        self.font_size = font_size * KOEF
        self.up_top = (self.h - self.font_size) // 2
        f = pygame.font.Font(None, int(self.font_size))
        self.text = f.render(self.name, True,
                             (0, 0, 0))
        self.image = pygame.transform.scale(Button.image, (int(self.w * KOEF), int(self.h * KOEF)))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image.blit(self.text, ((self.w * KOEF // 2 - self.text.get_rect()[2] / 2), self.up_top * KOEF))
        self.click_flag = False
        self.pressed_flag = False
        self.action = action

    def draw(self):
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(pos) and pressed:
            f = pygame.font.Font(None, int(self.font_size))
            self.image = pygame.transform.scale(Button.image, (int(self.w * KOEF), int(self.h * KOEF)))
            self.text = f.render(self.name, True,
                                 (255, 255, 0))
            self.image.blit(self.text, ((self.w * KOEF // 2 - self.text.get_rect()[2] / 2), self.up_top * KOEF))
            self.pressed_flag = True
        elif self.rect.collidepoint(pos) and self.pressed_flag and not pressed:
            if self.click_flag and self.action:
                self.pressed_flag = False
                self.action()
        elif self.rect.collidepoint(pos):
            self.click_flag = True
            f = pygame.font.Font(None, int(self.font_size))
            self.image = pygame.transform.scale(Button.image, (int(self.w * KOEF), int(self.h * KOEF)))
            self.text = f.render(self.name, True,
                                 (0, 162, 232))
            self.image.blit(self.text, ((self.w * KOEF // 2 - self.text.get_rect()[2] / 2), self.up_top * KOEF))
        else:
            self.pressed_flag = False
            f = pygame.font.Font(None, int(self.font_size))
            self.image = pygame.transform.scale(Button.image, (int(self.w * KOEF), int(self.h * KOEF)))
            self.text = f.render(self.name, True,
                                 (255, 255, 255))
            self.image.blit(self.text, ((self.w * KOEF // 2 - self.text.get_rect()[2] / 2), self.up_top * KOEF))


class Card(pygame.sprite.Sprite): #Класс карт
    def __init__(self, value, suit, pos):
        super().__init__()
        self.value = value
        self.suit = suit
        self.image = load_image(f'cards//{self.value}_{self.suit}.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.motion_go = False

    def update(self):
        pass


class Cards_back(pygame.sprite.Sprite): #Рубашка карт
    image = load_image('Back_card.png')

    def __init__(self):
        super().__init__()
        self.image = Cards_back.image
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0
        self.motion = False
        self.k = None
        self.b = None
        self.v = round(40 * KOEF)
        self.final_coords = [0, 0]

    def update(self):
        if self.motion:
            self.rect.x += self.v
            self.rect.y = int(self.k * self.rect.x + self.b)  # каждый кадр меняем х на 1, у соотвественно
            if self.rect.x in range(self.final_coords[0] - self.v, self.final_coords[0] + self.v):
                self.rect.x = self.final_coords[0]
                self.rect.y = self.final_coords[1]
                self.motion = False

    def get_trajectory(self, pos1, pos2):  # Получаем k и b уравнения y=kx+b - траектория полета карт
        x1, y1 = pos1
        x2, y2 = pos2
        self.rect.x = x1
        self.rect.y = y1
        self.k = (y2 - y1) / (x2 - x1)
        self.b = y1 - self.k * x1
        self.motion = True
        self.final_coords = pos2


class Place_from_card(pygame.sprite.Sprite): #Место для карты
    image = load_image('place_from_card.png')

    def __init__(self, pos):
        super().__init__()
        self.image = Place_from_card.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def resize(self, k):
        x = self.rect.x
        y = self.rect.y
        self.image = pygame.transform.scale(Place_from_card.image, (int(self.rect.w * k), (self.rect.h * k)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Slider(pygame.sprite.Sprite): #Класс слайдеров
    image = load_image('buttons//slider.png')
    def __init__(self, x, y, type, len, other):
        super().__init__()
        self.len = len
        self.type = type
        self.line_width = 20 * KOEF
        self.x0 = x + other.fon.rect.x
        self.y0 = y + other.fon.rect.y
        if self.type == 'vertical':
            self.image = pygame.transform.rotate(pygame.transform.scale(Slider.image, (int(20 * KOEF), int(50 * KOEF))), 90)
            line_image = pygame.Surface((self.line_width, self.len))
            self.line = pygame.sprite.Sprite()
            self.line.image = line_image
            self.line.rect = line_image.get_rect()
        elif self.type == 'gorizontal':
            self.image = pygame.transform.scale(Slider.image, (int(20 * KOEF), int(50 * KOEF)))
            line_image = pygame.Surface((self.len, self.line_width))
            self.line = pygame.sprite.Sprite()
            self.line.image = line_image
            self.line.rect = line_image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x + other.fon.rect.x
        self.rect.y = y + other.fon.rect.y
        if self.type == 'gorizontal':
            self.line.rect.x = self.rect.x
            self.line.rect.y = (self.rect.h - self.line.rect.h) // 2 + self.rect.y
        elif self.type == 'vertical':
            self.line.rect.x = (self.rect.w - self.line.rect.w) // 2 + self.rect.x
            self.line.rect.y = self.rect.y - (self.line.rect.h - self.rect.h)
        self.click_flag = False
        other.stack_sprites.add(self.line, self)
        self.value = 0

    def update(self):
        pressed = pygame.mouse.get_pressed()[0]
        pos = pygame.mouse.get_pos()
        if self.click_flag and pressed:
            if self.type == 'gorizontal':
                if pos[0] > self.x0 + self.rect.w // 2 and \
                    pos[0] < self.x0 + self.line.rect.w - self.rect.w // 2:
                    self.rect.centerx = pos[0]
            elif self.type == 'vertical':
                if pos[1] <= self.y0 + self.rect.h // 2 and \
                        pos[1] >= self.y0 - self.line.rect.h + self.rect.h // 2:
                    self.rect.centery = pos[1]
            if self.type == 'gorizontal':
                if pos[0] < self.x0:
                    self.rect.x = self.x0
                elif pos[0] > self.x0 + self.line.rect.w:
                    self.rect.x = self.x0 + self.line.rect.w
            elif self.type == 'verticle':
                if pos[1] < self.y0 + self.rect.h - self.line.rect.h:
                    self.rect.y = self.y0 + self.rect.h - self.line.rect.h
                elif pos[1] > self.y0 + self.rect.h // 2:
                    self.rect.y = self.y0 + self.rect.h // 2
            self.change_value()
        elif self.rect.collidepoint(pos):
            self.click_flag = True
        else:
            self.click_flag = False

    def change_value(self):
        if self.type == 'gorizontal':
            self.value = (self.rect.x - self.x0) / (self.len - self.rect.w)
        elif self.type == 'vertical':
            self.value = (self.y0 - self.rect.y) / (self.len - self.rect.h)
        self.value = round(self.value, 2)


class Counter(pygame.sprite.Sprite):
    def __init__(self, count, pos):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.image = pygame.Surface((pos[2], pos[3]), pygame.SRCALPHA)
        self.ramka = pygame.draw.rect(self.image, (0, 0, 0), (0, 0, pos[2], pos[3]), 4)
        self.count = count
        self.font = pygame.font.Font(None, int(100 * KOEF))
        self.text = self.font.render(str(self.count), True, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.image.blit(self.text, (0, 0))