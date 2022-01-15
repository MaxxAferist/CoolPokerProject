import pygame

from functions import *
from mini_menu import *

pygame.init()


class Poker_player():
    def __init__(self, money):
        self.money = money
        self.cards = [None, None]
        self.bid = 0
        self.play = True

    def call(self, table):
        self.bid = max(list(map(lambda x: x.bid, table.players)))
        self.money -= self.bid

    def can_call(self, table):
        bid = max(list(map(lambda x: x.bid, table.players)))
        if self.money < bid:
            return False
        return True

    def reise(self, bid):
        self.bid = bid
        self.money -= bid

    def fold(self):
        self.play = False
        self.cards = [None, None]

    def va_bank(self):
        self.bid += self.money
        self.money = 0

    def check(self):
        pass

    def bet(self, bid):
        self.bid = bid
        self.money -= bid


class Poker_Logic():
    def __init__(self):
        self.deck = self.full_deck()
        self.bank = 0
        self.players = []
        self.table_cards = []

    def full_deck(self):
        values = ['2', '3', '4', '5', '6', '7', '8', '9',
                  '10', 'J', 'Q', 'K', 'A']
        suits = ['krest', 'pik', 'cherv', 'bubn']
        deck = []
        for suit in suits:
            for value in values:
                deck.append(Card(value, suit, (-1000, -1000)))
        random.shuffle(deck)
        return deck

    def preflop(self):
        for player in self.players:
            player.append(self.deck.pop())
            player.append(self.deck.pop())

    def flop(self):
        self.table_cards.append(self.deck.pop())
        self.table_cards.append(self.deck.pop())
        self.table_cards.append(self.deck.pop())

    def tern(self):
        self.table_cards.append(self.deck.pop())

    def river(self):
        self.table_cards.append(self.deck.pop())

    def check(self, person):
        values = ['2', '3', '4', '5', '6', '7', '8', '9',
                  '10', 'J', 'Q', 'K', 'A']
        cards = []
        your_cards = []
        your_combunations = []
        combinations = ['royal flush', 'straight flush', 'four of kind',
                        'full house', 'flush', 'straight', 'three of kind',
                        'two pair', 'pair', 'high card']
        for i in self.table_cards:
            cards.append((i.value, i.suit))
        if person == 'player':
            your_cards = [(self.players[0][2].value, self.players[0][2].suit),
                          (self.players[0][3].value, self.players[0][3].suit)]
        elif person == 'bot':
            your_cards = [(self.players[1][2].value, self.players[1][2].suit),
                          (self.players[1][3].value, self.players[1][3].suit)]
        all_values = [i[0] for i in your_cards + cards]
        all_suits = [i[1] for i in your_cards + cards]
        card_suits = [i[1] for i in cards]
        card_val = [i[0] for i in cards]
        swap = True
        while swap:
            swap = False
            for i in range(len(all_values) - 1):
                if values.index(all_values[i]) > values.index(all_values[i + 1]):
                    all_values[i], all_values[i + 1] = all_values[i + 1], all_values[i]
                    swap = True
        while swap:
            swap = False
            for i in range(len(card_val) - 1):
                if values.index(card_val[i]) > values.index(card_val[i + 1]):
                    card_val[i], card_val[i + 1] = card_val[i + 1], card_val[i]
                    swap = True
        no_rep_all_val = []
        for i in all_values:
            if i not in no_rep_all_val:
                no_rep_all_val.append(i)
        no_rep_card = []
        for i in card_val:
            if i not in no_rep_card:
                no_rep_card.append(i)
        print(cards, your_cards)
        lst_straight = self.straight_check(no_rep_all_val, no_rep_card, values)
        # флеш рояль
        if (len(set(card_suits)) != 1 and max([all_suits.count(i) for i in all_suits]) == 5) and \
                (len(lst_straight) == 5 and lst_straight[0] == '10'):
            your_combunations.append(combinations[0])
            return your_combunations
        # стрит флеш
        if (len(set(card_suits)) != 1 and max([all_suits.count(i) for i in all_suits]) == 5) and \
                (len(lst_straight) == 5):
            your_combunations.append(combinations[1])
            return your_combunations
        # каре
        if self.intersection(all_values, card_val, 4) == 1:
            your_combunations.append(combinations[2])
        # фулхаус
        if self.intersection(all_values, card_val, 3) == 1 and self.intersection(all_values, card_val, 2) == 1:
            your_combunations.append(combinations[3])
            return your_combunations
        # флеш
        if len(set(card_suits)) != 1 and max([all_suits.count(i) for i in all_suits]) == 5:
            your_combunations.append(combinations[4])
        # стрит
        if len(lst_straight) == 5:
            your_combunations.append(combinations[5])
            return your_combunations
        # сет(тройка)
        if self.intersection(all_values, card_val, 3) == 1:
            your_combunations.append(combinations[6])
        # 2 пары
        if self.intersection(all_values, card_val, 2) == 2:
            your_combunations.append(combinations[7])
        # пара
        if self.intersection(all_values, card_val, 2) == 1:
            your_combunations.append(combinations[8])
        # большая карта
        if max([values.index(i) for i in card_val]) < max([values.index(i) for i in [j for j in all_values if j not in card_val]]):
            your_combunations.append(combinations[9])

        return your_combunations

    def intersection(self, all_cards, table_cards, count):

        all_cards = set([i for i in all_cards if all_cards.count(i) >= count])
        table_cards = set([i for i in table_cards if table_cards.count(i) >= count])
        if len(all_cards) > len(table_cards):
            return len(all_cards) - len(table_cards)
        return 0

    def straight_check(self, all_cards, table_cards, values):
        for i in range(len(all_cards), 0, -1):
            if ''.join(all_cards[i-5:i]) in ''.join(values):
                lst_straight = all_cards[i-5:i]
                if ''.join(table_cards[i-5:i]) in ''.join(values):
                    return [0]
                return lst_straight
        return [0]


