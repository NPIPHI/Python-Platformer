from abc import ABC
from numpy import asfarray, ndarray, linalg, einsum, inf
import math


maxEjectionDistance = 100


class Shape(ABC):
    boundingBox: tuple

    def __init__(self, dtype):
        self.type = dtype

    def rotate(self, radians):
        pass

    def translate(self, vector):
        pass

    def intersect(self, shape, cling):
        pass

    def rotate_absolute(self, radians):
        pass

    def translate_absolute(self, vector):
        pass


class Circle(Shape):
    _baseCenter: ndarray
    _translation: ndarray

    def __init__(self, center, radius):
        super().__init__('Circle')
        self._cached = True
        self._baseCenter = asfarray(center)
        self._center = self._baseCenter
        self._radius = radius
        self._boundingBox = (center[0] - radius, center[1] - radius,
                             center[0] + radius, center[1] + radius)
        self._rotation = asfarray([[1, 0], [0, 1]])
        self._translation = asfarray([0,0])

    def translate(self, vector):
        self._translation += vector
        self._cached = False

    def translate_absolute(self, vector):
        self._translation = vector
        self._cached = False

    def rotate(self, radians):
        c = math.cos(radians)
        s = math.sin(radians)
        self._rotation = self._rotation @ asfarray([[c, -s], [s, c]])
        self._cached = False

    def rotate_absolute(self, radians):
        c = math.cos(radians)
        s = math.sin(radians)
        self._rotation = asfarray([[c, -s], [s, c]])
        self._cached = False

    def get_radius(self):
        return self._radius

    def get_bounding_box(self):
        if not self._cached:
            self._generate()

        return self._boundingBox

    def get_shape(self):
        if not self._cached:
            self._generate()

        return self._center, self._radius

    def get_center(self):
        if not self._cached:
            self._generate()

        return self._center

    def _generate(self):
        self._center = self._baseCenter @ self._rotation + self._translation
        self._boundingBox = (self._center[0] - self._radius, self._center[1] - self._radius,
                             self._center[0] + self._radius, self._center[1] + self._radius)

        self._cached = True

    radius = property(get_radius)
    shape = property(get_shape)
    center = property(get_center)
    boundingBox = property(get_bounding_box)


