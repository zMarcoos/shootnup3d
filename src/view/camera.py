import glm
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from util.constants import CAMERA_STATES, FPS

class Camera:
    def __init__(self, position: glm.vec3 = glm.vec3(0, 0, 0), look_at: glm.vec3 = glm.vec3(0, 0, 0)):
        self.state = 'BACK'
        self.position = position
        self.look_at = look_at
        self.x0 = 0
        self.y0 = 0
        self.alpha = 0.0
        self.beta = 0.0
        self.is_transitioning = False
        self.transition_time = 0.0
        self.transition_duration = 1.0
        self.shake_magnitude = 0.0
        self.shake_duration = 0.0
        self.shake_time = 0.0
        self.update_angles_from_look_at()
        self.to_default_position()

    def apply(self):
        if self.is_transitioning:
            self.update_transition()
        elif self.shake_time > 0:
            self.update_shake()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(67, 48 / 32, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            *self.position,
            *self.look_at,
            0, 1, 0
        )

    def start_shake(self, magnitude: float, duration: float):
        self.shake_magnitude = magnitude
        self.shake_duration = duration
        self.shake_time = duration

    def update_shake(self):
        if self.shake_time > 0:
            self.shake_time -= 1.0 / FPS

            shake_offset = glm.vec3(
                random.uniform(-1, 1) * self.shake_magnitude,
                random.uniform(-1, 1) * self.shake_magnitude,
                random.uniform(-1, 1) * self.shake_magnitude
            )

            self.position += shake_offset
            self.shake_magnitude *= 0.9

            if abs(self.shake_time) < 0.01:
                self.shake_time = 0.0

                if self.state != 'BACK':
                    self.reset_to_state()

    def reset_to_state(self):
        state_info = CAMERA_STATES[self.state]
        target_position = glm.vec3(state_info['position'])
        target_look_at = glm.vec3(state_info['look_at'])

        self.start_transition(target_position, target_look_at, duration=0.5)

    def handle_mouse_motion(self, x, y):
        dx, dy = x - self.x0, y - self.y0
        self.beta += dx * 0.1
        self.alpha = glm.clamp(self.alpha - dy * 0.1, -89.0, 89.0)
        self.x0, self.y0 = x, y
        self.update_look_at()

    def to_default_position(self):
        self.position = glm.vec3(CAMERA_STATES['DEFAULT']['position'])
        self.look_at = glm.vec3(CAMERA_STATES['DEFAULT']['look_at'])
        self.update_angles_from_look_at()

    def handle_mouse(self, button, state, x, y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            self.x0, self.y0 = x, y

    def set_position(self, x, y, z):
        self.position = glm.vec3(x, y, z)
        self.update_angles_from_look_at()

    def set_look_at(self, x, y, z):
        self.look_at = glm.vec3(x, y, z)
        self.update_angles_from_look_at()

    def update_angles_from_look_at(self):
        direction = glm.normalize(self.look_at - self.position)
        self.alpha = glm.degrees(glm.asin(direction.y))
        self.beta = glm.degrees(glm.atan(direction.z, direction.x))

    def change_state(self):
        states = list(CAMERA_STATES.keys())[1:]

        next_index = (states.index(self.state) + 1) % len(states)

        self.state = states[next_index]
        self.reset_to_state()

    def follow(self, target_position, offset=glm.vec3(0, 2, 2), look_at_offset=glm.vec3(0.0012633, 1.63583, 1.06867), smoothness=0.1):
        desired_position = target_position + offset
        desired_look_at = target_position + look_at_offset

        self.position = glm.mix(self.position, desired_position, smoothness)
        self.look_at = glm.mix(self.look_at, desired_look_at, smoothness)

    def start_transition(self, target_position, target_look_at, duration):
        self.start_position = glm.vec3(self.position)
        self.start_look_at = glm.vec3(self.look_at)
        self.target_position = glm.vec3(target_position)
        self.target_look_at = glm.vec3(target_look_at)
        self.transition_time = 0.0
        self.transition_duration = duration
        self.is_transitioning = True

    def update_transition(self):
        if self.transition_time < self.transition_duration:
            t = self.transition_time / self.transition_duration
            self.position = glm.mix(self.start_position, self.target_position, t)
            self.look_at = glm.mix(self.start_look_at, self.target_look_at, t)
            self.transition_time += 1.0 / FPS
        else:
            self.position = self.target_position
            self.look_at = self.target_look_at
            self.is_transitioning = False

    def update_look_at(self):
        direction = glm.vec3(
            glm.cos(glm.radians(self.alpha)) * glm.cos(glm.radians(self.beta)),
            glm.sin(glm.radians(self.alpha)),
            glm.cos(glm.radians(self.alpha)) * glm.sin(glm.radians(self.beta))
        )
        self.look_at = self.position + glm.normalize(direction)
