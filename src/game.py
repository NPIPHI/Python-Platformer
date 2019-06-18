from player import Player
from mapElements import *

entities = list()
entities.append(Player(x=500, y=500, acceleration=1))

platforms = list()
platforms.append(RectanglePlatform((0, 0, 100, 1100)))
platforms.append(RectanglePlatform((0, 1000, 2000, 100)))
platforms.append(RectanglePlatform((1900, 0, 100, 1100)))
platforms.append(PolygonPlatform(((500, 500), (750, 250), (1000, 500))))

def game_loop():
    for e in entities:
        e.update(platforms)

def game_draw(screen):
    for e in entities:
        e.draw(screen)

    for p in platforms:
        p.draw(screen)
