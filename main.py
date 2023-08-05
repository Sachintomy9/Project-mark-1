import math
import random
import pygame
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")
#sound
mixer.music.load("background1.wav")
mixer.music.play(-1)
# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("001-rocket.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("001-spaceship.png")
playerx = 370
playery = 480
playerx_change = 0

# enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("001-ufo.png"))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 150))
    enemyx_change.append(4)
    enemyy_change.append(40)

# bullet
# ready-u cant see, fire-bullet moving
bulletImg = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bulletx_change = 6
bullety_change = 10
bullet_state = "ready"


#score
score_value  = 0
font = pygame.font.Font("freesansbold.ttf",32)
textx = 10
testy = 10

#game over
over_font=pygame.font.Font("freesansbold.ttf",64)
def show_score(x,y):
    score = font.render("Score :"+ str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = font.render("GAME OVER :" + str(score_value), True, (255, 255, 255))
    screen.blit(over_text,(200,250))
    
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt(((enemyx - bulletx) ** 2) + ((bullety - enemyy) ** 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key stroke is pressed , check left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -5
            if event.key == pygame.K_RIGHT:
                playerx_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # get the current x coordinate of the spaceship
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerx_change = 0
            if event.key == pygame.K_RIGHT:
                playerx_change = 0

    # boundry limits

    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    #enemy movement
    for i in range(num_of_enemies):

        #game over
        if enemyy[i] >440:
            for j in range(num_of_enemies):
                enemyy[j]= 2000
            game_over_text()
            break

        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:
            enemyx_change[i] = 4
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 736:
            enemyx_change[i] = -4
            enemyy[i] += enemyy_change[i]

        # collision
        collision = isCollision(enemyx[i], enemyy[i], bulletx, bullety)
        if (collision == True):
            collision_sound=mixer.Sound("explosion.wav")
            collision_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)

        enemy(enemyx[i], enemyy[i],i)

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bulletx_change

    show_score(textx,testy)

    player(playerx, playery)

    pygame.display.update()