class Game():
    def __init__(self, go_menu):
        pygame.display.set_caption('Game')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.player_place_sprites = pygame.sprite.Group()
        self.table_place_sprites = pygame.sprite.Group()
        self.bot_place_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite(self.all_sprites)
        fon_image = pygame.transform.scale(load_image('Poker_table_fon.png'), (WIDTH, HEIGHT))
        self.fon.image = fon_image
        self.fon.rect = fon_image.get_rect()
        robot_image = load_image('bot_head.png')
        koloda_image = load_image('Koloda_card.png')
        self.robot_image = pygame.transform.scale(robot_image, (int(robot_image.get_width() * KOEF),
                                                                int(robot_image.get_height() * KOEF)))
        self.koloda_image = pygame.transform.scale(koloda_image, (int(koloda_image.get_width() * KOEF),
                                                                  int(koloda_image.get_height() * KOEF)))

        buttons_width = 300
        buttons_height = 60
        promezh = 5
        font_size = 50
        self.buttons = [Button('Пас', (WIDTH * 0.8, HEIGHT * 0.75 - 15 * KOEF),
                               (buttons_width, buttons_height), font_size, termit),
                        Button('Чек', (WIDTH * 0.8, HEIGHT * 0.75 + 55 * KOEF),
                               (buttons_width, buttons_height), font_size, termit),
                        Button('Ва-Банк', (WIDTH * 0.8, HEIGHT * 0.75 + 125 * KOEF),
                               (buttons_width, buttons_height), font_size, termit),
                        Button('Райс', (WIDTH * 0.8, HEIGHT * 0.75 - 85 * KOEF),
                               (buttons_width, buttons_height), font_size, termit),
                        Button('Колл', (WIDTH * 0.8, HEIGHT * 0.75 - 155 * KOEF),
                               (buttons_width, buttons_height), font_size, termit)]
        self.all_sprites.add(self.buttons)
        self.button_sprites.add(self.buttons)
        self.add_sprites()
        self.logic = Poker_Logic()
        self.logic.players = [[1000, 'player'], [1000, 'bot']]
        self.logic.preflop()
        self.logic.flop()
        self.logic.tern()
        self.logic.river()
        print(self.logic.check('player'))
        self.go_menu = go_menu

    def run(self):
        self.running = True
        self.graph = Poker_graphic()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    self.start_mini_menu()
            for btn in self.buttons:
                btn.draw()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.screen.fill(pygame.Color(0, 0, 0))
            self.clock.tick(FPS)

    def add_sprites(self):
        w_card = Place_from_card.image.get_width()
        h_card = Place_from_card.image.get_height()
        left_top = (WIDTH - (w_card * 5 + 40 * KOEF * 4)) // 2
        up_top = (HEIGHT - h_card) * 0.4
        for i in range(5):
            pos = left_top + i * w_card + i * 40 * KOEF, up_top
            place = Place_from_card(pos)
            self.all_sprites.add(place)
            self.table_place_sprites.add(place)

        left_top = (WIDTH - (w_card * 2 + 40 * KOEF)) // 2
        up_top = (HEIGHT - h_card) * 0.85
        for i in range(2):
            pos = left_top + i * w_card + i * 40 * KOEF, up_top
            place = Place_from_card(pos)
            self.all_sprites.add(place)
            self.player_place_sprites.add(place)

        w_card_k = Place_from_card.image.get_width()
        h_card_k = Place_from_card.image.get_height()
        left_top = (WIDTH - (w_card_k * 2 + 40 * KOEF)) // 2
        up_top = int((HEIGHT - h_card) * 0.07)
        for i in range(2):
            pos = left_top + i * w_card_k + i * 40 * KOEF, up_top
            place = Place_from_card(pos)
            self.all_sprites.add(place)
            self.bot_place_sprites.add(place)

        robot = pygame.sprite.Sprite(self.all_sprites)
        robot.image = pygame.transform.scale(self.robot_image, (int(w_card_k * 0.75), (h_card_k * 0.75)))
        robot.rect = self.robot_image.get_rect()

        up_top = int((HEIGHT - h_card) * 0.07)
        left_top = (WIDTH - (w_card_k * 2 + 40 * KOEF)) // 2 - w_card_k
        robot.rect.x = left_top
        robot.rect.y = up_top

        self.koloda = pygame.sprite.Sprite(self.all_sprites)
        self.koloda.image = pygame.transform.scale(self.koloda_image, (w_card_k, h_card_k))
        self.koloda.rect = self.koloda_image.get_rect()

        up_top = (HEIGHT - h_card) * 0.4
        left_top = (WIDTH - self.koloda.rect.w) * 0.05
        self.koloda.rect.x = left_top
        self.koloda.rect.y = up_top

    def start_mini_menu(self):
        self.mini_menu = Mini_menu()
        self.mini_menu.run(self)


