import random
import glm
from OpenGL.GL import *
from OpenGL.GLUT import *

class Explosion:
    def __init__(self, position, count, scale, lifetime, speed, initial_size, color: glm.vec4):
        self.particles = []
        self.speed = speed
        self.lifetime = lifetime
        self.initial_size = initial_size

        for _ in range(count):
            particle = {
                'position': glm.vec3(position),
                'velocity': glm.vec3(
                    random.uniform(-1, 1) * scale,
                    random.uniform(-1, 1) * scale,
                    random.uniform(-1, 1) * scale
                ),
                'age': 0,
                'size': initial_size,
                'color': color[:],
            }

            self.particles.append(particle)

    def update(self):
        if not self.particles:
            return

        for particle in self.particles:
            particle['position'] += particle['velocity'] * self.speed
            particle['age'] += self.speed
            fade_factor = 1.0 - (particle['age'] / self.lifetime)
            particle['color'][3] = fade_factor
            particle['size'] = self.initial_size * fade_factor


        self.particles = [p for p in self.particles if p['age'] < self.lifetime]

    def draw(self):
        if not self.particles:
            return

        for particle in self.particles:
            glPushAttrib(GL_CURRENT_BIT | GL_LIGHTING_BIT)
            glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, particle['color'])
            glPushMatrix()
            glTranslatef(particle['position'].x, particle['position'].y, particle['position'].z)
            glutSolidCube(particle['size'])
            glPopMatrix()
            glPopAttrib()

    def is_done(self):
        return len(self.particles) == 0
