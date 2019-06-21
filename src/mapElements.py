from shape import *
from pygame import draw


class Platform(ABC):
    def __init__(self, shape):
        self.boundingBox = shape.boundingBox
        self.shape = shape

    def intersect(self, shape):
        pass

    def draw(self, screen):
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
    def __init__(self, center, radius):
        super().__init__(Circle(center, radius))

    def draw(self, screen):
        draw.circle(screen, (255, 255, 255), self.shape.center.astype(int), self.shape.radius)


class PolygonPlatform(Platform):
    def __init__(self, polygon):
        super().__init__(Polygon(polygon))

    def draw(self, screen):
        draw.polygon(screen, (255, 255, 255), self.shape.shape)


class RectanglePlatform(Platform):
    def __init__(self, rect):
        super().__init__(Rectangle(rect))

    def draw(self, screen):
        draw.polygon(screen, (255, 255, 255), self.shape.shape)


class ComboPlatform(Platform):
    def __init__(self, shapes):
        super().__init__(ComboShape(list(map(chose_shape, shapes))))

    def draw(self, screen):
        for shape in self.shape.shapes:
            if shape.type == 'Circle':
                draw.circle(screen, (255, 255, 255), shape.center.astype(int), shape.radius)
            if shape.type == 'Polygon':
                draw.polygon(screen, (255, 255, 255), shape.shape)
            if shape.type == 'Rectangle':
                draw.polygon(screen, (255, 255, 255), shape.shape)