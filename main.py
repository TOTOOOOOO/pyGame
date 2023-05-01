import pygame
import random
import math

from pygame import mixer

pygame.init()


screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("cuftalica peek")
icon = pygame.image.load('space.png')
background = pygame.image.load('background.png')


#background music
mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_icon(icon)


# score text
score_value = 0
font = pygame.font.Font('customFont.ttf' ,32)
textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('customFont.ttf', 64)
over_font1 = pygame.font.Font('customFont.ttf',16)

def game_over():

    run = True
    while run:
        over_text = over_font.render("GAME OVER", True, (255,255,255))
        over_text1 = over_font1.render("PRESS ANY KEY TO RESTART", True,(255,255,255))
        screen.blit(over_text, (125,250))
        screen.blit(over_text1,(220,350))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        player(playerX,playerY)
        show_score(textX,textY)
        pygame.display.update()

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True,(255,255,255))
    screen.blit(score,(x,y))

#player
playerImg = pygame.image.load('space.png')
playerX = 20
playerY = 300
vel = 2

enemyImg = []
enemyX = []
enemyY = []
enemy_xchange = []
enemy_ychange = []
num_of_enemies = 3
enemy_size = 64

igraci = []
igraci.append('alien.png')
igraci.append('alien.png')
igraci.append('alien.png')


for i in range(num_of_enemies):
    
    enemyImg.append(pygame.image.load(igraci[i]))
    enemyX.append(random.randint(650,800-enemy_size))
    enemyY.append(random.randint(0,600-enemy_size))
    enemy_xchange.append(50) 
    enemy_ychange.append(1.5)
    

bulletImg = pygame.image.load('bullet.png')
bulletX = 20
bulletY = 300
bullet_xchange = 5
bullet_state = "ready"

run = True

def player(x,y):
    screen.blit(playerImg, (x,y))
    
def enemy(x,y, i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+64,y + 15))


def isCollision(enemyX, enemyY, bulletX, bulletY, i):
    if enemyImg[i].get_rect(x = enemyX, y= enemyY).colliderect(bulletImg.get_rect(x = bulletX, y = bulletY)):    
        return True
    return False

    #drugi nacin za collision
    # distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    # if distance < 27:
    #     return True
    # return False


def mainMenu():
    
    pom = True
    while pom:
        screen.fill("black")
        screen.blit(background,(0,0))

        tekst = font.render("PRESS SPACE TO PLAY", True, (255,255,255))
        screen.blit(tekst,(110,250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        if keys[pygame.K_SPACE]:
            pom = False; 
        
        pygame.display.update()


mainMenu()
#glavna petlja
while run:

    #background
    screen.fill("black")
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        
    if keys[pygame.K_UP]:
        playerY -= vel
        if playerY  < 0:
            playerY = 0
    if keys[pygame.K_DOWN]:
        playerY += vel 
        if playerY >= 600 - 72: 
            playerY = 600 - 72

    if keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_sound = mixer.Sound('laser.wav')
        bullet_sound.play()
        bulletY = playerY
        fire_bullet(bulletX,bulletY)
   
    #granice za enemy i collision za enemy

    for i in range(num_of_enemies):

        # game over

        if enemyX[i] < 500:
            for j in range(num_of_enemies):
                enemyX[j] = -100
            
            game_over()
            break   


        #kretnja protivnika
          
        enemyY[i] += enemy_ychange[i]

        if enemyY[i] <= 0:
            enemy_ychange[i] = 1.5
            enemyX[i] -= enemy_xchange[i]

        elif enemyY[i] >= 600-enemy_size:
            enemy_ychange[i] = -1.5
            enemyX[i] -= enemy_xchange[i]
        

        #kolizija

        collision = isCollision(enemyX[i],enemyY[i], bulletX, bulletY, i)
        if collision:
            
            #sound for collision
            # explosion_sound = mixer.Sound('explosion.wav')
            # explosion_sound.play()
            bulletX = 20
            bullet_state = "ready"
            score_value +=1
            enemyX[i] = random.randint(650,800-enemy_size)
            enemyY[i] = random.randint(0,600 - enemy_size)
        
        enemy(enemyX[i], enemyY[i],i)
        

    #bullet movement
    if bulletX >= 800 - 32:
        bulletX = 20
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX,bulletY)
        bulletX += bullet_xchange


    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()

pygame.quit()