import pygame
import random
import pymysql

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
screen_size = (600, 700)

screen = pygame.display.set_mode(screen_size)
cards = pygame.sprite.Group()

level = 1

image1 = 'pikachu.jpg'
image2 = 'pinkbean.png'
image3 = 'fork.jpg'
image4 = "car.jpg"
image5 = "food.jpg"
image6 = "money.jpg"
image7 = "study.jpg"
image8 = "sun.jpg"

IMAGES = [[pygame.image.load(image1).convert(), image1],
          [pygame.image.load(image2).convert(), image2],
          [pygame.image.load(image3).convert(), image3],
          [pygame.image.load(image4).convert(), image4],
          [pygame.image.load(image5).convert(), image5],
          [pygame.image.load(image6).convert(), image6],
          [pygame.image.load(image7).convert(), image7],
          [pygame.image.load(image8).convert(), image8]]

coords = [[50, 50], [200, 50], [350, 50], [50, 175], [200, 175], [350, 175],
          [50, 300], [200, 300], [350, 300], [50, 425], [200, 425], [350, 425]]

real_coords = coords[:level * 6]

con = pymysql.connect(host="localhost", user="root",
                      password="carry_to_internship247",
                      db="my_database")

cursor = con.cursor()


class Card(pygame.sprite.Sprite):
    """A card sprite
    === Attributes ===
    name: the name of the card (Ex: pikachu, fork)
    image: the image loaded for the card
    save_image: duplicate of the iamge created for show_image() method
    rect: stores the pygame.Rect object of the image
    rect.x, rect.y: the x, y coordinate of the card
    locx, locy: duplicate of the x, y coordinate created for hide_image()
                and show_image() methods
    """

    def __init__(self, image, x, y):
        """Initialize the card"""

        super().__init__()

        self.name = image[1]

        self.image = image[0]
        self.save_image = image[0]

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.locx = x
        self.locy = y

    def hide_image(self):
        """Hide the image of the card from the screen"""

        self.image = pygame.Surface([100, 50])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = self.locx
        self.rect.y = self.locy

    def show_image(self):
        """Show the image of the card on the screen"""

        self.image = self.save_image

        self.rect = self.image.get_rect()
        self.rect.x = self.locx
        self.rect.y = self.locy

    def new_loc(self, index):
        """Moves the card to a new location"""

        self.locx = real_coords[index][0]
        self.locy = real_coords[index][1]


def randomize(cards):
    """Mix up the locations of the cards"""
    index = 0
    for card in cards:
        card.rect.x = real_coords[index][0]
        card.rect.y = real_coords[index][1]
        card.new_loc(index)
        index += 1


