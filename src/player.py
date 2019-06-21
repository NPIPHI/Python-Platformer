from entity import Entity
from keyboard import default_keymap
from numpy import array
from pygame import draw
from shape import *

up = 'w'
down = 's'
left = 'a'
right = 'd'
jump = ' '
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
        self.frictionless = False  # use to apply force to player in high friction states

    def update(self, platforms):
        self.calc_movement()
        self.velocity += self.gravity
        self.pos += self.velocity
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

            c = math.cos(self.gravityRotation)
            s = math.sin(self.gravityRotation)
            self.gravityTransform = asfarray([[c, -s], [s, c]])
            self.gravity = self.baseGravity @ self.gravityTransform
            self.gravityNormal = asfarray([self.gravity[1], -self.gravity[0]])

        self.frictionless = False
        self.grounded = False
        self.wallRide = False

        if self.keyMap['p']:
            breakpoint()
        self.calc_intersects(platforms)

    def calc_intersects(self, platforms):
        for plat in platforms:
            plat.shape: Shape
            inter = self.shape.intersect(plat.shape)
            if inter[0]:
                if inter[0] <= 0:
                    self.pos -= inter[0] * inter[1]
                    self.velocity -= (inter[1] * (self.velocity @ inter[1]))
                    if -inter[1] @ self.gravity > self.groundMinVerticalNormal:
                        self.grounded = True

                    elif -inter[1] @ self.gravity >= self.wallMinVerticalNormal \
                            and self.gravity @ self.velocity > 0 and self.canWallCling:
                        self.wallRide = True
                        self.wallNormal = inter[1]

                    self.shape.translate_absolute(self.pos)

    def calc_movement(self):
        movVector = asfarray([0,0])
        if self.keyMap[left]:
            movVector[0] -= 1

        if self.keyMap[right]:
            movVector[0] += 1

        if self.keyMap[up]:
            movVector[1] -= 1

        if self.keyMap[down]:
            movVector[1] += 1

        self.velocity += self.gravityNormal * movVector[0] * self.acceleration

        if self.keyMap.get_toggle(jump) and self.grounded:
            self.velocity -= self.gravity * 30

        elif self.keyMap.get_toggle(jump) and self.wallRide:
            self.velocity += self.wallNormal * 20
            self.velocity -= self.gravity * 30
            self.frictionless = True


    def __str__(self):
        return "Player at {} with velocity {}".format(self.pos, self.velocity)

    def draw(self, screen):
        draw.polygon(screen, (255, 255, 0), self.shape.shape)
        draw.polygon(screen, (255, 0, 0), gravityArrow @ self.gravityTransform * 50 + asfarray([500, 100]))
