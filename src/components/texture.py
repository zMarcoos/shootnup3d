from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from util.constants import SCREEN_DIMENSIONS

class Texture:
    def __init__(self, image_path: str) -> None:
        self.image_path = image_path
        self.texture_id = None
        self.load_texture()

    def load_texture(self) -> None:
        image = Image.open(self.image_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image_data = image.convert('RGBA').tobytes()

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def bind(self) -> None:
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

    def unbind(self) -> None:
        glBindTexture(GL_TEXTURE_2D, 0)

    def draw_2d(self, x: float, y: float, width: float, height: float) -> None:
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, SCREEN_DIMENSIONS[0], 0, SCREEN_DIMENSIONS[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        self.bind()

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex2f(x, y)
        glTexCoord2f(1.0, 0.0); glVertex2f(x + width, y)
        glTexCoord2f(1.0, 1.0); glVertex2f(x + width, y + height)
        glTexCoord2f(0.0, 1.0); glVertex2f(x, y + height)
        glEnd()

        self.unbind()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
