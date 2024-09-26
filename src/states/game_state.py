from OpenGL.GL import *
from abc import ABC, abstractmethod

class GameState(ABC):
    
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def handle_key_down(self, key, mods):
        pass

    @abstractmethod
    def handle_key_up(self, key, mods):
        pass

    @abstractmethod
    def handle_mouse_motion(self, x, y):
        pass

    @abstractmethod
    def handle_mouse(self, button, state, x, y):
        pass

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        light_position = [1.0, 1.0, 1.0, 0.0]
        light_ambient = [0.2, 0.2, 0.2, 1.0]
        light_diffuse = [0.8, 0.8, 0.8, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]

        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
