from entity import Entity
from keyboard import default_keymap
from numpy import array, linalg
from pygame import draw
from shape import *
import math

UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'
JUMP = ' '
gravityArrow = asfarray([[0, 0], [1, 0], [1, 2], [1.5, 2], [0.5, 3], [-0.5, 2], [0, 2]])


class Player(Entity):
    def __init__(self, x, y, acceleration, key_map=default_keymap()):
        self.keyMap = key_map
        self.pos = array([x, y], dtype=float)
        self.velocity = array([0, 0], dtype=float)
        self.acceleration = acceleration
        self.shape = Rectangle((-20, -20, 40, 40))
        self.grounded = False
        self.wallRide = False
        self.wallNormal = None
        self.canWallCling = False
        self.baseGravity = asfarray([0, 1])
        self.gravity = self.baseGravity
        self.gravityNormal = asfarray([self.baseGravity[1], -self.baseGravity[0]])
        self.gravityTransform = asfarray([[1, 0], [0, 1]])
        self.groundMinVerticalNormal = 0.5
        self.wallMinVerticalNormal = -0.1
        self.gravityRotation = 0
        self.rotationAngle = 0
        self.frictionless = False  # use to apply force to player in high friction states
        self.surfaceCling = False  # weather the player should cling to the clingId surface
        self.clingId = 0

    def update(self, platforms):
        self.calc_movement()
        self.pos += self.velocity
        self.velocity += self.gravity

        if not self.frictionless:
            if self.wallRide:
                self.velocity *= 0.20
            else:
                self.velocity *= 0.95

        self.shape.translate_absolute(self.pos)
        if self.keyMap.get_toggle('r'):
            if self.keyMap[chr(304)]:
                self.gravityRotation += math.pi/2
            else:
                self.gravityRotation -= math.pi/2

        self.frictionless = False
        self.grounded = False
        self.wallRide = False

        if self.keyMap['p']:
            breakpoint()
        self.calc_intersects(platforms)

    def calc_intersects(self, platforms):
        for plat in platforms:
            plat.shape: Shape
            cling = False
            if self.surfaceCling:
                if self.clingId == id(plat):
                    cling = True

            inter = self.shape.intersect(plat.shape, cling)
            if inter[0]:
                if inter[0] <= 0 or cling:
                    self.pos -= inter[0] * inter[1]
                    velMag = linalg.norm(self.velocity)

                    self.velocity -= inter[1] * (self.velocity @ inter[1])

                    if abs(self.velocity @ inter[1]) < velMag * 0.1:
                        if linalg.norm(self.velocity) > 0.1:
                            self.velocity /= linalg.norm(self.velocity)
                            self.velocity *= velMag

                    if -inter[1] @ self.gravity > self.groundMinVerticalNormal:
                        self.grounded = True

                    if -inter[1] @ self.gravity >= self.wallMinVerticalNormal \
                            and self.gravity @ self.velocity > 0 and self.canWallCling:
                        self.wallRide = True
                        self.wallNormal = inter[1]

                    self.shape.translate_absolute(self.pos)

                    if inter[1][0] == 0:
                        self.rotationAngle = -math.pi/2
                    else:
                        self.rotationAngle = math.atan(inter[1][1]/inter[1][0])

                    self.rotationAngle += math.pi/2

                    if inter[1][1] < 0:
                        self.rotationAngle *= -1
                    self.shape.rotate_absolute(self.rotationAngle)

                    if cling:
                        self.set_gravity(self.rotationAngle)

    def calc_movement(self):
        mov_vector = asfarray([0, 0])
        if self.keyMap[LEFT]:
            mov_vector[0] -= 1

        if self.keyMap[RIGHT]:
            mov_vector[0] += 1

        if self.keyMap[UP]:
            mov_vector[1] -= 1

        if self.keyMap[DOWN]:
            mov_vector[1] += 1

        self.velocity += self.gravityNormal * mov_vector[0] * self.acceleration

        if self.keyMap.get_toggle(JUMP) and self.grounded:
            self.velocity -= self.gravity * 30
            self.surfaceCling = False

        elif self.keyMap.get_toggle(JUMP) and self.wallRide:
            self.velocity += self.wallNormal * 20
            self.velocity -= self.gravity * 30
            self.frictionless = True

    def set_gravity(self, radians):
        c = math.cos(radians)
        s = math.sin(radians)
        self.gravityTransform = asfarray([[c, -s], [s, c]])
        self.gravity = self.baseGravity @ self.gravityTransform
        self.gravityNormal = asfarray([self.gravity[1], -self.gravity[0]])

    def __str__(self):
        return "Player at {} with velocity {}".format(self.pos, self.velocity)

    def draw(self, screen, screen_box):
        draw.polygon(screen, (255, 255, 0), self.shape.shape - screen_box[0:2])
        draw.polygon(screen, (0, 255, 0) if self.grounded else (255, 0, 0), gravityArrow @ self.gravityTransform * 50 + asfarray([500, 100]))

    def set_cling_id(self, cling_id):
        self.clingId = cling_id
        self.surfaceCling = True
