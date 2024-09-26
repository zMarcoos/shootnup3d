from OpenGL.GL import *
from OpenGL.GLU import *
from enum import Enum, auto
from components.text_2d import Text2D
from states.game_state import GameState
from states.active_state import ActiveState
from util.file_util import load_high_scores
from util.constants import *
from util.painter import draw_frame
from controller.texture_cache import TextureCache
from controller.sound_manager import SoundManager
import os

class ScreenState(Enum):
    PRINCIPAL = auto()
    LEADERBOARD = auto()
    CREDITS = auto()

class SelectState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.screen_state = ScreenState.PRINCIPAL
        self.current_page = 0
        self.items_per_page = 15
        self.leaderboard_data = self.load_leaderboard_data()
        self.logo_texture = TextureCache.get_texture(os.path.join(IMAGES_PATH, 'logo.png'))
        self.credits_offset = -SCREEN_DIMENSIONS[1] / 4
        self.credits_paused = False
        self.credits_speed = 1
        self.credits_text = Text2D(TEXTS['credits'], 0.2, self.credits_offset / SCREEN_DIMENSIONS[1] + 0.1)
        SoundManager.play_sound('select_background.wav', loop=True)

        self.key_actions = {
            257: self.start_active_state,  # Enter
            335: self.start_active_state,  # Numpad Enter
            67: lambda: self.change_screen_state(ScreenState.CREDITS, 'select.wav'),  # 'C' para Créditos
            76: lambda: self.change_screen_state(ScreenState.LEADERBOARD, 'select.wav'),  # 'L' para Leaderboard
            66: self.handle_back_key,  # 'B' para voltar
            80: self.handle_previous_page,  # 'P' para página anterior
            78: self.handle_next_page,  # 'N' para próxima página
            32: self.toggle_pause_credits,  # 'Espaço' para pausar créditos
            265: self.zoom_in_credits,  # 'Seta para cima' para aumentar tamanho da fonte
            264: self.zoom_out_credits,  # 'Seta para baixo' para diminuir tamanho da fonte
            87: self.move_credits_up,  # 'W' para mover créditos para cima
            83: self.move_credits_down,  # 'S' para mover créditos para baixo
            65: self.move_credits_left,  # 'A' para mover créditos para a esquerda
            68: self.move_credits_right  # 'D' para mover créditos para a direita
        }

    def load_leaderboard_data(self):
        scores = load_high_scores()
        return sorted(scores.items(), key=lambda item: item[1], reverse=True) if scores else None

    def draw(self):
        self.game.camera.apply()
        self.setup_lighting()

        if self.screen_state == ScreenState.PRINCIPAL:
            self.draw_principal()
        elif self.screen_state == ScreenState.LEADERBOARD:
            self.draw_leaderboard()
        elif self.screen_state == ScreenState.CREDITS:
            self.draw_credits()

    def draw_principal(self):
        self.draw_frame_and_logo(TEXTS['select'])

    def draw_leaderboard(self):
        self.draw_frame_and_logo()

        if not self.leaderboard_data:
            Text2D('Nenhum registro ainda.', 0.45, 0.5).render()
        else:
            self.render_leaderboard()

        Text2D('B para voltar', 0.45, 0.2).render()

    def render_leaderboard(self):
        start_index = self.current_page * self.items_per_page
        page_data = self.leaderboard_data[start_index:start_index + self.items_per_page]

        for index, (name, score) in enumerate(page_data):
            Text2D(f'{start_index + index + 1}. {name}: {score}', 0.45, 0.7 - index * 0.03).render()

        if self.current_page > 0:
            Text2D('P para Anterior', 0.27, 0.3).render()
        if (start_index + self.items_per_page) < len(self.leaderboard_data):
            Text2D('N para Próximo', 0.65, 0.3).render()

    def draw_credits(self):
        self.credits_text.y = self.credits_offset / SCREEN_DIMENSIONS[1] + 0.1
        self.credits_text.render()

        if not self.credits_paused:
            self.credits_offset += self.credits_speed

        line_count = len(TEXTS['credits'].split('\n'))
        total_text_height = line_count * self.credits_text.line_height
        max_offset = (total_text_height / SCREEN_DIMENSIONS[1]) * 3

        print(max_offset)

        if self.credits_offset / SCREEN_DIMENSIONS[1] > max_offset:
            self.reset_credits()
            SoundManager.play_sound('select_background.wav', loop=True)

    def reset_credits(self):
        self.credits_offset = -SCREEN_DIMENSIONS[1] / 4
        self.screen_state = ScreenState.PRINCIPAL

    def draw_frame_and_logo(self, text=None):
        draw_frame(SCREEN_DIMENSIONS[0] * 0.25,
                   SCREEN_DIMENSIONS[1] * 0.75,
                   SCREEN_DIMENSIONS[0] * 0.75,
                   SCREEN_DIMENSIONS[1] * 0.25)
        if text:
            Text2D(text, 0.45, 0.55).render()
            self.logo_texture.draw_2d(SCREEN_DIMENSIONS[0] * 0.33, SCREEN_DIMENSIONS[1] * 0.65, 400, 200)

    def handle_key_down(self, key, mods):
        action = self.key_actions.get(key)
        if action:
            action()

    def start_active_state(self):
        self.game.state = ActiveState(self.game)
        SoundManager.play_sound('select.wav')

    def change_screen_state(self, new_state, sound):
        if new_state == self.screen_state: return
        self.screen_state = new_state
        SoundManager.play_sound(sound)

        if new_state == ScreenState.CREDITS:
            SoundManager.play_sound('credits_background.wav', loop=True)

    def handle_back_key(self):
        if self.screen_state == ScreenState.LEADERBOARD:
            self.screen_state = ScreenState.PRINCIPAL
            SoundManager.play_sound('back.wav')

    def handle_previous_page(self):
        if self.screen_state == ScreenState.LEADERBOARD and self.current_page > 0:
            self.current_page -= 1
            SoundManager.play_sound('back.wav')

    def handle_next_page(self):
        if self.screen_state == ScreenState.LEADERBOARD:
            max_pages = len(self.leaderboard_data) // self.items_per_page
            if self.current_page < max_pages:
                self.current_page += 1
                SoundManager.play_sound('select.wav')

    def toggle_pause_credits(self):
        if self.screen_state != ScreenState.CREDITS: return

        self.credits_paused = not self.credits_paused
        SoundManager.play_sound('select.wav')

    def move_credits_up(self):
        if self.screen_state != ScreenState.CREDITS: return
        self.credits_offset += 5

    def move_credits_down(self):
        if self.screen_state != ScreenState.CREDITS: return
        self.credits_offset -= 5

    def zoom_in_credits(self):
        if self.screen_state != ScreenState.CREDITS: return
        self.credits_text.zoom_in()

    def zoom_out_credits(self):
        if self.screen_state != ScreenState.CREDITS: return
        self.credits_text.zoom_out()

    def move_credits_left(self):
        if self.screen_state != ScreenState.CREDITS: return
        self.credits_text.x -= 0.02

    def move_credits_right(self):
        if self.screen_state != ScreenState.CREDITS: return
        self.credits_text.x += 0.02

    def update(self, delta_time):
        pass

    def handle_key_up(self, key, mods):
        pass

    def handle_mouse_motion(self, x, y):
        pass

    def handle_mouse(self, button, state, x, y):
        pass
