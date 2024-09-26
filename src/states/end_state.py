from OpenGL.GL import *
from OpenGL.GLUT import *
from components.text_2d import Text2D
from states.game_state import GameState
from util.file_util import update_high_score
from util.painter import draw_frame
from util.constants import SCREEN_DIMENSIONS
from controller.sound_manager import SoundManager
import glm
import time

class EndState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.texts = [
            'Fim de jogo!',
            lambda: f'Sua pontuação: {self.game.score}',
            lambda: f'Digite seu nome: {self.game.player.name}'
        ]
        self.start_time = time.time()
        self.fade_duration = 2.0
        self.amplitude = 0.02
        self.frequency = 2.0
        SoundManager.play_sound('end_background.wav', loop=True)

        self.key_actions = {
            259: self.remove_last_character,  # Backspace
            257: self.finalize_name_entry,    # Enter
            335: self.finalize_name_entry,    # Return
        }

    def draw(self):
        draw_frame(SCREEN_DIMENSIONS[0] * 0.25, 
                   SCREEN_DIMENSIONS[1] * 0.75, 
                   SCREEN_DIMENSIONS[0] * 0.75, 
                   SCREEN_DIMENSIONS[1] * 0.25)

        elapsed_time = time.time() - self.start_time
        fade_alpha = min(1.0, elapsed_time / self.fade_duration)

        for index, text in enumerate(self.texts):
            oscillation = glm.sin(elapsed_time * self.frequency) * self.amplitude
            text_position_y = 0.55 - index * 0.03 + oscillation
            text_content = text() if callable(text) else text
            Text2D(text_content, 0.45, text_position_y, color=(1.0, 1.0, 1.0, fade_alpha)).render()

    def update(self, delta_time):
        pass

    def handle_key_down(self, key, mods):
        action = self.key_actions.get(key)
        if action:
            action()
        elif 65 <= key <= 90:
            self.add_character_to_name(key, mods)

    def remove_last_character(self):
        if self.game.player.name:
            self.game.player.name = self.game.player.name[:-1]
            SoundManager.play_sound('typewriter.wav')

    def finalize_name_entry(self):
        if not self.game.player.name:
            return
        
        update_high_score(player_name=self.game.player.name, new_score=self.game.score)
        SoundManager.play_sound('typewriter.wav')

        from states.select_state import SelectState
        self.game.state = SelectState(self.game)

    def add_character_to_name(self, key, mods):
        if len(self.game.player.name) < 10:
            letter = chr(key).upper() if mods & 1 else chr(key).lower()
            self.game.player.name += letter
            SoundManager.play_sound('typewriter.wav')

    def handle_key_up(self, key, mods):
        pass

    def handle_mouse_motion(self, x, y):
        pass

    def handle_mouse(self, button, state, x, y):
        pass
