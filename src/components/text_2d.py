from typing import Callable, Union, Tuple
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from util.constants import SCREEN_DIMENSIONS

class Text2D:
    def __init__(self, text: Union[str, Callable[[], str]], x: float, y: float, color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), font: int = GLUT_BITMAP_HELVETICA_12):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.font_sizes = {
            "small": GLUT_BITMAP_HELVETICA_10,
            "medium": GLUT_BITMAP_HELVETICA_12,
            "large": GLUT_BITMAP_HELVETICA_18
        }
        self.current_font_size = "medium"

    @property
    def line_height(self) -> int:
        if self.font == GLUT_BITMAP_HELVETICA_10:
          return 10
        elif self.font == GLUT_BITMAP_HELVETICA_12:
          return 12
        elif self.font == GLUT_BITMAP_HELVETICA_18:
          return 18

    def draw(self) -> None:
        current_text = self.text() if callable(self.text) else self.text

        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glDisable(GL_LIGHTING)
        glColor4f(*self.color)

        x = self.x * SCREEN_DIMENSIONS[0]
        y = self.y * SCREEN_DIMENSIONS[1]

        for index, line in enumerate(current_text.split('\n')):
            glRasterPos2f(x, y - index * self.line_height)
            for char in line:
                glutBitmapCharacter(self.font, ord(char))

        glEnable(GL_LIGHTING)
        glPopAttrib()

    def render(self) -> None:
        glPushMatrix()
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, SCREEN_DIMENSIONS[0], 0, SCREEN_DIMENSIONS[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        self.draw()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
        glPopMatrix()

    def set_font_size(self, size: str) -> None:
        """Altera o tamanho da fonte."""
        if size in self.font_sizes:
            self.font = self.font_sizes[size]
            self.current_font_size = size

    def zoom_in(self) -> None:
        """Aumenta o tamanho da fonte."""
        if self.current_font_size == "small":
            self.set_font_size("medium")
        elif self.current_font_size == "medium":
            self.set_font_size("large")

    def zoom_out(self) -> None:
        """Diminui o tamanho da fonte."""
        if self.current_font_size == "large":
            self.set_font_size("medium")
        elif self.current_font_size == "medium":
            self.set_font_size("small")
