from game import game_loop, game_draw, set_screen_info
from keyboard import *

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (90, 30)
del os

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w-90, info.current_h-30), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Basic Platformer")
clock = pygame.time.Clock()


fps = 120
set_screen_info(info.current_w, info.current_h)


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
