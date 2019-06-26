from numpy import *
from keyboard import default_keymap
import pygame
from game import add_platform, set_screen_position
from mapElements import *

pygame.font.init()
myFont = pygame.font.SysFont('Times New Roman', 30)


class maker:
    def __init__(self, screen_dim=(1000, 1000), keymap=default_keymap()):
        self.screen_dim = screen_dim
        self.keymap = keymap
        self.mouse = asarray([0, 0])
        self.platType = 'Rect'
        self.points = [asarray([0, 0])] * 3
        self.currentPoint = 0
        self.stick = True
        self.position = asarray([0, 0])

    def update(self, mouse):
        self.mouse = asarray(mouse) + self.position
        if self.keymap.get_toggle('r'):
            self.platType = 'Rect'
            self.reset()

        if self.keymap.get_toggle('c'):
            self.platType = 'Circle'
            self.reset()

        if self.keymap.get_toggle('i'):
            self.platType = 'Inverse'
            self.reset()

        if self.keymap.get_toggle(chr(27)):
            self.reset()

        if self.keymap.get_toggle('t'):
            self.stick = not self.stick

        if self.keymap['w']:
            self.position[1] -= 5

        if self.keymap['a']:
            self.position[0] -= 5

        if self.keymap['s']:
            self.position[1] += 5

        if self.keymap['d']:
            self.position[0] += 5

        if self.platType == 'Rect':
            if self.currentPoint == 2:
                self.addPlatform('RectanglePlatform((%d, %d, %d, %d), stick=%s)'
                                 % (min(self.points[0][0], self.points[1][0]),
                                    min(self.points[0][1], self.points[1][1]),
                                    abs(self.points[0][0] - self.points[1][0]),
                                    abs(self.points[0][1] - self.points[1][1]),
                                    str(self.stick)))
                self.reset()

        if self.platType == 'Circle':
            if self.currentPoint == 2:
                self.addPlatform('CirclePlatform((%d, %d), %d, stick=%s)'
                                 % (self.points[0][0], self.points[0][1],
                                    linalg.norm(self.points[0] - self.points[1]), str(self.stick)))
                self.reset()

        if self.platType == 'Inverse':
            if self.currentPoint == 2:
                self.addPlatform('InverseCirclePlatform((%d, %d), %d, (%d, %d, %d, %d), stick=%s)'
                                 % self.genInverse(self.points[0], self.points[1]))
                self.reset()

        set_screen_position(self.position, centered=False)

    def click_event(self):
        self.points[self.currentPoint] = self.mouse
        self.currentPoint += 1

    def draw(self, screen):
        pygame.draw.rect(screen, (128, 128, 128), (self.screen_dim[0] * 0.8, 0,
                                                   self.screen_dim[0] * 0.2, self.screen_dim[1]))

        screen.blit(myFont.render(self.platType, True, (255, 255, 255)),
                    (self.screen_dim[0] * 0.85, self.screen_dim[1] * 0.2, 200, 50))
        screen.blit(myFont.render('sticky' if self.stick else 'not sticky', True, (255, 255, 255)),
                    (self.screen_dim[0] * 0.85, self.screen_dim[1] * 0.3, 200, 50))

        if self.platType == 'Rect':
            if self.currentPoint == 1:
                pygame.draw.rect(screen, (255, 255, 0), (self.points[0][0] - self.position[0],
                                                         self.points[0][1] - self.position[1],
                                                         self.mouse[0] - self.points[0][0],
                                                         self.mouse[1] - self.points[0][1]))

        if self.platType == 'Circle':
            if self.currentPoint == 1:
                pygame.draw.circle(screen, (255, 255, 0), (self.points[0] - self.position),
                                   int(linalg.norm(self.points[0] - self.mouse)))

        if self.platType == 'Inverse':
            if self.currentPoint == 1:
                shapeData = self.genInverse(self.points[0], self.mouse)
                pygame.draw.rect(screen, (255, 255, 0), (shapeData[3] - self.position[0],
                                                         shapeData[4] - self.position[1],
                                                         shapeData[5], shapeData[6]))
                pygame.draw.circle(screen, (0, 0, 0), (shapeData[0] - self.position[0],
                                                       shapeData[1] - self.position[1]), shapeData[2])

    def reset(self):
        self.currentPoint = 0

    def addPlatform(self, platStr):
        file = open('Platformer/res/map.txt', 'a')
        file.write('\n' + platStr)
        file.close()
        add_platform(eval(platStr))

    def genInverse(self, p1, p2):
        point_dist = int(linalg.norm(p1 - p2))
        if p1[0] > p2[0]:
            left = p1[0] - point_dist
        else:
            left = p1[0]

        if p1[1] > p2[1]:
            top = p1[1] - point_dist
        else:
            top = p1[1]

        return p1[0], p1[1], point_dist, left, top, point_dist, point_dist, str(self.stick)
