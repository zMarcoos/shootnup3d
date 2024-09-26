import os
import glm
from OpenGL.GLUT import *

ASSETS_PATH = os.path.join('resources', 'assets')
MODELS_PATH = os.path.join(ASSETS_PATH, 'models')
SOUNDS_PATH = os.path.join(ASSETS_PATH, 'sounds')
IMAGES_PATH = os.path.join(ASSETS_PATH, 'images')

SHOT_TEXTURE = os.path.join(IMAGES_PATH, 'shot.png')

SOUNDS_VOLUMES = {
  'background.wav': 0.0,
  'enemy_explosion.wav': 1.0,
  'enemy_shot.wav': 1.0,
  'hit.wav': 1.0,
  'mother_ship_explosion.wav': 1.0,
  'mother_ship.wav': 1.0,
  'player_explosion.wav': 1.0,
  'player_shot.wav': 1.0,
  'game_background.ogg': 1.0,
  'select_background.wav': 1.0,
  'select.wav': 1.0,
  'back.wav': 1.0,
  'end_background.wav': 1.0,
  'typewriter.wav': 1.0,
  'special.wav': 1.0
}

TEXTS = {
    'select': 'Shoot \'em up - Thevelopers\nPress Enter to Start\nPress L for Leaderboard\nPress C for Credits',
    'credits': 'Em uma galáxia distante, a última esperança da humanidade repousou em suas mãos.\nComo um piloto corajoso, você enfrentou ondas intermináveis de invasores intergalácticos, \ndemonstrando destreza, estratégia e bravura. As naves inimigas caíram uma a uma sob o seu comando,\n mas a verdadeira vitória foi provar que a coragem e a vontade humana não podem ser destruídas.\n\nEssa jornada cósmica, uma homenagem ao clássico Space Invaders, reimagina o confronto em uma dimensão 3D. \nEsperamos que você tenha se divertido tanto quanto nós nos divertimos criando este universo de pixels, \nexplosões e nostalgia.\n\nLembre-se: o universo é vasto e cheio de mistérios. Talvez, em algum lugar, outros desafios estejam esperando \npor você, comandante. Até lá, continue explorando e nunca deixe de mirar nas estrelas!\n\nEquipe de Desenvolvimento\nIsis Lavor\nMarcos Grégory\n\nProfessor: Prof. Dr. Rafael Ivo\nDisciplina: Computação Gráfica\n'
}

COLORS = {
  'green': [0.0, 1.0, 0.0, 1.0],
  'red': [1.0, 0.0, 0.0, 1.0],
  'blue': [0.0, 0.0, 1.0, 1.0],
  'yellow': [1.0, 1.0, 0.0, 1.0],
  'orange': [1.0, 0.5, 0.0, 1.0],
  'black': [0.0, 0.0, 0.0, 1.0],
  'gray': [0.7, 0.7, 0.7, 1.0],
  'silver': [0.9, 0.9, 0.9, 1.0],
  'white': [1.0, 1.0, 1.0, 1.0],
}

CAMERA_STATES = {
  'DEFAULT': {
    'position': glm.vec3(0, 6, 10),
    'look_at': glm.vec3(1.99378e-16, 5.28963, 1.29617)
  },
  'BACK': {
    'position': glm.vec3(0, 2, 2.7),
    'look_at': glm.vec3(0.0012633, 1.63583, 1.76867)
  },
  'FRONT': {
    'position': glm.vec3(0, 8, -19),
    'look_at': glm.vec3(-0.000851159, 7.31418, -18.2722)
  },
  'UP': {
    'position': glm.vec3(0, 15, -6),
    'look_at': glm.vec3(-3.17915e-05, 14.0002, -6.01745)
  }
}

SCREEN_DIMENSIONS = (1140, 648)
GAME_BOUNDS = {
  'X': (-10, 10),
  'Y': (-5, 10),
  'Z': (-25, 15)
}
GAME_NEXT_LEVEL_TIME = 50
GAME_MAX_STARS = 50

FPS = 60.0

SHIP = {
  'model': 'player.glb',
  'lives': 3,
  'max_rotation': 15.0,
  'scale': glm.vec3(0.05, 0.05, 0.05),
  'velocity': 5,
  'rotation_speed': 8
}

ENEMY = {
  'random': 2,
  'scale': glm.vec3(0.1, 0.1, 0.5),
  'lives': 1,
  'formation_speed': 1,
}

MOTHER_SHIP = {
  'model': 'mother_ship.glb',
  'lives': 5,
  'velocity': 1.5,
  'scale': glm.vec3(0.3, 0.3, 0.3),
  'fire_rate': 1,
  'sound_interval': 0.5,
  'interval': 30
}

STAR = {
  'velocity': 2,
}

SHOT = {
  'velocity': 6,
  'regular': {
    'size': glm.vec3(0.05, 0.05, 0.5),
    'damage': 1
  },
  'super': {
    'size': glm.vec3(0.3, 0.3, 1.0),
    'damage': 3
  }
}

BARRIER = {
  'brickSize': glm.vec3(0.1, 0.1, 0.4),
  'columns': 14,
  'rows': 7,
}