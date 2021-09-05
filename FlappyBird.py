import random
import sys
import pygame
from pygame.locals import *

# Global variables for game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
GROUNDY = SCREENHEIGHT*0.8
GAME_SPIRITS = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/Flappy Bird/sprites/bird.png'
BACKGROUND = 'gallery/Flappy Bird/sprites/background.png'
PIPE = 'gallery/Flappy Bird/sprites/pipe.png'

def flappy_game():
    # game will start from here
    pygame.init()
    pygame.display.set_caption('Flappy Bird by Mukul')
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)

    # Game spirits
    GAME_SPIRITS['numbers'] = (
        pygame.image.load('gallery/Flappy Bird/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/Flappy Bird/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/Flappy Bird/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/Flappy Bird/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/Flappy Bird/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/Flappy Bird/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/Flappy Bird/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/Flappy Bird/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/Flappy Bird/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/Flappy Bird/sprites/9.png').convert_alpha()
    )

    GAME_SPIRITS['message'] = pygame.image.load('gallery/Flappy Bird/sprites/message.png').convert_alpha()
    GAME_SPIRITS['base'] = pygame.image.load('gallery/Flappy Bird/sprites/base.png').convert_alpha()
    GAME_SPIRITS['pipe'] =(
        pygame.transform.rotate(pygame.image.load('gallery/Flappy Bird/sprites/pipe.png').convert_alpha(),180),
        pygame.image.load('gallery/Flappy Bird/sprites/pipe.png').convert_alpha()
        )


    # Game sound
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/Flappy Bird/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/Flappy Bird/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/Flappy Bird/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/Flappy Bird/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/Flappy Bird/audio/wing.wav')

    GAME_SPIRITS['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPIRITS['player'] = pygame.image.load(PLAYER).convert_alpha()

    def welcomeScreen():
        """
        Shows welcome images on screen
        """
        playerx = int(SCREENWIDTH/5)
        playery = int((SCREENHEIGHT-GAME_SPIRITS['player'].get_height())/2)
        messsagex = int((SCREENWIDTH - GAME_SPIRITS['message'].get_width())/2)
        messsagey = int(SCREENHEIGHT*0.13)
        basex=0

        while True:
            for event in pygame.event.get():
                # If user clicks on quit button, close the game
                if event.type==QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                # If use presses up or or start key, start the game
                elif event.type==KEYDOWN and(event.key == K_SPACE or event.key == K_UP):
                    return
                else:
                    SCREEN.blit(GAME_SPIRITS['background'],(0,0))
                    SCREEN.blit(GAME_SPIRITS['player'], (playerx, playery))
                    SCREEN.blit(GAME_SPIRITS['message'], (messsagex,messsagey))
                    SCREEN.blit(GAME_SPIRITS['base'], (basex, GROUNDY))
                    pygame.display.update()
                    FPSCLOCK = pygame.time.Clock()
                    FPSCLOCK.tick(FPS)


    def mainGame():
        score=0
        playerx = int(SCREENWIDTH/5)
        playery = int(SCREENWIDTH/2)
        basex=0

        # Create 2 pipes for blitting on screen

        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()


        #my list of upperpipes
        upperPipes =[
            {'x': SCREENWIDTH+200, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']},
        ]

        # my list of lowerpipes
        lowerPipes = [
            {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        pipeVelX = -4

        playerVelY = -9
        playerMaxVelY = 10
        playerMinVelY = -8
        playerAccY = 1

        playerFlapAccv = -8  # velocity while flapping
        playerFlapped = False  # It is true only when the bird is flapping

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key==K_UP or event.key==K_SPACE):
                    if playery>0:
                        playerVelY = playerFlapAccv
                        playerFlapped=True
                        GAME_SOUNDS['wing'].play()

            crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)
            # This function will return true if the player is crashed
            if crashTest:
                return

            # Check for score
            playerMidPos = playerx + GAME_SPIRITS['player'].get_width()/2
            for pipe in upperPipes:
                pipeMidPos = pipe['x'] + GAME_SPIRITS['pipe'][0].get_width()/2
                if pipeMidPos<= playerMidPos < pipeMidPos + 4:
                    score += 1
                    print(f"Your score is {score}")
                    GAME_SOUNDS['point'].play()

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            playerHeight = GAME_SPIRITS['player'].get_height()
            playery = playery + min(playerVelY,GROUNDY-playerHeight-playery)

            # move pipes to left
            for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # Add a new pipe when the first is about to cross the leftmost part of the screen
            if 0<upperPipes[0]['x']<5:
                newPipe = getRandomPipe()
                upperPipes.append(newPipe[0])
                lowerPipes.append(newPipe[1])

            # if the pipe is out of the screen, remove it
            if upperPipes[0]['x'] < -GAME_SPIRITS['pipe'][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

            # Lets blit our sprites now
            SCREEN.blit(GAME_SPIRITS['background'],(0,0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_SPIRITS['pipe'][0],(upperPipe['x'],upperPipe['y']))
                SCREEN.blit(GAME_SPIRITS['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
            SCREEN.blit(GAME_SPIRITS['base'], (basex, GROUNDY))
            SCREEN.blit(GAME_SPIRITS['player'], (playerx, playery))

            myDigits = [int(x) for x in list(str(score))]
            width=0
            for digit in myDigits:
                width += GAME_SPIRITS['numbers'][digit].get_width()/2
            Xoffset = (SCREENWIDTH-width)/2

            for digit in myDigits:
                SCREEN.blit(GAME_SPIRITS['numbers'][digit], (Xoffset,SCREENHEIGHT*0.12))
                Xoffset += GAME_SPIRITS['numbers'][digit].get_width()
            pygame.display.update()
            FPSCLOCK = pygame.time.Clock()
            FPSCLOCK.tick((FPS))


    def isCollide(playerx, playery, upperPipes, lowerPipes):
        if playery>= GROUNDY-GAME_SPIRITS['player'].get_height() or playery <0:
            GAME_SOUNDS['hit'].play()
            return True

        for pipe in upperPipes:
            pipeHeight = GAME_SPIRITS['pipe'][0].get_height()
            if playery < pipeHeight + pipe['y'] and abs(playerx-pipe['x']) < GAME_SPIRITS['player'].get_width():
                GAME_SOUNDS['hit'].play()
                return True

        for pipe in lowerPipes:
            pipeHeight = GAME_SPIRITS['pipe'][0].get_height()
            if playery + GAME_SPIRITS['player'].get_height() >= pipe['y'] and abs(playerx-pipe['x']) < GAME_SPIRITS['player'].get_width():
                GAME_SOUNDS['hit'].play()
                return True

        return False

    def getRandomPipe():
        """
        Generate positions of two pipes(one bottom straight and one top rotated) for blitting on screen
        """

        pipeHeight = GAME_SPIRITS['pipe'][0].get_height()
        offset = SCREENHEIGHT/3
        y2 = offset + random.randrange(0,int(SCREENHEIGHT-GAME_SPIRITS['base'].get_height()-1.2*offset))
        pipeX = SCREENHEIGHT+10
        y1 = pipeHeight - y2 + offset

        pipe = [
            {'x' : pipeX, 'y' : -y1}, # upper pipe
            {'x':pipeX, 'y' : y2} #lower pipe
        ]
        return pipe

    while True:
        welcomeScreen()
        mainGame()


if __name__ == '__main__':
    flappy_game()