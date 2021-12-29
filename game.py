from functions import *


pygame.init()


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
        self.robot_image = pygame.transform.scale(robot_image, (int(robot_image.get_width() * (WIDTH / 1920)),
                                                                int(robot_image.get_height() * (WIDTH / 1920))))
        self.add_sprites()
        self.deck = self.full_deck()
        self.card_sprites = pygame.sprite.Group()


    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
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
            pos = left_top + i * w_card + i * 40 * koef, up_top
            place = Place_from_card(pos)
            self.all_sprites.add(place)
            self.table_place_sprites.add(place)

        left_top = (1920 * koef - (w_card * 2 + 40 * koef)) // 2
        up_top = 1080 * koef - (1080 * koef - h_card) // 4 - h_card
        for i in range(2):
            pos = left_top + i * w_card + i * 40 * koef, up_top
            place = Place_from_card(pos)
            self.all_sprites.add(place)
            self.player_place_sprites.add(place)

        k_card = 0.75
        w_card_k = int(Place_from_card.image.get_width() * k_card)
        h_card_k = int(Place_from_card.image.get_height() * k_card)
        left_top = (1920 * koef - (w_card_k * 2 + 40 * koef)) // 2
        up_top = ((1080 * koef - h_card) // 4 - h_card_k) // 2
        for i in range(2):
            pos = left_top + i * w_card_k + i * 40 * koef, up_top
            place = Place_from_card(pos)
            place.resize(k_card)
            self.all_sprites.add(place)
            self.bot_place_sprites.add(place)

        robot = pygame.sprite.Sprite(self.all_sprites)
        robot.image = pygame.transform.scale(self.robot_image, (w_card_k, h_card_k))
        robot.rect = self.robot_image.get_rect()

        up_top = ((1080 * koef - h_card) // 4 - h_card_k) // 2
        left_top = (1920 * koef - (w_card_k * 2 + 40 * koef)) // 2 - w_card_k * 1.25
        robot.rect.x = left_top
        robot.rect.y = up_top


    def full_deck(self):
        self.card_sprites = pygame.sprite.Group()
        values = ['2', '3', '4', '5', '6', '7', '8', '9',
                  '10', 'J', 'Q', 'K', 'A']
        suits = ['krest', 'pik', 'cherv', 'bubn']
        deck = []
        for suit in suits:
            for value in values:
                deck.append(Card(value, suit, (-1000, -1000)))
        random.shuffle(deck)
        self.card_sprites.add(deck)
        return deck

if __name__ == '__main__':
    game = Game()
    game.run()
