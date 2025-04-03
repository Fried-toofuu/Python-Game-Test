import pygame 
from os.path import join 
from os import walk

WINDOW_WIDTH, WINDOW_HEIGHT = 1200,700
TILE_SIZE = 64

class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
