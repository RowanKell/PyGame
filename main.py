import os.path

import pygame
import random
import numpy as np
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)
import pygame.freetype

pygame.init()

field_top = 0

font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts", "FuturaRenner-Regular.otf")
font_size = 50
pygame.freetype.init()
myfont = pygame.freetype.Font(font_path, font_size)

total_score = 0
player_speed = 5
player_resize = [40, 40]
player_image = "Sprites/player.png"
cloud_image = "Sprites/cloud.png"
enemy_images = np.array(["", "", "", "", "", "", "", "", "", "", ""], dtype=object)
for i in range(10):
    enemy_images[i] = "Sprites/enemy" + str(i) + ".png"


def pick_color():
    random_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
    return random_color


def round_down(num):
    rounded = round(num)
    if rounded > num:
        rounded = rounded + 1
    return rounded


def round_up(num):
    rounded = round(num)
    if rounded < num:
        rounded = rounded + 1
    return rounded


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(player_image).convert()
        self.surf = pygame.transform.scale(self.surf, player_resize)
        self.rect = self.surf.get_rect()

    def update(self, key_press):
        if key_press[K_UP]:
            self.rect.move_ip(0, -player_speed)
        if key_press[K_DOWN]:
            self.rect.move_ip(0, player_speed)
        if key_press[K_RIGHT]:
            self.rect.move_ip(player_speed, 0)
        if key_press[K_LEFT]:
            self.rect.move_ip(-player_speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < round_up(field_top):
            self.rect.top = round_up(field_top)
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()
        enemy_image = enemy_images[random.randint(0, 9)]
        self.surf = pygame.image.load(enemy_image)
        enemy_height = 2 * self.surf.get_height()
        enemy_width = 2 * self.surf.get_width()
        enemy_resize = [enemy_height, enemy_width]
        self.surf = pygame.transform.scale(self.surf, enemy_resize)
        self.rect = self.surf.get_rect(
            # random starting position
            center=(
                random.randint(screen_width + 10, screen_width + 20),
                random.randint(round_up(field_top + enemy_height / 2), round_down(screen_height - enemy_height / 2)),
            )
        )
        # random speed
        rand_pick = random.randint(1, 10)
        if rand_pick < 5:
            self.speed = 1 + 1.2 * rand_pick
        elif rand_pick >= 5:
            self.speed = 1 + 1 * rand_pick
        self.enemies_passed = 0
        self.score = 0
        self.scorelimit = 0

    def score_count(self):
        if self.rect.right < 1:
            self.scorelimit += 1
            if self.scorelimit == 1:
                self.score = 1
            else:
                self.score = 0

    def update(self):
        # move enemy at its speed to the left
        self.rect.move_ip(-self.speed, 0)
        # Check for off-screen
        if self.rect.right < 0:
            # kill() removes the sprite from every group its in
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(cloud_image)
        cloud_resize = [150, 100]
        self.surf = pygame.transform.scale(self.surf, cloud_resize)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(screen_width - 20, screen_width),
                random.randrange(0, screen_height, 100)
            )
        )
        self.speed = 3

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


def stats(score):
    score_board_text = "Score: " + str(score)
    score_board_size = 64
    myfont_rect = myfont.get_rect(score_board_text, size=score_board_size)
    text_width = myfont_rect.right - myfont_rect.left
    text_height = myfont_rect.bottom - myfont_rect.top
    score_board = pygame.Surface((text_width + 60, text_height + 40))
    score_board_center = ((screen_width / 2), 40 + text_height / 2)
    score_board_rect = score_board.get_rect(
        center=score_board_center
    )
    score_board_border = pygame.Surface((text_width + 80, text_height + 60))
    score_board_border_rect = score_board_border.get_rect(
        center=score_board_center
    )
    global field_top
    field_top = score_board_border_rect.bottom
    pygame.draw.rect(screen, (0, 0, 50), score_board_border_rect)
    pygame.draw.rect(screen, (50, 50, 200), score_board_rect)

    myfont.render_to(screen, (score_board_center[0] - text_width / 2, score_board_center[1] - text_height / 2),
                     score_board_text, (255, 255, 255), None, size=score_board_size)


# display screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Custom event for adding new enemies
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 300)

# Custom event for clouds
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 5000)

# instantiate player from player class
player = Player()

# Creating groups
# - enemies holds only enemy sprites'
# - all_sprites holds enemies and player, and renders
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

enemylist = []
# Setup clock to control framerate
clock = pygame.time.Clock()

# Run game unless user stops
running = True
while running:
    for event in pygame.event.get():
        # is the user pressing a key
        if event.type == KEYDOWN:
            # is the key the escape key
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:  # stops game if window is closed
            running = False
        # add enemy
        elif event.type == ADDENEMY:
            # make new enemy and add to sprite group
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            enemylist.append(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    immune = False
    for enemy in enemylist:
        enemy.score_count()
        total_score += enemy.score
    pressed_key = pygame.key.get_pressed()
    player.update(pressed_key)
    enemies.update()
    clouds.update()
    # black background
    screen.fill((135, 206, 250))

    # draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    # Check if player is hiding in cloud, and give immunity if so
    if pygame.sprite.spritecollideany(player, clouds):
        immune = True
    # check for collision between player and enemy, don't kill if immune
    if pygame.sprite.spritecollideany(player, enemies):
        if not pygame.sprite.spritecollideany(player, clouds):
            player.kill()
            running = False
    stats(total_score)
    # flip everything to display
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
