from player import Player
from mapElements import *
from numpy import asarray, array
import mapLoader


player1 = Player(x=500, y=500, acceleration=1)
entities = list()
entities.append(player1)

platforms = list()
platforms += mapLoader.load('Platformer/res/map.txt')
screenBox: array
screenDim: array


def set_screen_info(width, height):
    global screenBox, screenDim
    screenBox = asarray([0, 0, width, height])
    screenDim = asarray([width, height])


def game_loop():
    for e in entities:
        e.update(platforms)


def game_draw(screen):
    set_screen_position(player1.pos)
    for p in platforms:
        p.draw(screen, screenBox)

    for e in entities:
        e.draw(screen, screenBox)


def draw_map(screen):
    for p in platforms:
        p.draw(screen, screenBox)


def add_platform(platform):
    platforms.append(platform)


def set_screen_position(position, centered=True):
    global screenBox
    screenBox = screenBox.reshape((2, 2))
    if centered:
        screenBox += -screenBox[0, 0:2] + asarray(position).astype(int) - (screenDim / 2).astype(int)

    else:
        screenBox += -screenBox[0, 0:2] + asarray(position).astype(int)

    screenBox = screenBox.reshape(4)