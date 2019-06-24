from player import Player
from mapElements import *
from numpy import asarray, array


player1 = Player(x=500, y=500, acceleration=1)
entities = list()
entities.append(player1)

platforms = list()
platforms.append(RectanglePlatform((0, 0, 100, 1100)))
platforms.append(RectanglePlatform((0, 1000, 2000, 100)))
platforms.append(RectanglePlatform((1900, 0, 100, 1100)))
platforms.append(RectanglePlatform((500, 800, 300, 20)))
platforms.append(ComboPlatform([((0, 0), 400)], (100, 900)))
entities[0].set_cling_id(id(platforms[-1]))
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
    for e in entities:
        e.draw(screen, screenBox)

    for p in platforms:
        p.draw(screen, screenBox)
