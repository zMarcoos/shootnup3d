import glm
import time
from OpenGL.GL import *
from OpenGL.GLUT import *
from abc import abstractmethod
from controller.model_cache import ModelCache
from util.constants import COLORS
from model.interface.collidable import Collidable

class Entity(Collidable):
    def __init__(self, x: float, y: float, z: float, model_path: str = None):
        self.position = glm.vec3(x, y, z)
        self.original_position = glm.vec3(x, y, z)
        self.color = COLORS['white']
        self.lives = 1
        self.velocity = 0.1
        self.scale = glm.vec3(1.0, 1.0, 1.0)
        self.model = ModelCache.get_model(model_path)
        self.is_visible = True
        self.is_invulnerable = self.shooting = False

    def update(self, delta_time: float, **kwargs):
        pass

    def is_active(self) -> bool:
        return self.is_visible and self.is_alive()

    def is_alive(self) -> bool:
        return self.lives > 0

    def damage(self, amount: float = 1.0):
        if self.is_invulnerable or not self.is_alive():
            return
        self.lives -= amount

    def reset_position(self):
        self.position = glm.vec3(self.original_position)
        self.is_visible = True
        self.set_invulnerability(True)

    def set_invulnerability(self, value: bool):
        self.is_invulnerable = value

    def set_visibility(self, value: bool):
        self.is_visible = value

    def bounding_box(self) -> dict:
        if not self.model:
            return {
                'min': self.position,
                'max': self.position
            }

        model_box = self.model.get_bounding_box()
        scaled_min = self.position + model_box['min'] * self.scale
        scaled_max = self.position + model_box['max'] * self.scale

        return {'min': scaled_min, 'max': scaled_max}

    def is_hit_by(self, other: 'Collidable') -> bool:
        box = self.bounding_box()
        target_box = other.bounding_box()
        return Collidable.aabb_collision(box['min'], box['max'], target_box['min'], target_box['max'])

    def draw(self):
        if not self.model or not self.is_visible:
            return

        if self.is_invulnerable and int(time.time() * 10) % 2 == 0:
            return

        glPushAttrib(GL_CURRENT_BIT | GL_LIGHTING_BIT)
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.color)
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        self.apply_transform()
        glScalef(self.scale[0], self.scale[1], self.scale[2])
        self.model.render()
        glPopMatrix()
        glPopAttrib()

    @abstractmethod
    def apply_transform(self):
        pass

    def get_scaled_size(self):
        model_box = self.model.get_bounding_box()
        scaled_min = model_box['min'] * self.scale
        scaled_max = model_box['max'] * self.scale
        return scaled_max - scaled_min
