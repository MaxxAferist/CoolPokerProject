import random

import pygame
from functions import *
from mini_menu import *
from WinOrLoseWindow import WinOrLose

pygame.init()


class Poker_player():  # Класс игрока покера
    def __init__(self, money, player_type):
        self.money = money
        self.cards = [None, None]
        self.bid = 0
        self.play = True
        self.move = False
        self.player_type = player_type
        self.v_bank = False

    def call(self, table):  # Ставка, равная наибольшей ставке на столе
        if self.money - (max(list(map(lambda x: x.bid, table.players))) - self.bid) > 0 and \
                len(set(list(map(lambda x: x.bid, table.players)))) != 1:
            self.money = self.money - (max(list(map(lambda x: x.bid, table.players))) - self.bid)
            self.bid = max(list(map(lambda x: x.bid, table.players)))
            self.move = False
            table.graph.go_bid = False

    def reise(self, bid):  # Ставка, большая чем самая большая
        self.bid += bid
        self.move = False
        self.money -= bid

    def fold(self, table):  # Пас
        self.play = False
        self.cards = [None, None]
        self.move = False
        table.reset = True
        table.graph.go_bid = False

    def va_bank(self, table):  # Ва-банк
        self.bid += self.money
        self.move = False
        self.money = 0
        table.graph.go_bid = False
        table.va_bank = True

    def check(self, table):  # Пропуск ставки
        if len(set(list(map(lambda x: x.bid, table.players)))) == 1:
            self.move = False
            table.graph.go_bid = False
            table.check = True

    def little_blind(self):
        self.bid = 25
        self.move = False
        self.money -= 25

    def big_blind(self):
        self.bid = 50
        self.move = False
        self.money -= 50


