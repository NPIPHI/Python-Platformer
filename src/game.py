from player import Player
from mapElements import *
from numpy import asarray, array
import mapLoader


player1 = Player(x=500, y=500, acceleration=0.5)
entities = list()
entities.append(player1)

platforms = list()
platforms += mapLoader.load('Platformer/res/map.txt')
platforms.append(InverseCirclePlatform((200, 900), 100, (100, 900, 100, 100)))
platforms.append(InverseCirclePlatform((200, 100), 100, (100, 0, 100, 100)))
platforms.append(InverseCirclePlatform((1200, 900), 100, (1200, 900, 100, 100)))
platforms.append(InverseCirclePlatform((1200, 100), 100, (1200, 0, 100, 100)))
platforms.append(RectanglePlatform((1300, 0, 100, 1000)))
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
    global screenBox
    screenBox = screenBox.reshape((2, 2))
    screenBox += -screenBox[0, 0:2] + player1.pos.astype(int) - (screenDim/2).astype(int)
    screenBox = screenBox.reshape(4)
    for p in platforms:
        p.draw(screen, screenBox)

    for e in entities:
        e.draw(screen, screenBox)

