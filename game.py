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
        self.robot_image = pygame.transform.scale(robot_image, (int(robot_image.get_width() * (WIDTH / 1920)),
                                                                int(robot_image.get_height() * (WIDTH / 1920))))
        self.koloda_image = pygame.transform.scale(koloda_image, (int(koloda_image.get_width() * (WIDTH / 1920)),
                                                                 int(koloda_image.get_height() * (WIDTH / 1920))))

        self.buttons = [Button('Ва Банк', (1550, 750), termit),
                        Button('Колл', (1550, 825), termit),
                        Button('Пас', (1550, 900), termit),
                        Button('Чек', (1550, 675), termit)]
        self.all_sprites.add(self.buttons)
        self.button_sprites.add(self.buttons)
        self.add_sprites()


    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                for btn in self.buttons:
                    btn.draw()
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def add_sprites(self):
        koef = WIDTH / 1920
        w_card = Place_from_card.image.get_width()
        h_card = Place_from_card.image.get_height()
        left_top = (1920 * koef - (w_card * 5 + 40 * koef * 4)) // 2
        up_top = (1080 * koef - h_card) // 4
        for i in range(5):
            pos = left_top + i * w_card + i * 40 * koef, up_top + 175
            place = Place_from_card(pos)
            self.all_sprites.add(place)
            self.table_place_sprites.add(place)

        left_top = (1920 * koef - (w_card * 2 + 40 * koef)) // 2
        up_top = 1080 * koef - (1080 * koef - h_card) // 4 - h_card
        for i in range(2):
            pos = left_top + i * w_card + i * 40 * koef, up_top + 75
            place = Place_from_card(pos)
            self.all_sprites.add(place)
            self.player_place_sprites.add(place)

        w_card_k = int(Place_from_card.image.get_width())
        h_card_k = int(Place_from_card.image.get_height())
        left_top = (1920 * koef - (w_card_k * 2 + 40 * koef)) // 2
        up_top = ((1080 * koef - h_card) // 4 - h_card_k) // 2
        for i in range(2):
            pos = left_top + i * w_card_k + i * 40 * koef, up_top + 75
            place = Place_from_card(pos)
            self.all_sprites.add(place)
            self.bot_place_sprites.add(place)

        robot = pygame.sprite.Sprite(self.all_sprites)
        robot.image = pygame.transform.scale(self.robot_image, (w_card_k, h_card_k))
        robot.rect = self.robot_image.get_rect()

        up_top = ((1080 * koef - h_card) // 4 - h_card_k) // 2 + 75
        left_top = (1920 * koef - (w_card_k * 2 + 40 * koef)) // 2 - w_card_k * 1.25
        robot.rect.x = left_top
        robot.rect.y = up_top

        koloda = pygame.sprite.Sprite(self.all_sprites)
        koloda.image = pygame.transform.scale(self.koloda_image, (w_card_k, h_card_k))
        koloda.rect = self.koloda_image.get_rect()

        up_top = 390
        left_top = 150
        koloda.rect.x = left_top
        koloda.rect.y = up_top


class Game_graphic():
    def __init__(self):
        pass

    def update(self):
        pass


if __name__ == '__main__':
    game = Game()
    game.run()
