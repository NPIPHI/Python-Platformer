from abc import ABC, abstractmethod


class Entity(ABC):
    def __inti__(self):
        pass

    @abstractmethod
    def draw(self, screen, screen_box):
        pass

    @abstractmethod
    def update(self, platforms):
        pass
