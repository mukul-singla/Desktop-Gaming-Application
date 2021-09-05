import pygame
import random
import  math
from pygame import mixer


def space_game():
    # initialize the game
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((800, 600),pygame.RESIZABLE )

    # Background
    background = pygame.image.load('gallery/Space Invader/background.png')

    # Background sound
    mixer.music.load('gallery/Space Invader/background.wav')
    mixer.music.play(-1)

    # Title and icon
    pygame.display.set_caption('Space Invaders')
    icon = pygame.image.load('gallery/Space Invader/ufo.png')
    pygame.display.set_icon(icon)

    # Player
    playerImg = pygame.image.load('gallery/Space Invader/player.png')
    playerX = 370
    playerY = 480
    playerX_change = 0

    # Enemy
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = 40
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('gallery/Space Invader/enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(2)
    # Bullet

    # Ready - You can't see the bullet on the screen
    # Fire - The bullet is currently moving
    bulletImg = pygame.image.load('gallery/Space Invader/bullet.png')
    bulletX = 0
    bulletY = 480
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"

    # Score
    score_value=0
    font = pygame.font.Font('freesansbold.ttf',32)

    textX = 10
    textY =10

    # Game over text
    over_font = pygame.font.Font('freesansbold.ttf',64)

    def show_score(x,y):
        score = font.render("Score: " + str(score_value), True,(255,255,255))
        screen.blit(score,(x,y))

    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))


    def player(x, y):
        screen.blit(playerImg, (x, y))


    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))


    def fire_bullet(x,y):
        nonlocal bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg,(x+16,y+10))


    def isCollision(enemyX,enemyY,bulletX,bulletY):
        distance = math.sqrt(math.pow(bulletX-enemyX,2) + math.pow(bulletY-enemyY,2))
        if distance<27:
            return True
        else:
            return False

    # Game loop
    running = True
    while running:
        # RGB - Red,Green,Blue
        screen.fill((0, 0, 0))
        # Background image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -2.5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 2.5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX=playerX
                        bullet_sound = mixer.Sound('gallery/Space Invader/laser.wav')
                        mixer.Sound.play(bullet_sound)
                        fire_bullet(bulletX,bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # Checking for boundaries for our spaceship
        playerX += playerX_change
        if playerX < 0:
            playerX = 0
        if playerX > 736:
            playerX = 736

        # Enemy movement:
        for i in range(num_of_enemies):
            # Game Over
            if enemyY[i]>440:
                for j in range(num_of_enemies):
                    enemyY[j]=500
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 2
                enemyY[i] += enemyY_change
            elif enemyX[i] >= 736:
                enemyX_change[i] = -2
                enemyY[i] += enemyY_change

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('gallery/Space Invader/explosion.wav')
                mixer.Sound.play(explosion_sound)
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        #Bullet Movement
        if bulletY<0:
            bulletY = 480
            bullet_state= "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX,bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX,textY)

        pygame.display.update()

if __name__ == '__main__':
    space_game()