class Poker_Logic():  # Логика покера
    def __init__(self):
        self.deck = self.full_deck()
        self.bank = 0
        self.players = []
        self.table_cards = []
        self.border = 1

    def full_deck(self):  # Полная перемешанная колода карт
        values = ['2', '3', '4', '5', '6', '7', '8', '9',
                  '10', 'J', 'Q', 'K', 'A']
        suits = ['krest', 'pik', 'cherv', 'bubn']
        deck = []
        for suit in suits:
            for value in values:
                deck.append(Card(value, suit, (-1000, -1000)))
        random.shuffle(deck)
        return deck

    def preflop(self):  # Выдача карт игрокам
        for player in self.players:
            player.cards = [self.deck.pop(), self.deck.pop()]

    def flop(self):  # 3 карты на стол
        for player in self.players:
            self.bank += player.bid
            player.bid = 0
        self.table_cards.append(self.deck.pop())
        self.table_cards.append(self.deck.pop())
        self.table_cards.append(self.deck.pop())

    def tern(self):  # 4-ая карта на стол
        for player in self.players:
            self.bank += player.bid
            player.bid = 0
        self.table_cards.append(self.deck.pop())

    def river(self):  # 5-ая карта на стол
        for player in self.players:
            self.bank += player.bid
            player.bid = 0
        self.table_cards.append(self.deck.pop())

    def max_bid(self):
        return max(list(map(lambda x: x.bid, self.players)))

    def check(self, player):
        values = ['2', '3', '4', '5', '6', '7', '8', '9',
                  '10', 'J', 'Q', 'K', 'A']
        cards = []
        your_combunations = []
        combinations = ['royal flush', 'straight flush', 'four of kind',
                        'full house', 'flush', 'straight', 'three of kind',
                        'two pair', 'pair', 'high card']
        for i in self.table_cards:
            cards.append((i.value, i.suit))
        your_cards = [(player.cards[0].value, player.cards[0].suit),
                      (player.cards[1].value, player.cards[1].suit)]
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
        lst_straight = self.straight_check(no_rep_all_val, no_rep_card, values)

        # Флеш рояль(Энергетик от суперсел)
        if (max([all_suits.count(i) for i in all_suits]) >= 5 and len(set(all_suits)) <= 3) and \
                (len(lst_straight) == 5 and lst_straight[0] == '10'):
            your_combunations.append((combinations[0], 10))
        # Стрит флеш
        if (max([all_suits.count(i) for i in all_suits]) >= 5 and len(set(all_suits)) <= 3) and \
                (len(lst_straight) == 5):
            your_combunations.append((combinations[1], lst_straight))
        kare = self.intersection(all_values, card_val, 4)
        # Каре(как у девочек дед инсайдих)
        if len(kare) == 1:
            your_combunations.append((combinations[2], kare))
        # Фулхаус
        if len(set([i for i in all_values if all_values.count(i) == 3])) >= 1 and len(
                set([i for i in all_values if all_values.count(i) == 2])) >= 1:
            lst2 = []
            if len(set([i for i in all_values if all_values.count(i) >= 2])) > 2:
                for j in set([i for i in all_values if all_values.count(i) >= 2]):
                    if j in [i[0] for i in your_cards]:
                        lst2.append(j)
            if len(lst2) > 0:
                lst2 = set(max(lst2))
                lst = set([i for i in all_values if all_values.count(i) >= 3]) | lst2
                your_combunations.append((combinations[3], list(lst)))
        # Флеш(энергетик)
        if max([all_suits.count(i) for i in all_suits]) >= 5 and len(set(all_suits)) <= 3:
            your_combunations.append((combinations[4], 7))
        # Стрит(улица)
        if len(lst_straight) == 5:
            your_combunations.append((combinations[5], lst_straight))
        three_of_kind = self.intersection(all_values, card_val, 3)
        # Сет(тройка)
        if len(three_of_kind) == 1:
            your_combunations.append((combinations[6], three_of_kind))
        pairs = self.intersection(all_values, card_val, 2)
        # 2 пары
        if len(pairs) == 2:
            your_combunations.append((combinations[7], pairs))
        # Пара
        if len(pairs) == 1:
            your_combunations.append((combinations[8], pairs))
        # Старшая карта
        your_combunations.append((combinations[9], values[max([values.index(i) for i in [j[0] for j in your_cards]])]))
        return [i for i in your_combunations if your_combunations.count(i) == 1]

    def intersection(self, all_cards, table_cards, count):
        all_cards = set([i for i in all_cards if all_cards.count(i) >= count])
        table_cards = set([i for i in table_cards if table_cards.count(i) >= count])
        if len(all_cards) > len(table_cards):
            lst = all_cards - table_cards
            return list(lst)
        return []

    def define_winner(self, table):
        players_counts = sorted(table.players, key=lambda x: self.counter(self.check(x)))
        player_count = self.counter(self.check(self.players[1]))
        bot_count = self.counter(self.check(self.players[0]))
        if bot_count == player_count:
            return players_counts
        return players_counts[-1]

    def counter(self, combunations):
        values = ['2', '3', '4', '5', '6', '7', '8', '9',
                  '10', 'J', 'Q', 'K', 'A']
        count = 0
        for i in combunations:
            if i[0] == 'royal flush':
                count += 1000
            if i[0] == 'straight flush':
                count += 900 + values.index(i[1][-1]) + 9
            if i[0] == 'four of kind':
                count += 800 + values.index(i[1][0]) + 8
            if i[0] == 'full house':
                count += 700 + (values.index(i[1][0]) + values.index(i[1][1])) // 2 + 7
            if i[0] == 'flush':
                count += 600
            if i[0] == 'straight':
                count += 500 + values.index(i[1][-1]) + 5
            if i[0] == 'three of kind':
                count += 400 + values.index(i[1][0]) + 4
            if i[0] == 'two pair':
                count += 300 + (values.index(i[1][0]) + values.index(i[1][1])) // 2 + 3
            if i[0] == 'pair':
                count += 200 + values.index(i[1][0]) + 2
            if i[0] == 'high card':
                count += 100 + values.index(i[1]) + 1
        return count

    def straight_check(self, all_cards, table_cards, values):
        for i in range(len(all_cards), 0, -1):
            if ''.join(all_cards[i - 5:i]) in ''.join(values):
                lst_straight = all_cards[i - 5:i]
                if ''.join(table_cards[i - 5:i]) in ''.join(values):
                    return [0]
                return lst_straight
        return [0]

    def bot_move(self, bot, player, stage_count, table):
        bot_count = self.counter(self.check(bot))
        if player.bid > bot.money:
            rand = random.randrange(0, 10)
            if rand > 4:
                bot.va_bank(table)
            else:
                table.fold(bot)
        elif stage_count == 0:
            if bot.money < 50:
                bot.va_bank(table)
            else:
                if player.bid > bot.bid:
                    rand = random.randrange(0, 10)
                    if rand > 5:
                        bot.call(table)
                    else:
                        bot.reise(random.randrange(player.bid + 1, player.bid + 26))
        else:
            rand = random.randrange(0, 10)
            if rand > 5:
                bot.call(table)
            else:
                if bot.bid > bot.money * self.border:
                    bot.call(table)
                else:
                    if (bot_count > 500 and bot.money <= 300) or (bot_count > 900):
                        bot.va_bank(table)
                    elif 700 <= bot_count <= 900:
                        self.border = 0.7
                        bot.reise(round(bot.money * 0.15) + player.bid)
                    elif 500 <= bot_count <= 700:
                        self.border = 0.5
                        bot.reise(round(bot.money * 0.1) + player.bid)
                    elif player.bid > bot.money * 0.5:
                        r = random.randrange(0, 10)
                        if r <= 2:
                            table.fold(bot)
                            print(2)
                        else:
                            bot.call(table)
                    elif 300 <= bot_count <= 500:
                        self.border = 0.3
                        bot.reise(round(bot.money * 0.08) + player.bid)
                    elif 200 <= bot_count <= 300:
                        self.border = 0.2
                        bot.reise(round(bot.money * 0.03) + player.bid)
                    elif 109 <= bot_count <= 113:
                        self.border = 0.15
                        bot.reise(round(bot.money * 0.02) + player.bid)
                    else:
                        move_choice = random.choice(['check' * 5, 'fold'])
                        if move_choice == 'check':
                            bot.check(table)
                        else:
                            table.fold(bot)

    def request_player_cards(self, player):
        cards = [(player.cards[0].value, player.cards[0].suit),
                 (player.cards[1].value, player.cards[1].suit)]
        return cards

    def request_table_cards(self):
        cards = []
        for i in self.table_cards:
            cards.append((i.value, i.suit))
        return cards

    def end_distribution(self, player, player2=None):
        for pl in self.players:
            pl.cards = [None, None]
            pl.play = True
            pl.move = False
            self.bank += pl.bid
            pl.bid = 0
        if player2:
            player.money += self.bank // 2
            player2.money += self.bank // 2
        else:
            player.money += self.bank
        self.deck = self.full_deck()
        self.bank = 0
        self.table_cards = []


