from OpenGL.GL import *
from OpenGL.GLU import *
from components.texture import Texture

class TextureCache:
    _textures = {}

    @classmethod
    def get_texture(cls, image_path):
        if image_path not in cls._textures:
            cls._textures[image_path] = Texture(image_path)
        return cls._textures[image_path]

    @classmethod
    def clear_cache(cls):
        cls._textures.clear()