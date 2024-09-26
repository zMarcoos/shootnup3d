from OpenGL.GL import *
from OpenGL.GLU import *
from util.constants import SCREEN_DIMENSIONS

def draw_frame(x1, y1, x2, y2, line_width=3.0, color=(1.0, 1.0, 1.0)):
  glMatrixMode(GL_PROJECTION)
  glPushMatrix()
  glLoadIdentity()
  gluOrtho2D(0, SCREEN_DIMENSIONS[0], 0, SCREEN_DIMENSIONS[1])
  glMatrixMode(GL_MODELVIEW)
  glPushMatrix()
  glLoadIdentity()

  glDisable(GL_LIGHTING)

  glColor3f(*color)
  glLineWidth(line_width)
  glBegin(GL_LINE_LOOP)
  glVertex2f(x1, y1)
  glVertex2f(x2, y1)
  glVertex2f(x2, y2)
  glVertex2f(x1, y2)
  glEnd()

  glEnable(GL_LIGHTING)

  glMatrixMode(GL_PROJECTION)
  glPopMatrix()
  glMatrixMode(GL_MODELVIEW)
  glPopMatrix()