class Game():  # Игра
    def __init__(self, count, User, go_menu):
        self.user = User
        pygame.display.set_caption('Game')
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.player_place_sprites = pygame.sprite.Group()
        self.table_place_sprites = pygame.sprite.Group()
        self.bot_place_sprites = pygame.sprite.Group()
        self.button_sprites = pygame.sprite.Group()
        self.fon_sprite = pygame.sprite.Group()
        self.cards_sprites = pygame.sprite.Group()
        self.fon = pygame.sprite.Sprite(self.all_sprites, self.fon_sprite)
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
        self.bot = Poker_player(5000, 'bot')
        self.player = Poker_player(count, 'player')
        self.players = [self.bot, self.player]
        self.logic.players = [self.bot, self.player]
        buttons_width = 300
        buttons_height = 60
        font_size = 50
        self.buttons = [Button('Пас', (WIDTH * 0.8, HEIGHT * 0.75 - 15 * KOEF),
                               (buttons_width, buttons_height), font_size, lambda: self.fold(self.player)),
                        Button('Чек', (WIDTH * 0.8, HEIGHT * 0.75 + 55 * KOEF),
                               (buttons_width, buttons_height), font_size, lambda: self.player.check(self)),
                        Button('Ва-Банк', (WIDTH * 0.8, HEIGHT * 0.75 + 125 * KOEF),
                               (buttons_width, buttons_height), font_size, lambda: self.player.va_bank(self)),
                        Button('Райс', (WIDTH * 0.8, HEIGHT * 0.75 - 85 * KOEF),
                               (buttons_width, buttons_height), font_size, termit),
                        Button('Колл', (WIDTH * 0.8, HEIGHT * 0.75 - 155 * KOEF),
                               (buttons_width, buttons_height), font_size, lambda: self.player.call(self))]
        self.button_sprites.add(self.buttons)
        self.add_sprites()
        self.go_menu = go_menu
        self.timer = None

    def run(self):
        pygame.mixer.music.load('data//music//Mark Shubin - Path of life.mp3')
        pygame.mixer.music.play(-1)
        while self.player.money > 0 and self.bot.money > 0:
            self.reset = False
            self.check = False
            self.va_bank = False
            self.ask_on_va_bank = False
            self.random_blind()
            self.little_blind()
            self.update()
            self.big_blind()
            self.update()
            self.preflop()
            self.update()
            while min(list(map(lambda x: x.bid, self.players))) != max(list(map(lambda x: x.bid, self.players))) or \
                    max(list(map(lambda x: x.bid, self.players))) == 0 or self.check:
                if self.va_bank:
                    if self.ask_on_va_bank:
                        break
                    else:
                        self.ask_on_va_bank = True
                        for pl in self.players:
                            if pl.money > 0:
                                asker = pl
                            if pl.money == 0:
                                va_banker = pl
                        if asker.bid >= va_banker.bid:
                            break
                self.bet(0)
                self.update()
                if self.reset:
                    break
            if self.reset:
                continue
            self.flop()
            self.update()
            while min(list(map(lambda x: x.bid, self.players))) != max(list(map(lambda x: x.bid, self.players))) or \
                    max(list(map(lambda x: x.bid, self.players))) == 0 or self.check:
                if self.va_bank:
                    if self.ask_on_va_bank:
                        break
                    else:
                        self.ask_on_va_bank = True
                        for pl in self.players:
                            if pl.money > 0:
                                asker = pl
                            if pl.money == 0:
                                va_banker = pl
                        if asker.bid >= va_banker.bid:
                            break
                self.bet(1)
                self.update()
                if self.reset:
                    break
            if self.reset:
                continue
            self.tern()
            self.update()
            while min(list(map(lambda x: x.bid, self.players))) != max(list(map(lambda x: x.bid, self.players))) or \
                    max(list(map(lambda x: x.bid, self.players))) == 0 or self.check:
                if self.va_bank:
                    if self.ask_on_va_bank:
                        break
                    else:
                        self.ask_on_va_bank = True
                        for pl in self.players:
                            if pl.money > 0:
                                asker = pl
                            if pl.money == 0:
                                va_banker = pl
                        if asker.bid >= va_banker.bid:
                            break
                self.bet(2)
                self.update()
                if self.reset:
                    break
            if self.reset:
                continue
            self.river()
            self.update()
            while min(list(map(lambda x: x.bid, self.players))) != max(list(map(lambda x: x.bid, self.players))) or \
                    max(list(map(lambda x: x.bid, self.players))) == 0 or self.check:
                if self.va_bank:
                    if self.ask_on_va_bank:
                        break
                    else:
                        self.ask_on_va_bank = True
                        for pl in self.players:
                            if pl.money > 0:
                                asker = pl
                            if pl.money == 0:
                                va_banker = pl
                        if asker.bid >= va_banker.bid:
                            break
                self.bet(3)
                self.update()
                if self.reset:
                    break
            if self.reset:
                continue
            self.open_bot_cards()
            self.update()
            self.waiting(2)
            self.who_win()
        if self.player.money <= 0:
            self.lose_window = WinOrLose('bot', self)
            self.lose_window.run(self)
        elif self.bot.money <= 0:
            self.win_window = WinOrLose('player', self)
            self.win_window.run(self)

    def fold(self, player):
        player.fold(self)
        for pl in self.players:
            if not (pl is player):
                self.logic.bank += pl.bid
                pl.bid = 0
                self.end_distribution(pl, False)
                self.update()

    def random_blind(self):
        random.choice(self.players).move = True

    def little_blind(self):
        for i in range(len(self.players)):
            if self.players[i].move and self.players[i].play:
                if self.players[i].player_type == 'bot':
                    self.waiting(1)
                self.players[i].little_blind()
                if i + 1 < len(self.players):
                    self.players[i + 1].move = True
                else:
                    self.players[0].move = True
                break

    def big_blind(self):
        for i in range(len(self.players)):
            if self.players[i].move and self.players[i].play:
                if self.players[i].player_type == 'bot':
                    self.waiting(1)
                self.players[i].big_blind()
                if i + 1 < len(self.players):
                    self.players[i + 1].move = True
                else:
                    self.players[0].move = True
                break

    def preflop(self):
        self.logic.preflop()
        player = list(filter(lambda x: x.player_type == 'player', self.players))[0]
        self.graph.preflop(self, player.cards)

    def flop(self):
        self.logic.flop()
        self.graph.flop(self, self.logic.table_cards)

    def tern(self):
        self.logic.tern()
        self.graph.tern(self, self.logic.table_cards)

    def river(self):
        self.logic.river()
        self.graph.river(self, self.logic.table_cards)

    def bet(self, stage_count):
        self.check = False
        for i in range(len(self.players)):
            if self.players[i].move and self.players[i].play:
                if self.players[i].player_type == 'bot':
                    self.waiting(1)
                    self.logic.bot_move(self.players[i], self.players[i + 1], stage_count, self)
                    if i + 1 < len(self.players):
                        self.players[i + 1].move = True
                    else:
                        self.players[0].move = True
                else:
                    if self.players[i].bid == 0 and self.logic.max_bid() - self.players[i].bid < 25:
                        self.graph.bet(self, self.players[i],
                                       25, self.players[i].money - 1)
                    else:
                        self.graph.bet(self, self.players[i],
                                       self.logic.max_bid() - self.players[i].bid + 1, self.players[i].money - 1)
                    if i + 1 < len(self.players):
                        self.players[i + 1].move = True
                    else:
                        self.players[0].move = True
                break

    def waiting(self, seconds):
        start = time.perf_counter()
        end = time.perf_counter()
        while end - start < seconds:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.start_mini_menu()
            self.all_sprites.draw(self.screen)
            self.cards_sprites.draw(self.screen)
            pygame.display.flip()
            self.screen.fill(pygame.Color(0, 0, 0))
            end = time.perf_counter()

    def update(self):
        self.money_count.gererate_count(self.player.money)
        self.bot_money_count.gererate_count(self.bot.money)
        self.bank_count.gererate_count(self.logic.bank)
        self.bot_bid_count.gererate_count(self.bot.bid)
        self.player_bid_count.gererate_count(self.player.bid)

    def who_win(self):
        im = pygame.sprite.Group()
        winner = self.logic.define_winner(self)
        if type(winner) == list:
            pos = WIDTH / 2 - 300 * KOEF, HEIGHT / 2 - 150 * KOEF
            image = Draw_image(pos)
            im.add(image)
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        running = False
                self.all_sprites.draw(self.screen)
                self.cards_sprites.draw(self.screen)
                im.draw(self.screen)
                im.update()
                pygame.display.flip()
                self.screen.fill(pygame.Color(0, 0, 0))
        elif winner.player_type == 'player':
            volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
            sound = random.choice(WIN_SOUNDS)
            sound.set_volume(volume)
            sound.play()
            pos = WIDTH / 2 - 300 * KOEF, HEIGHT / 2 - 150 * KOEF
            image = YouWin_image(pos)
            im.add(image)
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        running = False
                self.all_sprites.draw(self.screen)
                self.cards_sprites.draw(self.screen)
                im.draw(self.screen)
                im.update()
                pygame.display.flip()
                self.screen.fill(pygame.Color(0, 0, 0))
            sound.stop()
            pygame.mixer.music.set_volume(volume)
        elif winner.player_type == 'bot':
            volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
            sound = random.choice(LOSE_SOUNDS)
            sound.set_volume(volume)
            sound.play()
            pos = WIDTH / 2 - 300 * KOEF, HEIGHT / 2 - 150 * KOEF
            image = YouLose_image(pos)
            im.add(image)
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        running = False
                self.all_sprites.draw(self.screen)
                self.cards_sprites.draw(self.screen)
                im.draw(self.screen)
                im.update()
                pygame.display.flip()
                self.screen.fill(pygame.Color(0, 0, 0))
            sound.stop()
            pygame.mixer.music.set_volume(volume)
        if type(winner) == list:
            self.update()
            self.end_distribution(winner[0], player2=winner[1])
        else:
            self.update()
            self.end_distribution(winner)

    def open_bot_cards(self):
        for i in range(2):
            x = self.bot_place_sprites.sprites()[i].rect.x
            y = self.bot_place_sprites.sprites()[i].rect.y
            value = self.bot.cards[i].value
            suit = self.bot.cards[i].suit
            bot_card = Card(value, suit, (x, y))
            self.cards_sprites.add(bot_card)

    def add_sprites(self):  # Все спрайты на столе
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
        robot.image = pygame.transform.scale(self.robot_image, (int(w_card_k * 0.75), int(h_card_k * 0.75)))
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
        self.money_count = Counter(self.player.money, (WIDTH * 0.434, HEIGHT * 0.9, 250 * KOEF, 70 * KOEF), 100 * KOEF)
        self.all_sprites.add(self.money_count)
        self.bot_money_count = Counter(self.bot.money, (WIDTH * 0.313, HEIGHT * 0.23, 150 * KOEF, 60 * KOEF), 70 * KOEF)
        self.all_sprites.add(self.bot_money_count)
        self.bank_count = Counter(self.logic.bank, (WIDTH * 0.21, HEIGHT * 0.9, 250 * KOEF, 70 * KOEF), 100 * KOEF)
        self.all_sprites.add(self.bank_count)
        self.bot_bid_count = Counter(self.bot.bid, (WIDTH * 0.408, HEIGHT * 0.57, 150 * KOEF, 60 * KOEF), 70 * KOEF)
        self.all_sprites.add(self.bot_bid_count)
        self.player_bid_count = Counter(self.player.bid, (WIDTH * 0.514, HEIGHT * 0.57, 150 * KOEF, 60 * KOEF),
                                        70 * KOEF)
        self.all_sprites.add(self.player_bid_count)

    def start_mini_menu(self):
        self.mini_menu = Mini_menu(self)
        self.mini_menu.run(self)

    def end_distribution(self, player, player2=None):
        if player2:
            self.logic.end_distribution(player, player2=player2)
        else:
            self.logic.end_distribution(player)
        for elem in self.cards_sprites:
            elem.kill()


