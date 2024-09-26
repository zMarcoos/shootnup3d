import glm
import random

from OpenGL.GL import *
from util.constants import COLORS, STAR
from components.timer import Timer

class Star:
    def __init__(self, x, y, z):
        self.position = glm.vec3(x, y, z)
        self.color = random.choice(list(COLORS.values()))
        self.size = random.uniform(0.01, 0.03)
        self.blink_interval = random.uniform(0.5, 5.0)
        self.is_visible = True
        
        self.blink()
    
    def blink(self):
        self.is_visible = not self.is_visible
        Timer.add_timer(self.blink_interval, self.blink)

    def update(self, delta_time):
        self.position.z += delta_time * STAR['velocity']

    def draw(self):
        if not self.is_visible:
            return
        
        glPushAttrib(GL_CURRENT_BIT | GL_LIGHTING_BIT)
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glScalef(self.size, self.size, self.size)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [self.color[0], self.color[1], self.color[2], 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [self.color[0], self.color[1], self.color[2], 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        
        glBegin(GL_QUADS)

        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
        
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(-1, 1, -1)
        
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, 1, -1)
        
        glVertex3f(1, -1, -1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, -1)
        
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
        
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)
        
        glEnd()

        glPopMatrix()
        glPopAttrib()
