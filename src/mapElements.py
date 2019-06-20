from shape import *
from pygame import draw


class Platform(ABC):
    def __init__(self, bounding_box):
        self.boundingBox = bounding_box

    def intersect(self, shape):
        pass

    def draw(self, screen):
        pass


class CirclePlatform(Platform):
    def __init__(self, center, radius):
        self.shape = Circle(center, radius)
        super().__init__(self.shape.boundingBox)

    def draw(self, screen):
        draw.circle(screen, (255, 255, 255), self.shape.center.astype(int), self.shape.radius)


class PolygonPlatform(Platform):
    def __init__(self, polygon):
        self.shape = Polygon(polygon)
        super().__init__(self.shape.boundingBox)

    def draw(self, screen):
        draw.polygon(screen, (255, 255, 255), self.shape.shape)


class RectanglePlatform(Platform):
    def __init__(self, rect):
        self.shape = Rectangle(rect)
        super().__init__(self.shape.boundingBox)

    def draw(self, screen):
        draw.polygon(screen, (255, 255, 255), self.shape.shape)
