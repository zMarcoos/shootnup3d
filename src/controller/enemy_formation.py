from model.enemy import Enemy
from util.constants import GAME_BOUNDS, ENEMY

class EnemyFormation:
    def __init__(self, game):
        self.game = game
        self.direction = "right"
        self.next_direction = "left"
        self.movement_started = False
        self.formation_speed = ENEMY['formation_speed']
        self.min_x = GAME_BOUNDS['X'][0] + 5
        self.max_x = GAME_BOUNDS['X'][1] - 5
        self.min_z = GAME_BOUNDS['Z'][0]
        self.enemies = []
        self.current_size = 4
        self.build_formation()
        self.start_movement()

    def build_formation(self):
        formation_width = self.current_size
        start_x = -(formation_width / 2) + 0.5
        
        formation_depth = self.current_size
        start_z = -(formation_depth / 2) - 10
        
        for row in range(self.current_size):
            for column in range(self.current_size):
                enemy = Enemy(start_x + row, 0, start_z + column)
                self.enemies.append(enemy)
                self.game.enemies.append(enemy)

    def start_movement(self):
        self.movement_started = True

    def update_formation(self, delta_time):
        if self.movement_started:
            self.move_formation(delta_time)
            self.update_alien_positions()

    def move_formation(self, delta_time):
        self.formation_speed = ENEMY['formation_speed'] + (self.game.level * 0.01)
        
        if self.direction == "right":
            for alien in self.enemies:
                alien.position.x += self.formation_speed * delta_time
        elif self.direction == "left":
            for alien in self.enemies:
                alien.position.x -= self.formation_speed * delta_time
        elif self.direction == "down":
            for alien in self.enemies:
                alien.position.z += self.formation_speed * delta_time + 0.5
            self.direction = self.next_direction

    def update_alien_positions(self):
        for alien in self.enemies:
            position = alien.position
            self.check_edges(position)

    def check_edges(self, position):
        if position.x > self.max_x and self.direction == "right":
            self.direction = "down"
            self.next_direction = "left"
        elif position.x < self.min_x and self.direction == "left":
            self.direction = "down"
            self.next_direction = "right"
        elif position.z > 0:
            self.movement_started = False
            self.game.player.lives = 0

            self.game.game_over()

    def increase_formation_size(self):
        if self.current_size < 7:
            self.current_size += 1

        self.build_formation()