def update_score(count, screen):
    """Update the score of the time"""
    if count >= frame * 4 + 7:
        score = font.render(str((count-67) // frame), 1, WHITE)
        screen.blit(score, (screen_size[0] - 100, 25))


def show_result(screen, duplicate_list):
    """Once the player chose two cards, show the result"""

    global timer, result

    if result != "":
        message = font.render(result, 1, WHITE)
        screen.blit(message, (screen_size[0] - 100, 55))
        timer += 1
        if timer > message_duration:
            timer = 0
            if result == "Failed!":
                duplicate_list[0].hide_image()
                duplicate_list[1].hide_image()
            duplicate_list.clear()
            result = ""


def show_gameover(screen, count):
    """Once player finishes game, show the final
    time score"""

    end_score_message = str((count - 67) // frame) + " is your score! "
    gameover_message = font.render(end_score_message, 1, WHITE)
    screen.blit(gameover_message, (screen_size[0] // 2, 2 * screen_size[1] // 3))


def reset_game(success_cards):
    """Reset the game settings for a
    game restart"""
    success_cards.clear()
    return 0, False, False


def draw_buttons(screen, restart, record, next_level):
    """Draw buttons once the game is over"""
    pygame.draw.rect(screen, RED, restart)
    screen.blit(restart_text, (screen_size[0] // 3, screen_size[1] - 50))
    pygame.draw.rect(screen, RED, record)
    screen.blit(record_text, (screen_size[0] // 3 + button_width + 10,
                              screen_size[1] - 50))
    pygame.draw.rect(screen, RED, next_level)
    screen.blit(next_level_text, (screen_size[0] // 3 + 3 * button_width,
                                  screen_size[1] - 50))


def record_score(cur, score, frame, con):

    name = input("Enter your name: ")
    final_score = (score - 67) // frame

    add_sql = "INSERT INTO users VALUES ('{}', '{}');".format(name, final_score)

    cur.execute(add_sql)

    con.commit()


def update_level(cards, lvl, coordinates):
    cards.empty()
    for k in range(lvl * 3):
        IMAGES[k][0] = pygame.transform.scale(IMAGES[k][0], (100, 50))
        cards.add(Card(IMAGES[k], coordinates[k][0], coordinates[k][1]))
        cards.add(Card(IMAGES[k], coordinates[k + 3][0], coordinates[k + 3][1]))


for c in range(3):
    IMAGES[c][0] = pygame.transform.scale(IMAGES[c][0], (100, 50))
    cards.add(Card(IMAGES[c], real_coords[c][0], real_coords[c][1]))
    cards.add(Card(IMAGES[c], real_coords[c+3][0], real_coords[c+3][1]))

pygame.display.set_caption("Card Game")

count = 0
frame = 20
message_duration = frame / 2
timer = 0
elapsed = 0

result = ""

revealed_num = 0
revealed_cards = []
success_cards = []
duplicate_list = []

font = pygame.font.SysFont("monospace", 20)

ready_label = font.render("Ready?", 1, WHITE)
restart_text = font.render("Restart", 1, WHITE)
record_text = font.render("Record Score", 1, WHITE)
next_level_text = font.render("Next Level", 1, WHITE)


button_width = 90
button_height = 50

restart_button = pygame.Rect((screen_size[0] // 3, screen_size[1] - 80),
                             (button_width, button_height))

record_button = pygame.Rect((screen_size[0] // 3 + button_width + 10,
                             screen_size[1] - 80), (button_width + 30,
                                                    button_height))

next_level_button = pygame.Rect((screen_size[0] // 3 + button_width * 3,
                                 screen_size[1] - 80),
                                (button_width, button_height))

clock = pygame.time.Clock()

recorded = False
con_to_db = False
game_over = False
done = False

while not done:

    clock.tick(frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if not game_over:
                for card in cards:
                    if count >= 68 and card.rect.collidepoint(pos):
                        card.show_image()
                        if card not in success_cards \
                                and card not in revealed_cards:
                            revealed_cards.append(card)
                            revealed_num += 1
            else:
                if restart_button.collidepoint(pos):
                    count, game_over, recorded = reset_game(success_cards)

                elif not recorded and record_button.collidepoint(pos):
                    record_score(cursor, count, frame, con)

                    recorded = True

                elif level < 2 and next_level_button.collidepoint(pos):

                    level += 1
                    real_coords = coords[:level * 6]
                    update_level(cards, level, real_coords)

                    count, game_over, recorded = reset_game(success_cards)

    if revealed_num == 2:
        duplicate_list = revealed_cards[:]
        if revealed_cards[0].name == revealed_cards[1].name:
            result = "Success!"
            success_cards.extend(revealed_cards)
        else:
            result = "Failed!"
        revealed_num = 0
        revealed_cards.clear()

    if count == frame * 3:
        random.shuffle(real_coords)
        randomize(cards)

    if count == frame * 3 + 7:
        for card in cards:
            card.hide_image()

    screen.fill(BLACK)

    if count <= frame * 3:
        screen.blit(ready_label, (screen_size[0] // 3, 25))

    cards.draw(screen)

    update_score(count, screen)

    show_result(screen, duplicate_list)

    if len(success_cards) == len(cards):
        show_gameover(screen, count)
        game_over = True
    else:
        count += 1

    if game_over:
        draw_buttons(screen, restart_button, record_button, next_level_button)

    pygame.display.flip()

pygame.quit()
