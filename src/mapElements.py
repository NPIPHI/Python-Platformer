from shape import *
from pygame import draw


class Platform(ABC):
    def __init__(self, shape, offset):
        self.shape = shape
        self.shape.translate_absolute(asfarray(offset))
        self.boundingBox = shape.boundingBox

    @abstractmethod
    def draw(self, screen, screen_box):
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
    def __init__(self, center, radius, offset=(0, 0)):
        super().__init__(Circle(center, radius), offset)

    def draw(self, screen, screen_box):
        if contain(self.boundingBox, screen_box):
            draw.circle(screen, (255, 255, 255), self.shape.center.astype(int) - screen_box[0:2],
                        self.shape.radius)


class PolygonPlatform(Platform):
    def __init__(self, polygon, offset=0):
        super().__init__(Polygon(polygon), offset)

    def draw(self, screen, screen_box):
        if contain(self.boundingBox, screen_box):
            draw.polygon(screen, (255, 255, 255), self.shape.shape - screen_box[0:2])


class RectanglePlatform(Platform):
    def __init__(self, rect, offset=(0, 0)):
        super().__init__(Rectangle(rect), offset)

    def draw(self, screen, screen_box):
        draw.polygon(screen, (255, 255, 255), self.shape.shape - screen_box[0:2])


class ComboPlatform(Platform):
    def __init__(self, shapes, offset=(0, 0)):
        super().__init__(ComboShape(list(map(chose_shape, shapes))), offset)

    def draw(self, screen, screen_box):
        if contain(self.boundingBox, screen_box):
            for shape in self.shape.shapes:
                if shape.type == 'Circle':
                    draw.circle(screen, (255, 255, 255), shape.center.astype(int) - screen_box[0:2],
                                shape.radius)
                if shape.type == 'Polygon':
                    draw.polygon(screen, (255, 255, 255), shape.shape - screen_box[0:2])
                if shape.type == 'Rectangle':
                    draw.polygon(screen, (255, 255, 255), shape.shape - screen_box[0:2])


class InverseCirclePlatform(Platform):
    def __init__(self, exclude_circle_center, exclude_circle_radius, polygon, offset=(0, 0)):
        super().__init__(InverseCircle(exclude_circle_center, exclude_circle_radius, polygon), offset)

    def draw(self, screen, screen_box):
        if contain(self.boundingBox, screen_box):
            draw.polygon(screen, (255, 255, 255), self.shape.polygon - screen_box[0:2])
            draw.circle(screen, (0, 0, 0), self.shape.excludeCircle[0].astype(int) - screen_box[0:2],
                        int(self.shape.excludeCircle[1]))
