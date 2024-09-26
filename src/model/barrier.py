import random
import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
from particles.explosion import Explosion
from model.interface.collidable import Collidable
from util.constants import COLORS, BARRIER

class Brick:
    def __init__(self, position: glm.vec3, size: glm.vec3, color: glm.vec4):
        self.position = position
        self.size = size
        self.color = color

    def draw(self):
        glPushAttrib(GL_CURRENT_BIT | GL_LIGHTING_BIT)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color)
        
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glScalef(self.size.x, self.size.y, self.size.z)
        glutSolidCube(1.0)
        glPopMatrix()
        
        glPopAttrib()

class Barrier(Collidable):
    def __init__(self, position: glm.vec3):
        self.position = position
        self.explosions = []
        self.hit_count = 0
        self.hit_limit = 7
        self.brick_size = BARRIER['brickSize']
        self.columns = BARRIER['columns']
        self.rows = BARRIER['rows']
        self.color = list(COLORS.values())[random.randint(0, len(COLORS) - 1)]
        self.bricks = self.build_barrier()

    def build_barrier(self):
        bricks = []
        half_columns = (self.columns - 1) / 2
        half_rows = (self.rows - 1) / 2

        for row in range(self.rows):
            for column in range(self.columns):
                if self.is_hole_position(row, column):
                    continue

                x = (column - half_columns) * self.brick_size.x
                y = (row - half_rows) * self.brick_size.y
                position = glm.vec3(self.position.x + x, self.position.y + y, self.position.z)
                bricks.append(Brick(position, self.brick_size, self.color))

        return bricks

    def is_hole_position(self, row, column):
        return (
            (row == 2 and 3 < column < self.columns - 4) or
            (row < 2 and 2 < column < self.columns - 3) or
            (row == self.rows - 1 and (column == 0 or column == self.columns - 1))
        )

    def draw(self):
        for brick in self.bricks:
            brick.draw()
        
        for explosion in self.explosions:
            explosion.draw()

    def update(self, delta_time):
        self.explosions = [exp for exp in self.explosions if not exp.is_done()]
        for explosion in self.explosions:
            explosion.update()

    def on_hit(self):
        if self.bricks:
            explosion_position = random.choice(self.bricks).position
            self.explosions.append(Explosion(explosion_position, 5, 0.05, 10.0, 0.2, 0.2, self.color))

    def on_destroy(self):
        for brick in self.bricks:
            self.explosions.append(Explosion(brick.position, 2, 0.1, 30.0, 0.5, 0.4, self.color))
        self.bricks.clear()

    def destroy_barrier(self):
        self.on_destroy()

    def is_colliding(self, entity) -> bool:
        if not self.bricks: return False
        
        entity_box = entity.bounding_box()
        barrier_box = self.bounding_box()

        return (
            entity_box['min'].x <= barrier_box['max'].x and entity_box['max'].x >= barrier_box['min'].x and
            entity_box['min'].y <= barrier_box['max'].y and entity_box['max'].y >= barrier_box['min'].y and
            entity_box['min'].z <= barrier_box['max'].z and entity_box['max'].z >= barrier_box['min'].z
        )

    def is_hit_by(self, entity) -> bool:
        return self.bricks and self.is_colliding(entity)
    
    def damage(self, damage: float):
        self.hit_count += damage
        self.on_hit()

        if self.hit_count >= self.hit_limit:
            self.destroy_barrier()

    def bounding_box(self) -> dict:
        half_size = glm.vec3(
            self.brick_size.x * self.columns / 2,
            self.brick_size.y * self.rows / 2,
            self.brick_size.z / 2
        )

        return {
            'min': self.position - half_size,
            'max': self.position + half_size
        }
