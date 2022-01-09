from ctypes import *
import pygame
import sys
import os
import random


WIDTH = windll.user32.GetSystemMetrics(0)
HEIGHT = windll.user32.GetSystemMetrics(1)
FPS = 60
KOEF = WIDTH / 1920


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
    koef = WIDTH / 1920
    image = pygame.transform.scale(image, (int(w * koef), (h * koef)))
    return image

class Button(pygame.sprite.Sprite):
    def __init__(self, name, pos, size, action=None):
        super(Button, self).__init__()
        self.w = size[0]
        self.h = size[1]
        self.name = name
        f = pygame.font.Font(None, int(48 * KOEF))
        self.text = f.render(self.name, True,
                             (0, 0, 0))
        self.image = pygame.Surface((self.w * KOEF, self.h * KOEF))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.image.blit(self.text, ((self.w * KOEF // 2 - self.text.get_rect()[2] / 2), 20 * KOEF))
        self.click_flag = False
        self.pressed_flag = False
        self.action = action

    def draw(self):
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if self.rect.collidepoint(pos) and pressed:
            self.image.fill((100, 100, 100))
            self.image.blit(self.text, ((self.w * KOEF // 2 - self.text.get_rect()[2] / 2), 20 * KOEF))
            self.pressed_flag = True
        elif self.rect.collidepoint(pos) and self.pressed_flag and not pressed:
            if self.click_flag and self.action:
                self.pressed_flag = False
                self.action()
        elif self.rect.collidepoint(pos):
            self.click_flag = True
            self.image.fill((200, 200, 200))
            self.image.blit(self.text, ((self.w * KOEF // 2 - self.text.get_rect()[2] / 2), 20 * KOEF))
        else:
            self.pressed_flag = False
            self.image.fill((255, 255, 255))
            self.image.blit(self.text, ((self.w * KOEF // 2 - self.text.get_rect()[2] / 2), 20 * KOEF))


class Card(pygame.sprite.Sprite):
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


class Cards_back(pygame.sprite.Sprite):
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
        self.v = 10
        self.final_coords = None, None

    def update(self):
        if self.motion:
            self.rect.x += self.v
            self.rect.y = int(self.k * self.rect.x + self.b) # каждый кадр меняем х на 1, у соотвественно
            if self.rect.x in range(self.final_coords[0] - self.v, self.final_coords[0] + self.v):
                self.rect.x = self.final_coords[0]
                self.rect.y = self.final_coords[1]
                self.motion = False

    def get_trajectory(self, pos1, pos2): #Получаем k и b уравнения y=kx+b - траектория полета карт
        x1, y1 = pos1
        x2, y2 = pos2
        self.rect.x = x1
        self.rect.y = y1
        self.k = (y2 - y1) / (x2 - x1)
        self.b = y1 - self.k * x1
        self.motion = True
        self.final_coords = pos2


class Place_from_card(pygame.sprite.Sprite):
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
        self.image = pygame.transform.scale(Place_from_card.image, (self.rect.w * k, self.rect.h * k))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y