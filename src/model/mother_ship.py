import glm
import random

from OpenGL.GL import *
from util.constants import MOTHER_SHIP
from model.entity import Entity
from components.timer import Timer
from controller.sound_manager import SoundManager

class MotherShip(Entity):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z, MOTHER_SHIP['model'])
        self.is_visible = False
        self.interval = MOTHER_SHIP['interval']
        self.sound_interval = MOTHER_SHIP['sound_interval']
        self.lives = 0
        self.velocity = MOTHER_SHIP['velocity']
        self.scale = MOTHER_SHIP['scale']
        self.direction = "leftToRight"
        self.fire_timer = 0
        self.fire_rate = MOTHER_SHIP['fire_rate']
        self.angle_offset = 0

        self.deactivate()

    def activate(self):
        self.lives = MOTHER_SHIP['lives']
        self.direction = "leftToRight"
        self.is_visible = True
        self.angle_offset = 0

    def deactivate(self):
        self.is_visible = False
        self.position = glm.vec3(self.original_position)

        Timer.add_timer(self.interval, self.activate)

    def start_moving(self, delta_time):
        move_distance = self.velocity * delta_time

        if self.direction == "leftToRight":
            self.position.x += move_distance
            if self.position.x > 15:
                self.direction = "rightToLeft"
        else:
            self.position.x -= move_distance
            if self.position.x < -15:
                self.direction = "leftToRight"

        self.angle_offset += self.velocity * delta_time + 2
        if self.angle_offset > 360:
            self.angle_offset -= 360

        if not Timer.has_timer('mother_ship_sound'):
            Timer.add_timer(self.sound_interval, lambda: SoundManager.play_sound('mother_ship.wav'), 'mother_ship_sound')

    def update(self, delta_time):
        if self.is_visible:
            self.start_moving(delta_time)

    def apply_transform(self):
        glRotatef(-90, 1, 0, 0)
        glRotatef(self.angle_offset, 0, 1, 0)

    def draw(self):
        super().draw()

    def damage(self, amount: float = 1.0):
        super().damage(amount)

        if self.lives > 0:
            self.is_invulnerable = True
            Timer.add_timer(6.0, lambda: self.set_invulnerability(False))
