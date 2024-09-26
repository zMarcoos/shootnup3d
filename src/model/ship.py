import glm
from OpenGL.GL import *
from model.entity import Entity
from util.constants import COLORS, SHIP
from components.timer import Timer

class Ship(Entity):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z, SHIP['model'])
        self.name = ''
        self.color = COLORS['red']
        self.lives = SHIP['lives']
        self.velocity = SHIP['velocity']
        self.rotation = 0.0
        self.max_rotation = SHIP['max_rotation']
        self.scale = SHIP['scale']
        self.left = self.right = False

    def update(self, delta: float):
        super().update(delta)

        if not self.is_visible:
            return

        if self.left:
            self.position.x -= self.velocity * delta
            target_rotation = self.max_rotation
        elif self.right:
            self.position.x += self.velocity * delta
            target_rotation = -self.max_rotation
        else:
            target_rotation = 0.0

        time_step = min(delta * SHIP['rotation_speed'], 1.0)
        self.rotation = glm.mix(self.rotation, target_rotation, time_step)

    def damage(self, amount: float = 1):
        super().damage(amount)

        if self.lives > 0:
            self.is_visible = False
            
            Timer.add_timer(1.0, self.reset_position)
            Timer.add_timer(6.0, lambda: self.set_invulnerability(False))

    def apply_transform(self):
        glRotatef(270, 1, 0, 0)
        glRotatef(-self.rotation, 0, 1, 0)