class Polygon(Shape):
    _baseShape: ndarray
    _rotation: ndarray
    _translation: ndarray
    _cachedShape: ndarray
    _cached: bool

    def __init__(self, points):  # Points is an array-like of an array-like
        super().__init__('Polygon')
        self._baseShape = asfarray(points)
        self._rotation = asfarray([[1, 0], [0, 1]])
        self._translation = asfarray([0, 0])
        self._cachedShape = self._baseShape
        self._boundingBox = (self._baseShape[:, 0].min(), self._baseShape[:, 1].min(),
                             self._baseShape[:, 0].max(), self._baseShape[:, 1].max())
        self._baseNormals = get_normals(self._baseShape)
        self._minOnNormals = einsum('ij, ij->i', self._baseShape, self._baseNormals)
        self._normals = self._baseNormals
        self._cached = True

    def rotate(self, radians):
        c = math.cos(radians)
        s = math.sin(radians)
        self._rotation = self._rotation @ asfarray([[c, -s], [s, c]])
        self._cached = False

    def rotate_absolute(self, radians):
        c = math.cos(radians)
        s = math.sin(radians)
        self._rotation = asfarray([[c, -s], [s, c]])
        self._cached = False

    def translate(self, vector):
        self._translation += asfarray(vector)
        self._cached = False

    def translate_absolute(self, vector):
        self._translation = asfarray(vector)
        self._cached = False

    def get_shape(self):
        if not self._cached:
            self._generate()

        return self._cachedShape

    def get_bounding_box(self):
        if not self._cached:
            self._generate()

        return self._boundingBox

    def get_normals(self):
        if not self._cached:
            self._generate()

        return self._normals

    def get_min_on_normals(self):
        if not self._cached:
            self._generate()

        return self._minOnNormals

    def _generate(self):  # generates properties after a transformation
        self._cachedShape = self._baseShape @ self._rotation + self._translation
        self._boundingBox = (self._cachedShape[:, 0].min(), self._cachedShape[:, 1].min(),
                             self._cachedShape[:, 0].max(), self._cachedShape[:, 1].max())
        self._normals = self._baseNormals @ self._rotation
        self._minOnNormals = einsum('ij, ij->i', self._cachedShape, self._normals)
        self._cached = True

    def intersect(self, shape, cling):
        if (shape.boundingBox[0] <= self.boundingBox[2]
                and shape.boundingBox[2] >= self.boundingBox[0]
                and shape.boundingBox[1] <= self.boundingBox[3]
                and shape.boundingBox[3] >= self.boundingBox[1]) \
                or cling:
            if shape.type == 'Polygon':
                shape: Polygon

                dif = -maxEjectionDistance
                dif_vect = None

                for normal in shape.normals:
                    norm_dif = (self.shape @ normal).min() - (shape.shape @ normal).max()
                    if norm_dif > dif:
                        dif = norm_dif
                        dif_vect = normal

                for normal in self.normals:
                    norm_dif = (shape.shape @ normal).min() - (self.shape @ normal).max()
                    if norm_dif > dif:
                        dif = norm_dif
                        dif_vect = -normal

                if dif <= 0 and dif != - maxEjectionDistance:
                    return dif, dif_vect

            if shape.type == 'Circle':
                shape: Circle

                best_point_index = None
                normal = None

                best_point_dist = 100000
                for index, point in enumerate(self.shape):
                    dist = linalg.norm(point - shape.center)
                    if dist < best_point_dist:
                        best_point_index = index
                        best_point_dist = dist
                        normal = (point - shape.center) / dist

                line1 = (self.shape[best_point_index], self.shape[(best_point_index+1) % len(self.shape)])
                line2 = (self.shape[(best_point_index-1) % len(self.shape)], self.shape[best_point_index])
                line1_vector = line1[0] - line1[1]
                line2_vector = line2[0] - line2[1]

                if line1[0].dot(line1_vector) > shape.center.dot(line1_vector) > line1[1].dot(line1_vector):
                    line1_vector = asfarray([line1_vector[1], -line1_vector[0]]) / linalg.norm(line1_vector)
                    dist = line1_vector.dot(line1[0]) - line1_vector.dot(shape.center)
                    if dist < best_point_dist:
                        normal = line1_vector
                        best_point_dist = dist

                if line2[0].dot(line2_vector) > shape.center.dot(line2_vector) > line2[1].dot(line2_vector):
                    line2_vector = asfarray([line2_vector[1], -line2_vector[0]]) / linalg.norm(line2_vector)
                    dist = line2_vector.dot(line2[0]) - line2_vector.dot(shape.center)
                    if dist < best_point_dist:
                        normal = line2_vector
                        best_point_dist = dist

                return best_point_dist - shape.radius, normal

            if shape.type == 'Combo':
                best_dist = 100000
                normal = None
                for shape in shape.shapes:
                    ret = self.intersect(shape, cling)
                    if ret[0] < best_dist:
                        best_dist = ret[0]
                        normal = ret[1]

                if best_dist != 100000:
                    return best_dist, normal

        return False, None

    normals = property(get_normals)
    minOnNormals = property(get_min_on_normals)
    shape = property(get_shape)
    boundingBox = property(get_bounding_box)


class Rectangle(Polygon):

    def __init__(self, rect):  # rect is a tuple of (x, y, w, h)
        super().__init__(((rect[0], rect[1]), (rect[0] + rect[2], rect[1]),
                          (rect[0] + rect[2], rect[1] + rect[3]), (rect[0], rect[1] + rect[3])))


class ComboShape(Shape):
    def __init__(self, shapes):
        super().__init__('Combo')
        self.shapes = shapes
        self._cached = False

    def translate(self, vector):
        for shp in self.shapes:
            shp.translate(vector)

        self._cached = False

    def translate_absolute(self, vector):
        for shp in self.shapes:
            shp.translate_absolute(vector)

        self._cached = False

    def rotate(self, radians):
        for shp in self.shapes:
            shp.rotate(radians)

        self._cached = False

    def rotate_absolute(self, radians):
        for shp in self.shapes:
            shp.rotate_absolute(radians)

        self._cached = False

    def get_bounding_box(self):
        if not self._cached:
            self._generate()

        return self._boundingBox

    def _generate(self):
        sub_bounding_boxes = asfarray([shp.boundingBox for shp in self.shapes])
        self._boundingBox = (sub_bounding_boxes[:, 0].min(), sub_bounding_boxes[:, 1].min(),
                             sub_bounding_boxes[:, 2].max(), sub_bounding_boxes[:, 3].max())
        self._cached = True

    boundingBox = property(get_bounding_box)


def get_normals(points):  # points is the vertices of a polygon in clockwise order
    ret = ndarray(shape=(len(points), 2), dtype=float)
    for ind in range(len(points)):
        vec = (points[ind] - points[ind + 1 if ind < len(points) - 1 else 0])
        vec[0], vec[1] = -vec[1], vec[0]
        ret[ind] = vec / linalg.norm(vec)

    return ret


def chose_shape(shape):
    if len(shape) == 4:
        return Rectangle(shape)
    elif type(shape[1]) == int:
        return Circle(shape[0], shape[1])

    else:
        return Polygon(shape)

