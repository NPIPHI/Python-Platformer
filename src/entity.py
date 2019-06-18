from abc import ABC


class Entity(ABC):
    def __inti__(self):
        pass

    def draw(self, screen):
        pass

    def update(self, platforms):
        pass
