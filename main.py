import pygame
import random
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)
pygame.init()

player_resize = [40,40]
player_image = "Sprites/player.png"
for i in range(10):
    enemy_images[i] = "Sprites/enemy" + i + ".png"
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
            self.rect.move_ip(0,-2.2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,2.2)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2.2,0)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2.2,0)

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
        self.surf = pygame.Surface((40,40))
        enemy_color = PickColor()
        if enemy_color == [0,0,0]:
            enemy_color = [255,255,255]
        elif enemy_color == [170,0,255]:
            enemy_color = [0,170,255]
        self.surf.fill((enemy_color[0],enemy_color[1],enemy_color[2]))
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
            self.speed = 1 + 0.7 * rand_pick
        elif rand_pick >= 5:
            self.speed = 1 + 0.4 * rand_pick
        
    def update(self):
        #move enemy at its speed to the left
        self.rect.move_ip(-self.speed,0)
        #Check for off screen
        if self.rect.right < 0:
            #kill() removes the sprite from every group its in
            self.kill()
#display screen
screen_width = 1200;
screen_height = 1000;
screen = pygame.display.set_mode((screen_width,screen_height))

# Custom event for adding new enemies
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 200)

circle_x, circle_y = screen_width / 2,screen_height / 2
inner_radius = 70
outer_radius = 75

#instantiate player from player class
player = Player() 

#Creating groups
#- enemies holds only enemy sprites'
#- all_sprites holds enemies and player, and renders
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

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
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    #black background
    screen.fill((0,0,0))
    
    #draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
    #Check for collisions between player and enemies
    if pygame.sprite.spritecollideany(player,enemies):
        # If the player collides with an enemy, they lose
        player.kill()
        running = False
    #flip everything to display
    pygame.display.flip()

pygame.quit()