class Poker_graphic():
    def __init__(self):
        self.bank = 0
        self.table_cards = pygame.sprite.Group()
        self.players_cards = pygame.sprite.Group()

    def preflop(self, table):
        cards = pygame.sprite.Group()
        for i in range(2):
            card = Cards_back()
            x2 = table.player_place_sprites.sprites()[i].rect.x
            y2 = table.player_place_sprites.sprites()[i].rect.y
            x1 = table.koloda.rect.x
            y1 = table.koloda.rect.y
            card.get_trajectory((x1, y1), (x2, y2))
            cards.add(card)
        for i in range(2):
            card = Cards_back()
            x2 = table.bot_place_sprites.sprites()[i].rect.x
            y2 = table.bot_place_sprites.sprites()[i].rect.y
            x1 = table.koloda.rect.x
            y1 = table.koloda.rect.y
            card.get_trajectory((x1, y1), (x2, y2))
            cards.add(card)
        table.all_sprites.add(cards)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    table.go_menu()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    table.start_mini_menu()
            for btn in table.buttons:
                btn.draw()
            table.all_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
            table.screen.fill(pygame.Color(0, 0, 0))
            if not any(list(map(lambda x: x.motion, cards.sprites()))):
                break

    def flop(self, table):
        cards = pygame.sprite.Group()
        for i in range(3):
            card = Cards_back()
            x2 = table.table_place_sprites.sprites()[i].rect.x
            y2 = table.table_place_sprites.sprites()[i].rect.y
            x1 = table.koloda.rect.x
            y1 = table.koloda.rect.y
            card.get_trajectory((x1, y1), (x2, y2))
            cards.add(card)
        table.all_sprites.add(cards)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    table.go_menu()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    table.start_mini_menu()
            for btn in table.buttons:
                btn.draw()
            table.all_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
            table.screen.fill(pygame.Color(0, 0, 0))
            if not any(list(map(lambda x: x.motion, cards.sprites()))):
                break

    def tern(self, table):
        cards = pygame.sprite.Group()
        card = Cards_back()
        x2 = table.table_place_sprites.sprites()[-2].rect.x
        y2 = table.table_place_sprites.sprites()[-2].rect.y
        x1 = table.koloda.rect.x
        y1 = table.koloda.rect.y
        card.get_trajectory((x1, y1), (x2, y2))
        cards.add(card)
        table.all_sprites.add(cards)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    table.go_menu()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    table.start_mini_menu()
            for btn in table.buttons:
                btn.draw()
            table.all_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
            table.screen.fill(pygame.Color(0, 0, 0))
            if not any(list(map(lambda x: x.motion, cards.sprites()))):
                break

    def river(self, table):
        cards = pygame.sprite.Group()
        card = Cards_back()
        x2 = table.table_place_sprites.sprites()[-1].rect.x
        y2 = table.table_place_sprites.sprites()[-1].rect.y
        x1 = table.koloda.rect.x
        y1 = table.koloda.rect.y
        card.get_trajectory((x1, y1), (x2, y2))
        cards.add(card)
        table.all_sprites.add(cards)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    table.go_menu()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    table.start_mini_menu()
            for btn in table.buttons:
                btn.draw()
            table.all_sprites.draw(table.screen)
            for btn in table.buttons:
                btn.draw()
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
            table.screen.fill(pygame.Color(0, 0, 0))
            if not any(list(map(lambda x: x.motion, cards.sprites()))):
                break
