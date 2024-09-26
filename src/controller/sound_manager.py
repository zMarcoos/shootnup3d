import pygame
import os
from util.constants import SOUNDS_PATH, SOUNDS_VOLUMES

class SoundManager:
    _sounds = {}

    @staticmethod
    def init():
        pygame.mixer.init()
        SoundManager.load_sounds()

    @staticmethod
    def load_sounds():
        for root, _, files in os.walk(SOUNDS_PATH):
            for file in files:
                if file.endswith(('wav', 'mp3', 'mp4', 'ogg')):
                    SoundManager._sounds[file] = pygame.mixer.Sound(os.path.join(root, file))

    def is_playing(self):
        return pygame.mixer.get_busy()

    @staticmethod
    def get_sound(file_name):
        sound = SoundManager._sounds.get(file_name, None)

        if not sound:
            sound_path = os.path.join(SOUNDS_PATH, file_name)
            if os.path.exists(sound_path):
                try:
                    sound = pygame.mixer.Sound(sound_path)
                    SoundManager._sounds[file_name] = sound
                except pygame.error as e:
                    return None
            else:
                return None

        return sound

    @staticmethod
    def play_sound(file_name, volume=None, loop=False):
        sound = SoundManager.get_sound(file_name)

        if not sound:
            print(f"Erro: Som '{file_name}' não pôde ser carregado.")
            return

        if volume is None:
            volume = SOUNDS_VOLUMES.get(file_name, 1.0)

        try:
            if loop:
                pygame.mixer.stop()
                sound.play(-1).set_volume(volume)
            else:
                sound.play().set_volume(volume)
        except Exception as e:
            pass
