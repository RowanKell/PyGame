import pygame
import random
import numpy as np
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)
pygame.init()

player_speed = 5
player_resize = [40,40]
player_image = "Sprites/player.png"
cloud_image = "Sprites/cloud.png"
enemy_images = np.array(["","","","","","","","","","",""], dtype=object)
for i in range(10):
    enemy_images[i] = "Sprites/enemy" + str(i) + ".png"
def PickColor():
    random_color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    return random_color
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(player_image).convert()
        self.surf = pygame.transform.scale(self.surf,player_resize)
        self.rect = self.surf.get_rect()
        
    def update(self,pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-player_speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,player_speed)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(player_speed,0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-player_speed,0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        for i in enemy_images:
            enemy_image = enemy_images[random.randint(0,9)]
        self.surf = pygame.image.load(enemy_image)
        enemy_height = 2 * self.surf.get_height()
        enemy_width = 2 * self.surf.get_width()
        enemy_resize = [enemy_height,enemy_width]
        self.surf = pygame.transform.scale(self.surf,enemy_resize)
        self.rect = self.surf.get_rect(
            #random starting position
            center = (
                random.randint(screen_width + 10, screen_width + 20),
                random.randint(0, screen_height),
            )
        )
        #random speed
        rand_pick = random.randint(1,10)
        if rand_pick < 5:
            self.speed = 1 + 1.2 * rand_pick
        elif rand_pick >= 5:
            self.speed = 1 + 1 * rand_pick
        
    def update(self):
        #move enemy at its speed to the left
        self.rect.move_ip(-self.speed,0)
        #Check for off screen
        if self.rect.right < 0:
            #kill() removes the sprite from every group its in
            self.kill()
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud,self).__init__()
        self.surf = pygame.image.load(cloud_image)
        cloud_resize = [150, 100]
        self.surf = pygame.transform.scale(self.surf,cloud_resize)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(screen_width - 20, screen_width),
                random.randrange(0, screen_height, 100)
            )
        )
        self.speed = 3
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
#display screen
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width,screen_height))

# Custom event for adding new enemies
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 300)

# Custom event for clouds
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 5000)

#instantiate player from player class
player = Player() 

#Creating groups
#- enemies holds only enemy sprites'
#- all_sprites holds enemies and player, and renders
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup clock to control framerate
clock = pygame.time.Clock()

#Run game unless user stops
running = True; 
while running:
    for event in pygame.event.get():
        #is the user pressing a key
        if event.type == KEYDOWN:
            #is the key the escape key
            if event.key == K_ESCAPE:
                running = False
                
        elif event.type == QUIT: #stops game if window is closed
            running = False
        #add enemy
        elif event.type == ADDENEMY:
            #make new enemy and add to sprite group
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
    
    immune = False
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()
    #black background
    screen.fill((135, 206, 250))
    
    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
    #Check if player is hiding in cloud, and give immunity if so
    if pygame.sprite.spritecollideany(player, clouds):
        immune = True
    #check for collision between player and enemy, don't kill if immune
    if pygame.sprite.spritecollideany(player, enemies) and immune == False:
        # If the player collides with an enemy, they lose
        player.kill()
        running = False
    #flip everything to display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()