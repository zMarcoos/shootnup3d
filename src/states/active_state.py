import random
import glm
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from components.text_2d import Text2D
from states.game_state import GameState
from model.shot import Shot
from model.mother_ship import MotherShip
from model.barrier import Barrier
from components.cooldown import Cooldown
from particles.explosion import Explosion
from controller.enemy_formation import EnemyFormation
from util.constants import CAMERA_STATES, GAME_BOUNDS, FPS, GAME_NEXT_LEVEL_TIME, COLORS
from controller.sound_manager import SoundManager

class ActiveState(GameState):

    def __init__(self, game):
        super().__init__(game)
        self.game.reset()
        self.game.camera.start_transition(target_position=CAMERA_STATES['BACK']['position'], target_look_at=CAMERA_STATES['BACK']['look_at'], duration=2.0)
        self.mother_ship = MotherShip(GAME_BOUNDS['X'][0], 0, -15)
        self.alien_formation = EnemyFormation(self.game)
        self.explosions = []
        self.barriers = [Barrier(glm.vec3(-3, 0, -2)), Barrier(glm.vec3(3, 0, -2))]
        SoundManager.play_sound('game_background.ogg', loop=True)

    def draw(self):
        self.setup_lighting()
        self.game.camera.apply()

        self.batch_draw([self.game.player] +
            [self.mother_ship] +
            self.barriers +
            self.alien_formation.enemies +
            self.game.shots +
            self.explosions)
        self.draw_texts()

    def batch_draw(self, entities):
        for entity in entities:
            entity.draw()

    def draw_texts(self):
        Text2D(f'Pontos: {str(self.game.score)}', 0.1, 0.95).render()
        Text2D(f'Level: {str(self.game.level)}', 0.5, 0.95).render()
        Text2D(f'Vidas: {str(self.game.player.lives)}', 0.85, 0.95).render()

        if len(self.alien_formation.enemies) <= 0:
            Text2D(f'Level {str(self.game.level)} em {str(int(self.game.time_to_next_level))}', 0.5, 0.5).render()

    def update(self, delta_time):
        if not self.alien_formation.movement_started: return

        self.explosions = [explosion for explosion in self.explosions if not explosion.update() and not explosion.is_done()]

        self.mother_ship.update(delta_time)
        self.alien_formation.update_formation(delta_time)
        self.move_and_check_collisions(delta_time)
        self.mother_ship_fire_logic(delta_time)

        for barrier in self.barriers:
            barrier.update(delta_time)

        self.check_level_up(delta_time)

    def mother_ship_fire_logic(self, delta_time):
        self.mother_ship.fire_timer += delta_time
        fire_interval = 1 / self.mother_ship.fire_rate

        if self.mother_ship.is_active():
            if self.mother_ship.fire_timer > fire_interval:
                self.handle_shot(self.mother_ship.position)
                self.mother_ship.fire_timer = 0

    def move_and_check_collisions(self, delta_time):
        self.game.player.update(delta_time)
        if self.game.camera.state == 'BACK':
            self.game.camera.follow(self.game.player.position)

        self.game.player.position.x = min(max(self.game.player.position.x, GAME_BOUNDS['X'][0]), GAME_BOUNDS['X'][1])

        for enemy in self.alien_formation.enemies:
            enemy.update(delta_time)
            if enemy.is_alive() and random.randint(0, 1500) < 1:
                self.handle_shot(enemy.position, 'regular')

            for barrier in self.barriers:
                if barrier.is_hit_by(enemy):
                    barrier.damage(1)
                    break

        for shot in self.game.shots[:]:
            self.move_shot(shot, delta_time)
            if not self.game.is_within_arena(shot.position):
                self.game.shots.remove(shot)
                continue

            if shot.from_player:
                for enemy in self.alien_formation.enemies[:]:
                    if shot.is_hit_by(enemy):
                        self.handle_enemy_hit(enemy, shot)
                        break
            else:
                if self.game.player.is_hit_by(shot):
                    self.handle_player_hit()
                    self.game.shots.remove(shot)
                    continue

            for barrier in self.barriers:
                if barrier.is_hit_by(shot):
                    barrier.damage(shot.damage)
                    self.game.shots.remove(shot)
                    continue

            if shot.from_player and self.mother_ship.is_hit_by(shot):
                if self.mother_ship.is_invulnerable or not self.mother_ship.is_alive():
                    continue

                self.mother_ship.damage(shot.damage)
                SoundManager.play_sound('hit.wav')

                if not self.mother_ship.is_alive():
                    self.active_explode_particle(self.mother_ship.position)
                    self.mother_ship.deactivate()
                    self.game.score += 50

                    SoundManager.play_sound('mother_ship_explosion.wav')

                self.game.shots.remove(shot)
                continue

    def handle_enemy_hit(self, enemy, shot):
        enemy.damage(shot.damage)

        if not enemy.is_alive():
            self.active_explode_particle(enemy.position)
            self.alien_formation.enemies.remove(enemy)
            self.game.score += 10

            SoundManager.play_sound('enemy_explosion.wav')
        if not shot.kind == 'super':
            self.game.shots.remove(shot)

    def handle_player_hit(self):
        if not self.game.player.is_invulnerable and self.game.player.is_visible:
            self.active_explode_particle(self.game.player.position)
            self.game.player.damage()

            SoundManager.play_sound('player_explosion.wav')
            self.game.game_over()

    def move_shot(self, shot, delta: float):
        shot.update(delta)

    def active_explode_particle(self, position):
        self.explosions.append(Explosion(position, 20, 0.1, 30.0, 0.5, 0.4, COLORS['gray']))

    def level_up(self):
        self.game.level += 1
        self.alien_formation.increase_formation_size()
        self.barriers = [Barrier(glm.vec3(-3, 0, -2)), Barrier(glm.vec3(3, 0, -2))]

    def handle_shot(self, position: glm.vec3, kind = 'regular'):
        if self.game.camera.is_transitioning: return

        if position == self.game.player.position:
            if not self.game.player.is_visible: return

            if kind == 'super':
                if Cooldown.is_on_cooldown('super_shot'): return

                if self.game.camera.state == 'BACK':
                    self.game.camera.start_shake(0.3, 0.5)

                Cooldown.start_cooldown('super_shot', 5)
                SoundManager.play_sound('special.wav')
            else:
                SoundManager.play_sound('player_shot.wav')

            from_player = True
        else:
            SoundManager.play_sound('enemy_shot.wav')
            from_player = False

        self.game.shots.append(Shot(position.x, position.y, position.z - 0.85, from_player, kind))

    def check_level_up(self, delta_time):
        if len(self.alien_formation.enemies) <= 0:
            if self.game.time_to_next_level == 0:
                self.level_up()
                self.game.time_to_next_level = GAME_NEXT_LEVEL_TIME
            self.game.time_to_next_level = max(self.game.time_to_next_level - delta_time * FPS, 0)

    def handle_key_down(self, key, mods):
        if key == 32:
            if not self.game.player.shooting:
                self.game.player.shooting = True
                self.handle_shot(self.game.player.position)
        elif key == 81:
            self.handle_shot(self.game.player.position, 'super')
        elif key == 65:
            self.game.player.left = True
        elif key == 68:
            self.game.player.right = True
        elif key == 53:
            self.game.camera.change_state()

    def handle_key_up(self, key, mods):
        if key == 32:
            self.game.player.shooting = False
        elif key == 65:
            self.game.player.left = False
        elif key == 68:
            self.game.player.right = False

    def handle_mouse_motion(self, x, y):
        pass

    def handle_mouse(self, button, state, x, y):
        pass