class Poker_graphic():
    def __init__(self):
        self.bank = 0
        self.table_cards = pygame.sprite.Group()
        self.players_cards = pygame.sprite.Group()

    def preflop(self, table, player_cards):
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
        fishka = Fishka((380 * KOEF, 645 * KOEF))
        table.cards_sprites.add(cards)
        table.cards_sprites.add(fishka)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    table.start_mini_menu()
            table.all_sprites.draw(table.screen)
            table.cards_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
            table.screen.fill(pygame.Color(0, 0, 0))
            if not any(list(map(lambda x: x.motion, cards.sprites()))):
                for i in range(2):
                    x = table.player_place_sprites.sprites()[i].rect.x
                    y = table.player_place_sprites.sprites()[i].rect.y
                    value = player_cards[i].value
                    suit = player_cards[i].suit
                    player_card = Card(value, suit, (x, y))
                    table.cards_sprites.add(player_card)
                    table.cards_sprites.draw(table.screen)
                    table.all_sprites.draw(table.screen)
                break

    def flop(self, table, table_cards):
        cards = pygame.sprite.Group()
        for i in range(3):
            card = Cards_back()
            x2 = table.table_place_sprites.sprites()[i].rect.x
            y2 = table.table_place_sprites.sprites()[i].rect.y
            x1 = table.koloda.rect.x
            y1 = table.koloda.rect.y
            card.get_trajectory((x1, y1), (x2, y2))
            cards.add(card)
        table.cards_sprites.add(cards)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    table.start_mini_menu()
            table.all_sprites.draw(table.screen)
            table.cards_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
            table.screen.fill(pygame.Color(0, 0, 0))
            if not any(list(map(lambda x: x.motion, cards.sprites()))):
                for i in range(3):
                    x = table.table_place_sprites.sprites()[i].rect.x
                    y = table.table_place_sprites.sprites()[i].rect.y
                    value = table_cards[i].value
                    suit = table_cards[i].suit
                    table_card = Card(value, suit, (x, y))
                    table.all_sprites.draw(table.screen)
                    table.cards_sprites.add(table_card)
                    table.cards_sprites.draw(table.screen)
                break

    def tern(self, table, table_cards):
        cards = pygame.sprite.Group()
        card = Cards_back()
        x2 = table.table_place_sprites.sprites()[-2].rect.x
        y2 = table.table_place_sprites.sprites()[-2].rect.y
        x1 = table.koloda.rect.x
        y1 = table.koloda.rect.y
        card.get_trajectory((x1, y1), (x2, y2))
        cards.add(card)
        table.cards_sprites.add(card)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    table.start_mini_menu()
            table.all_sprites.draw(table.screen)
            table.cards_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
            table.screen.fill(pygame.Color(0, 0, 0))
            if not any(list(map(lambda x: x.motion, cards.sprites()))):
                x = table.table_place_sprites.sprites()[-2].rect.x
                y = table.table_place_sprites.sprites()[-2].rect.y
                value = table_cards[-1].value
                suit = table_cards[-1].suit
                table_card = Card(value, suit, (x, y))
                table.all_sprites.draw(table.screen)
                table.cards_sprites.add(table_card)
                table.cards_sprites.draw(table.screen)
                break

    def river(self, table, table_cards):
        cards = pygame.sprite.Group()
        card = Cards_back()
        x2 = table.table_place_sprites.sprites()[-1].rect.x
        y2 = table.table_place_sprites.sprites()[-1].rect.y
        x1 = table.koloda.rect.x
        y1 = table.koloda.rect.y
        card.get_trajectory((x1, y1), (x2, y2))
        cards.add(card)
        table.cards_sprites.add(cards)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    table.start_mini_menu()
            table.all_sprites.draw(table.screen)
            table.cards_sprites.draw(table.screen)
            cards.update()
            pygame.display.flip()
            table.screen.fill(pygame.Color(0, 0, 0))
            if not any(list(map(lambda x: x.motion, cards.sprites()))):
                x = table.table_place_sprites.sprites()[-1].rect.x
                y = table.table_place_sprites.sprites()[-1].rect.y
                value = table_cards[-1].value
                suit = table_cards[-1].suit
                table_card = Card(value, suit, (x, y))
                table.all_sprites.draw(table.screen)
                table.cards_sprites.add(table_card)
                table.cards_sprites.draw(table.screen)
                break

    def bet(self, table, player, first_value, last_value):
        if first_value >= last_value:
            table.buttons[3].action = None
        else:
            table.buttons[3].action = lambda: self.reise(table, player, first_value, last_value)
        self.close_reise_flag = False
        self.go_bid = True
        while self.go_bid:
            table.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    table.start_mini_menu()
            table.all_sprites.draw(table.screen)
            table.cards_sprites.draw(table.screen)
            table.button_sprites.update()
            table.button_sprites.draw(table.screen)
            pygame.display.flip()
            table.clock.tick(FPS)
            if player.money == 0:
                self.go_bid = False

    def reise(self, table, player, first_value, last_value):
        table.buttons[3].action = self.close_reise
        slider = Slider(WIDTH * 0.75, HEIGHT * 0.88, 'vertical', 300 * KOEF, table)
        all_sprites = pygame.sprite.Group()
        all_sprites.add(slider.line, slider)
        counter = Counter(first_value, (WIDTH * 0.61, HEIGHT * 0.8, 250 * KOEF, 70 * KOEF), 100 * KOEF)
        all_sprites.add(counter)
        running = True
        while running:
            table.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    table.start_mini_menu()
            if self.close_reise_flag:
                running = False
            table.all_sprites.draw(table.screen)
            table.cards_sprites.draw(table.screen)
            table.button_sprites.update()
            table.button_sprites.draw(table.screen)
            all_sprites.update()
            all_sprites.draw(table.screen)
            table.clock.tick(FPS)
            pygame.display.flip()
            count = round((last_value - first_value) * slider.value + first_value)
            counter.gererate_count(count)
        if self.close_reise_flag:
            self.bet(table, player, first_value, last_value)
        else:
            player.reise(round((last_value - first_value) * slider.value + first_value))
            self.go_bid = False

    def close_reise(self):
        self.close_reise_flag = True
