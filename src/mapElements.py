from shape import *
from pygame import draw, Surface


class Platform(ABC):
    def __init__(self, shape, offset, stick, kill):
        self.kill = kill
        self.shape = shape
        self.stick = stick
        self.shape.translate_absolute(asfarray(offset))
        self.boundingBox = shape.boundingBox

    @abstractmethod
    def draw(self, screen, screen_box, color):
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
    def __init__(self, polygon, offset=0, stick=False, kill=False):
        super().__init__(Polygon(polygon), offset, stick, kill)

    def draw(self, screen, screen_box, color):
        if contain(self.boundingBox, screen_box):
            draw.polygon(screen, color, self.shape.shape - screen_box[0:2])


class RectanglePlatform(Platform):
    def __init__(self, rect, offset=(0, 0), stick=False, kill=False):
        super().__init__(Rectangle(rect), offset, stick, kill)

    def draw(self, screen, screen_box, color):
        draw.polygon(screen, color, self.shape.shape - screen_box[0:2])


class ComboPlatform(Platform):
    def __init__(self, shapes, offset=(0, 0), stick=False, kill=False):
        super().__init__(ComboShape(list(map(chose_shape, shapes))), offset, stick, kill)

    def draw(self, screen, screen_box, color):
        if contain(self.boundingBox, screen_box):
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
