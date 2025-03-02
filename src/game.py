from player import Player
from mapElements import *
from numpy import asarray, array
import mapLoader
from random import randint


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

    for p in platforms:
        p.update(player1)


def game_draw(screen):
    set_screen_position(player1.pos)
    for p in platforms:
        if p.win:
            p.draw(screen, screenBox, (255, 255, 0))
        elif p.kill:
            p.draw(screen, screenBox, (255, 0, 0))
        else:
            p.draw(screen, screenBox, (255, 255, 255))

    for e in entities:
        e.draw(screen, screenBox)


def draw_map(screen):
    player1.pos = screenBox[0:2].astype(float)
    for p in platforms:
        if p.kill:
            p.draw(screen, screenBox, (255, 0, 0))
        elif p.stick:
            p.draw(screen, screenBox, (255, 255, 255))
        else:
            p.draw(screen, screenBox, (128, 255, 255))


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