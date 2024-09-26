import os
from components.model import Model
from util.constants import MODELS_PATH

class ModelCache:
  _models = {}

  @classmethod
  def register_model(cls, name, path):
    if name not in cls._models:
      cls._models[name] = Model(path)

  @classmethod
  def get_model(cls, name):
    if name not in cls._models: return None
    return ModelCache._models[name]

  @classmethod
  def load_models(cls):
    for root, _, files in os.walk(MODELS_PATH):
      for file in files:
        if file.endswith(('.glb', '.obj')):
          cls.register_model(file, os.path.join(root, file))
