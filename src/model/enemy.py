import random
from OpenGL.GL import *
from util.constants import COLORS, ENEMY
from model.ship import Entity

class Enemy(Entity):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z, f"enemy_{random.randint(0, ENEMY['random'])}.glb")
        self.lives = ENEMY['lives']
        self.color = random.choice(list(COLORS.values()))
        self.scale = ENEMY['scale']

    def update(self, delta: float):
        pass

    def apply_transform(self):
        glRotatef(180, 0, 1, 0)
        glRotatef(90, 1, 0, 0)
    
    def draw(self):
        super().draw()
    