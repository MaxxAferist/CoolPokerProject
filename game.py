import pygame

from functions import *
from mini_menu import *


pygame.init()


class Poker_player(): #Класс игрока покера
    def __init__(self, money, player_type):
        self.money = money
        self.cards = [None, None]
        self.bid = 0
        self.play = True
        self.move = False
        self.player_type = player_type

    def call(self, table): #Ставка, равная наибольшей ставке на столе
        self.money -= max(list(map(lambda x: x.bid, table.players))) - self.bid
        self.bid += max(list(map(lambda x: x.bid, table.players))) - self.bid
        self.move = False
        print(self.bid)

    def can_call(self, table):
        bid = max(list(map(lambda x: x.bid, table.players)))
        if self.money < bid:
            return False
        return True

    def reise(self, bid): #Ставка, большая чем самая большая
        self.bid += bid
        self.money -= bid
        self.move = False

    def fold(self): #Пас
        self.play = False
        self.cards = [None, None]
        self.move = False

    def va_bank(self): #Ва-банк
        self.bid += self.money
        self.money = 0
        self.move = False

    def check(self): #Пропуск ставки
        self.move = False

    def bet(self, bid):
        self.bid += bid
        self.money -= bid
        self.move = False

    def little_blind(self):
        self.bid = 25
        self.money -= 25
        self.move = False

    def big_blind(self):
        self.bid = 50
        self.money -= 50
        self.move = False


class Poker_Logic(): # Логика покера
    def __init__(self):
        self.deck = self.full_deck()
        self.bank = 0
        self.players = []
        self.table_cards = []

    def full_deck(self): # Полная перемешанная колода карт
        values = ['2', '3', '4', '5', '6', '7', '8', '9',
                  '10', 'J', 'Q', 'K', 'A']
        suits = ['krest', 'pik', 'cherv', 'bubn']
        deck = []
        for suit in suits:
            for value in values:
                deck.append(Card(value, suit, (-1000, -1000)))
        random.shuffle(deck)
        return deck

    def preflop(self): # Выдача карт игрокам
        for player in self.players:
            self.bank += player.bid
            player.bid = 0
            player.cards = [self.deck.pop(), self.deck.pop()]

    def flop(self): # 3 карты на стол
        for player in self.players:
            self.bank += player.bid
            player.bid = 0
        self.table_cards.append(self.deck.pop())
        self.table_cards.append(self.deck.pop())
        self.table_cards.append(self.deck.pop())

    def tern(self): # 4-ая карта на стол
        for player in self.players:
            self.bank += player.bid
            player.bid = 0
        self.table_cards.append(self.deck.pop())

    def river(self): # 5-ая карта на стол
        for player in self.players:
            self.bank += player.bid
            player.bid = 0
        self.table_cards.append(self.deck.pop())

    def max_bid(self):
        return max(list(map(lambda x: x.bid, self.players)))


class Game(): # Игра
    def __init__(self, go_menu):
        pygame.display.set_caption('Game')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.player_place_sprites = pygame.sprite.Group()
        self.table_place_sprites = pygame.sprite.Group()
        self.bot_place_sprites = pygame.sprite.Group()
        self.stack_sprites = pygame.sprite.Group()
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

        self.graph = Poker_graphic()
        self.logic = Poker_Logic()
        self.bot = Poker_player(1000, 'bot')
        self.player = Poker_player(1000, 'player')
        self.players = [self.bot, self.player]
        self.logic.players = [self.bot, self.player]

        buttons_width = 300
        buttons_height = 60
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
                               (buttons_width, buttons_height), font_size, lambda: self.player.call(self))]
        self.all_sprites.add(self.buttons)
        self.button_sprites.add(self.buttons)
        self.add_sprites()
        self.go_menu = go_menu


    def run(self):
        self.running = True
        while self.running:
            self.stack_sprites = pygame.sprite.Group()
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
            self.random_blind()
            self.little_blind()
            self.big_blind()
            while min(list(map(lambda x: x.bid, self.players))) != max(list(map(lambda x: x.bid, self.players))):
                self.stack_sprites = pygame.sprite.Group()
                self.bet()
            self.preflop()

    def random_blind(self):
        random.choice(self.players).move = True

    def little_blind(self):
        for i in range(len(self.players)):
            if self.players[i].move and self.players[i].play:
                self.players[i].little_blind()
                if i + 1 < len(self.players):
                    self.players[i + 1].move = True
                else:
                    self.players[0].move = True
                print(self.players[i].bid)
                break

    def big_blind(self):
        for i in range(len(self.players)):
            if self.players[i].move and self.players[i].play:
                self.players[i].big_blind()
                if i + 1 < len(self.players):
                    self.players[i + 1].move = True
                else:
                    self.players[0].move = True
                print(self.players[i].bid)
                break

    def preflop(self):
        self.logic.preflop()
        self.graph.preflop(self)

    def bet(self):
        for i in range(len(self.players)):
            if self.players[i].move and self.players[i].play:
                if self.players[i].player_type == 'bot':
                    self.players[i].reise(100)
                    if i + 1 < len(self.players):
                        self.players[i + 1].move = True
                    else:
                        self.players[0].move = True
                else:
                    self.graph.bet(self, self.players[i],
                                   self.logic.max_bid() - self.players[i].bid, self.players[i].money)
                    if i + 1 < len(self.players):
                        self.players[i + 1].move = True
                    else:
                        self.players[0].move = True
                print(self.players[i].bid)
                break

    def add_sprites(self): # Все спрайты на столе
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

    def bet(self, table, player, first_value, last_value):
        slider = Slider(400, 500, 'vertical', 200, table)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(slider)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                    running = False
            for btn in table.buttons:
                btn.draw()
            table.all_sprites.draw(table.screen)
            table.stack_sprites.draw(table.screen)
            all_sprites.update()
            all_sprites.draw(table.screen)
            pygame.display.flip()
            table.screen.fill(pygame.Color(0, 0, 0))
        player.bid = round((last_value - first_value) * slider.value + first_value)