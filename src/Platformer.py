from game import game_loop, game_draw, set_screen_info, draw_map
from keyboard import *
import mapMaker

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (90, 30)
del os

pygame.init()
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w-90, info.current_h-30), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Basic Platformer")
clock = pygame.time.Clock()
maker = mapMaker.maker(screen_dim=(info.current_w-90, info.current_h-30))

fps = 60
set_screen_info(info.current_w-90, info.current_h-30)


def main():
    playMode = 'Play'
    done = False
    frame_count = 0
    while not done:
        kbrd.reset_toggle()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                maker.click_event()

            if event.type == pygame.KEYDOWN:
                if event.key == ord('\t'):
                    if playMode == 'Play':
                        playMode = 'Make'

                    else:
                        playMode = 'Play'
            kbrd.give_event(event)

        frame_count += 1
        screen.fill((0, 0, 0))
        if playMode == 'Play':
            game_loop()
            game_draw(screen)

        if playMode == 'Make':
            maker.update(pygame.mouse.get_pos())
            draw_map(screen)
            maker.draw(screen)

        pygame.display.flip()
        clock.tick_busy_loop(fps)
        if frame_count % fps == 0:
            print(clock.get_fps())


main()
