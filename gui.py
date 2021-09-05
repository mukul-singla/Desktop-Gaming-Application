# from tkinter import *
# top = tk.Tk()
#
# B = tk.b
#
# top.mainloop()

import pygame_menu
import os
from FlappyBird import *
from Snake import snake_game
from SpaceInvader import *

x = 100
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
game=1;

def choose_game(value, game_code):
    print("here")
    print(game_code)
    global game
    game = game_code

def start_the_game():
    print(game)
    if game == 1:
        flappy_game()
    elif game == 2:
        space_game()
    else:
        snake_game()


pygame.init()
surface = pygame.display.set_mode((500, 300),pygame.RESIZABLE )

menu = pygame_menu.Menu('Welcome', 500, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Game :', [('Flappy Bird', 1), ('Space Invader', 2),('Snake',3)], onchange=choose_game)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)