from game import game_loop, game_draw
from keyboard import *


import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (90, 30)
del os

pygame.init()
screen = pygame.display.set_mode((1920-90, 1080-30), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Basic Platformer")
clock = pygame.time.Clock()


fps = 30


def main():
    done = False
    frame_count = 0

    while not done:
        kbrd.reset_toggle()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            kbrd.give_event(event)

        frame_count += 1
        screen.fill((0, 0, 0))
        game_loop()
        game_draw(screen)
        pygame.display.flip()
        clock.tick(fps)
        if frame_count % fps == 0:
            print(clock.get_fps())



main()
