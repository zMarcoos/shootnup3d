import glm
from OpenGL.GL import *
from OpenGL.GLUT import *
from util.constants import COLORS, SHOT
from model.interface.collidable import Collidable
from controller.texture_cache import TextureCache
from util.constants import SHOT_TEXTURE

class Shot(Collidable):
    def __init__(self, x, y, z, from_player, kind):
        self.position = glm.vec3(x, y, z)
        self.from_player = from_player
        self.kind = kind
        self.velocity = SHOT['velocity']
        self.size = SHOT[kind]['size']
        self.damage = SHOT[kind]['damage']
        self.texture = TextureCache.get_texture(SHOT_TEXTURE)

    def is_hit_by(self, other: 'Collidable') -> bool:
        box = self.bounding_box()
        target_box = other.bounding_box()
        return Collidable.aabb_collision(box['min'], box['max'], target_box['min'], target_box['max'])

    def bounding_box(self):
        return Collidable.get_aabb(self.position, self.size)

    def update(self, delta):
        if self.from_player:
            self.position.z -= self.velocity * delta
        else:
            self.position.z += self.velocity * delta

    def draw(self):
        glPushAttrib(GL_CURRENT_BIT | GL_LIGHTING_BIT)
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glScalef(self.size.x, self.size.y, self.size.z)

        if self.texture:
            glDisable(GL_LIGHTING)
            self.texture.bind()
            glBegin(GL_QUADS)

            # Face frontal
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5,  0.5)
            glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.5,  0.5)
            glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.5,  0.5)
            glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.5,  0.5)

            # Face traseira
            glTexCoord2f(0.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
            glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
            glTexCoord2f(1.0, 1.0); glVertex3f(-0.5,  0.5, -0.5)
            glTexCoord2f(0.0, 1.0); glVertex3f( 0.5,  0.5, -0.5)

            # Face esquerda
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
            glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5,  0.5)
            glTexCoord2f(1.0, 1.0); glVertex3f(-0.5,  0.5,  0.5)
            glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.5, -0.5)

            # Face direita
            glTexCoord2f(0.0, 0.0); glVertex3f( 0.5, -0.5,  0.5)
            glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
            glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.5, -0.5)
            glTexCoord2f(0.0, 1.0); glVertex3f( 0.5,  0.5,  0.5)

            # Face superior
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5,  0.5,  0.5)
            glTexCoord2f(1.0, 0.0); glVertex3f( 0.5,  0.5,  0.5)
            glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.5, -0.5)
            glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.5, -0.5)

            # Face inferior
            glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
            glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
            glTexCoord2f(1.0, 1.0); glVertex3f( 0.5, -0.5,  0.5)
            glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, -0.5,  0.5)

            glEnd()
            self.texture.unbind()
            glEnable(GL_LIGHTING)
        else:
            glMaterialfv(GL_FRONT, GL_AMBIENT, COLORS['white'])
            glutSolidCube(1.0)

        glPopMatrix()
        glPopAttrib()
