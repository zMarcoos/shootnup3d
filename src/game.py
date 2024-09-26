import random
import pygame
import glfw

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from util.constants import *
from model.ship import Ship
from view.camera import Camera
from states.select_state import SelectState
from states.end_state import EndState
from model.star import Star
from controller.model_cache import ModelCache
from components.timer import Timer
from controller.sound_manager import SoundManager

class Game:
    def __init__(self):
        self.camera = Camera()
        self.time_to_next_level = GAME_NEXT_LEVEL_TIME
        self.level = 1
        self.score = 0
        self.player = None
        self.enemies = []
        self.shots = []
        self.stars = []
        self.state = None
        self.clock = pygame.time.Clock()

        ModelCache.load_models()
        SoundManager.init()
        self.add_star()

    def reset(self):
        self.level = 1
        self.score = 0
        self.player = Ship(0, 0, 0.7)
        self.shots.clear()
        self.enemies.clear()
        self.time_to_next_level = GAME_NEXT_LEVEL_TIME
        self.camera.to_default_position()

    def add_star(self):
        if len(self.stars) >= GAME_MAX_STARS:
            return

        x = random.uniform(GAME_BOUNDS['X'][0], GAME_BOUNDS['X'][1])
        y = 0
        z = random.uniform(GAME_BOUNDS['Z'][0], GAME_BOUNDS['Z'][1])
        self.stars.append(Star(x, y, z))

        Timer.add_timer(0, self.add_star)

    def is_within_arena(self, position):
        return (GAME_BOUNDS['X'][0] <= position.x <= GAME_BOUNDS['X'][1] and
                GAME_BOUNDS['Y'][0] <= position.y <= GAME_BOUNDS['Y'][1] and
                GAME_BOUNDS['Z'][0] <= position.z <= GAME_BOUNDS['Z'][1])

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)

        self.state.draw()

        for star in self.stars:
            star.draw()

        glfw.swap_buffers(self.window)

        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

    def update(self):
        self.clock.tick(FPS)
        delta_time = self.clock.get_time() / 1000.0

        self.state.update(delta_time)

        for star in self.stars:
            star.update(delta_time)

            if not self.is_within_arena(star.position):
                star.position.x = random.uniform(GAME_BOUNDS['X'][0], GAME_BOUNDS['X'][1])
                star.position.y = 0
                star.position.z = random.uniform(GAME_BOUNDS['Z'][0], GAME_BOUNDS['Z'][1])

        Timer.update_timers()

    def game_over(self):
        if not self.player.is_alive():
            self.state = EndState(self)

    def handle_key(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(self.window, True)
                return

            self.state.handle_key_down(key, mods)
        elif action == glfw.RELEASE:
            self.state.handle_key_up(key, mods)

    def handle_mouse_motion(self, window, xpos, ypos):
        self.state.handle_mouse_motion(xpos, ypos)

    def handle_mouse(self, window, button, action, mods):
        if action == glfw.PRESS:
            self.state.handle_mouse(button, action, 0, 0)
        elif action == glfw.RELEASE:
            self.state.handle_mouse(button, action, 0, 0)

    def reshape(self, window, width, height):
        global SCREEN_DIMENSIONS
        SCREEN_DIMENSIONS = (width, height)

        if height == 0:
            height = 1

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width / height, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def run(self):
        if not glfw.init():
            raise Exception("GLFW não pôde ser inicializado.")

        self.window = glfw.create_window(*SCREEN_DIMENSIONS, "Shoot 'em up - Thevelopers", None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("GLFW não conseguiu criar a janela.")

        glfw.set_window_pos(self.window, 100, 50)
        glfw.make_context_current(self.window)

        glfw.set_key_callback(self.window, self.handle_key)
        glfw.set_cursor_pos_callback(self.window, self.handle_mouse_motion)
        glfw.set_mouse_button_callback(self.window, self.handle_mouse)
        glfw.set_window_size_callback(self.window, self.reshape)

        glutInit()
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.state = SelectState(self)

        glClearColor(0.02, 0.02, 0.1, 1.0)
        glViewport(0, 0, *SCREEN_DIMENSIONS)

        while not glfw.window_should_close(self.window):
            self.draw()
            self.update()
            glfw.poll_events()

        glfw.terminate()
