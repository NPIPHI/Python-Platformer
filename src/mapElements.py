from shape import *
from pygame import draw, Surface

class Platform(ABC):
    def __init__(self, shape, offset, stick, kill):
        self.mov = (0, 0)
        self.win = False
        self.kill = kill
        self.shape = shape
        self.stick = stick
        self.shape.translate_absolute(asfarray(offset))
        self.boundingBox = shape.boundingBox

    @abstractmethod
    def draw(self, screen, screen_box, color):
        pass

    def update(self, player):
        pass

    def touch(self):
        pass

    def translate(self, vector):
        self.shape.translate(vector)

    def translate_absolute(self, vector):
        self.shape.translate_absolute(vector)

    def rotate(self, radians):
        self.shape.rotate(radians)

    def rotate_absolute(self, radians):
        self.shape.rotate_absolute(radians)

class CirclePlatform(Platform):
    def __init__(self, center, radius, offset=(0, 0),  stick=False, kill=False):
        super().__init__(Circle(center, radius), offset, stick, kill)

    def draw(self, screen, screen_box, color):
        if contain(self.boundingBox, screen_box):
            draw.circle(screen, color, self.shape.center.astype(int) - screen_box[0:2],
                        self.shape.radius)


class PolygonPlatform(Platform):
    def __init__(self, polygon, offset=(0, 0), stick=False, kill=False):
        super().__init__(Polygon(polygon), offset, stick, kill)

    def draw(self, screen, screen_box, color):
        if contain(self.boundingBox, screen_box):
            draw.polygon(screen, color, self.shape.shape - screen_box[0:2])


class RectanglePlatform(Platform):
    def __init__(self, rect, offset=(0, 0), stick=False, kill=False):
        super().__init__(Rectangle(rect), offset, stick, kill)

    def draw(self, screen, screen_box, color):
        draw.polygon(screen, color, self.shape.shape - screen_box[0:2])


class FallingPlatform(RectanglePlatform):
    def __init__(self, rect, offset=(0, 0), stick=False, kill=False):
        super().__init__(rect, offset, stick, kill)
        self.fallFrames = 120
        self.fallVect = (0, 4)
        self.fallTrack = -1

    def touch(self):
        if self.fallTrack == -1:
            self.fallTrack = 0
            self.mov = self.fallVect

    def update(self, player):
        if self.fallTrack != -1:
            self.fallTrack += 1
            self.shape.translate(self.fallVect)
            if self.fallTrack > self.fallFrames:
                self.fallTrack = -1
                self.mov = (0, 0)
                self.shape.translate_absolute((0, 0))


class ComboPlatform(Platform):
    def __init__(self, shapes, offset=(0, 0), stick=False, kill=False):
        super().__init__(ComboShape(list(map(chose_shape, shapes))), offset, stick, kill)

    def draw(self, screen, screen_box, color):
        if contain(self.shape.boundingBox, screen_box):
            for shape in self.shape.shapes:
                if shape.type == 'Circle':
                    draw.circle(screen, color, shape.center.astype(int) - screen_box[0:2],
                                shape.radius)
                if shape.type == 'Polygon':
                    draw.polygon(screen, color, shape.shape - screen_box[0:2])
                if shape.type == 'Rectangle':
                    draw.polygon(screen, color, shape.shape - screen_box[0:2])


class InverseCirclePlatform(Platform):
    def __init__(self, exclude_circle_center, exclude_circle_radius, polygon, offset=(0, 0), stick=False, kill=False):
        super().__init__(InverseCircle(exclude_circle_center, exclude_circle_radius, polygon), offset, stick, kill)
        self.drawImage = Surface((self.shape.boundingBox[2] - self.shape.boundingBox[0],
                                  self.shape.boundingBox[3] - self.shape.boundingBox[1]))
        draw.polygon(self.drawImage, (255, 255, 255), self.shape.polygon - self.shape.boundingBox[0:2])
        draw.circle(self.drawImage, (0, 0, 0), (int(self.shape.excludeCircle[1]),
                                                int(self.shape.excludeCircle[1])),
                    int(self.shape.excludeCircle[1]))
        self.drawImage.set_colorkey((0, 0, 0))

    def draw(self, screen, screen_box, color):
        if contain(self.boundingBox, screen_box):
            screen.blit(self.drawImage, self.shape.boundingBox[0:2] - screen_box[0:2])
            # TODO: Improve Render time


class WinPlatform(RectanglePlatform):
    def __init__(self, rect, offset=(0, 0), stick=False, kill=False):
        super().__init__(rect, offset, stick, kill)
        self.win = True


class ChasePlatform(PolygonPlatform):
    def __init__(self, polygon, offset=(0, 0), stick=False, kill=False):
        super().__init__(polygon, offset, stick, kill)
        self.activationBox = (self.shape.boundingBox[0], self.shape.boundingBox[1],
                              self.shape.boundingBox[2]+1000, self.shape.boundingBox[3])
        self.movVect = (15, 0)
        self.attack = False
        self.attackFrames = 0

    def update(self, player):
        if contain(player.shape.boundingBox, self.activationBox) and not self.attack:
            self.attack = True
            self.attackFrames = 0

        if self.attack:
            self.attackFrames += 1
            if self.attackFrames < 30:
                self.shape.translate((self.attackFrames/2, 0))
            else:
                self.shape.translate(self.movVect)

    def draw(self, screen, screen_box, color):
        if contain(self.shape.boundingBox, screen_box):
            draw.polygon(screen, color, self.shape.shape - screen_box[0:2])
