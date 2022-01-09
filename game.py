import pygame.sprite

from functions import *


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
            player.cards.append(self.deck.pop())
            player.cards.append(self.deck.pop())

    def flop(self):
        self.table_cards.append(self.deck.pop())
        self.table_cards.append(self.deck.pop())
        self.table_cards.append(self.deck.pop())

    def tern(self):
        self.table_cards.append(self.deck.pop())

    def river(self):
        self.table_cards.append(self.deck.pop())


class Game():
    def __init__(self):
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

        self.buttons = [Button('Пас', (WIDTH * 0.75, HEIGHT * 0.75 - 15 * KOEF), (400, 60), termit),
                        Button('Чек', (WIDTH * 0.75, HEIGHT * 0.75 + 55 * KOEF), (400, 60), termit),
                        Button('Ва-Банк', (WIDTH * 0.75, HEIGHT * 0.75 + 125 * KOEF), (400, 60), termit),
                        Button('Райс', (WIDTH * 0.75, HEIGHT * 0.75 - 85 * KOEF), (400, 60), termit),
                        Button('Колл', (WIDTH * 0.75, HEIGHT * 0.75 - 155 * KOEF), (400, 60), termit)]
        self.all_sprites.add(self.buttons)
        self.button_sprites.add(self.buttons)
        self.add_sprites()


    def run(self):
        self.running = True
        self.graph = Poker_graphic()
        self.graph.preflop(self)
        self.graph.flop(self)
        self.graph.tern(self)
        self.graph.river(self)
        while self.running:
            for event in pygame.event.get():
                for btn in self.buttons:
                    btn.draw()
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
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
            table.screen.fill(pygame.Color(0, 0, 0))
            table.all_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
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
            table.screen.fill(pygame.Color(0, 0, 0))
            table.all_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
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
            table.screen.fill(pygame.Color(0, 0, 0))
            table.all_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
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
            table.screen.fill(pygame.Color(0, 0, 0))
            table.all_sprites.draw(table.screen)
            cards.draw(table.screen)
            cards.update()
            pygame.display.flip()
            if not any(list(map(lambda x: x.motion, cards.sprites()))):
                break

if __name__ == '__main__':
    game = Game()
    game.run()

