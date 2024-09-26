from abc import ABC, abstractmethod

class Collidable(ABC):

    @abstractmethod
    def is_hit_by(self, other: 'Collidable') -> bool:
        pass

    @abstractmethod
    def bounding_box(self) -> dict:
        pass

    @staticmethod
    def get_aabb(position, size):
        min_corner = position - size / 2
        max_corner = position + size / 2
        return {'min': min_corner, 'max': max_corner}

    @staticmethod
    def aabb_collision(a_min, a_max, b_min, b_max):
        return (a_min.x <= b_max.x and a_max.x >= b_min.x and
                a_min.y <= b_max.y and a_max.y >= b_min.y and 
                a_min.z <= b_max.z and a_max.z >= b_min.z)
