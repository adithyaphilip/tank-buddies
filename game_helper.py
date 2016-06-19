import threading
import socket

GAME_INTERVAL = 1 / 25  # in seconds

lock = threading.Lock()


# TODO: PHILAD

class Player:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def __init__(self, player_sock: socket.socket, player_id):
        self.socket = player_sock
        self.id = player_id
        self.x = 0
        self.y = 0
        self.direction = 0

    def setup(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def __repr__(self):
        return str([self.id, self.x, self.y, self.direction])


class Move:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    FIRE = 4
    LOOK_LEFT = 5
    LOOK_UP = 6
    LOOK_RIGHT = 7
    LOOK_DOWN = 8

    move_switch = {LEFT: (-1, 0), RIGHT: (1, 0), UP: (0, -1), DOWN: (0, 1)}

    def __init__(self, move):
        self.move = move

    def make_move(self, player: Player, game):
        game_map = game.map
        if Move.LEFT <= self.move <= Move.DOWN:
            new_x, new_y = new_pos(player.x, player.y, *Move.move_switch[self.move])
            if not is_invalid_pos(new_x, new_y, game_map):
                player.x = new_x
                player.y = new_y
        elif self.move == Move.FIRE:
            bx, by = new_pos(player.x, player.y, *Move.move_switch[player.direction])
            bullet = Bullet(Bullet.SPEED, bx, by, player.direction)
            game.add_bullet(bullet)
        elif Move.LOOK_LEFT <= self.move <= Move.LOOK_DOWN:
            player.direction = self.move - Move.LOOK_LEFT


            # TODO: PHILIP add support for other moves


class Bullet:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    SPEED = 0.25  # blocks per GAME_INTERVAL

    def __init__(self, speed, x, y, direction):
        self.speed = speed
        self.x = x
        self.y = y
        self.direction = direction

    def get_x(self):
        return int(self.x)

    def get_y(self):
        return int(self.y)

    def go_next_pos(self):
        if self.direction == Bullet.LEFT:
            self.x -= self.speed
        elif self.direction == Bullet.UP:
            self.y -= self.speed
        elif self.direction == Bullet.RIGHT:
            self.x += self.speed
        elif self.direction == Bullet.DOWN:
            self.y += self.speed

    def __repr__(self):
        return str([self.get_x(), self.get_y()])


class Game:
    OBSTACLE = 1

    def __init__(self, players: list, game_map):
        self.players = players
        self.map = game_map
        self.bullets = []

    def add_bullet(self, bullet: list):
        self.bullets.append(bullet)

    def next_instance(self):
        dead_players = []
        dead_bullets = []
        for bullet in self.bullets:
            ox = bullet.get_x()
            oy = bullet.get_y()
            bullet.go_next_pos()
            for player in self.players:
                if is_hit(ox, oy, player) or is_hit(bullet.get_x(), bullet.get_y(), player):
                    dead_players.append(player)
                    dead_bullets.append(bullet)
                elif is_invalid_pos(ox, oy, self.map) or is_invalid_pos(bullet.get_x(), bullet.get_y(), self.map):
                    dead_bullets.append(bullet)

        self.players = [player for player in self.players if player not in dead_players]
        self.bullets = [bullet for bullet in self.bullets if bullet not in dead_bullets]


def new_pos(old_x, old_y, offset_x, offset_y):
    return [old_x + offset_x, old_y + offset_y]


def is_invalid_pos(x, y, game_map):
    return x < 0 or y < 0 or x >= len(game_map[0]) or y >= len(game_map) or game_map[x][y] == Game.OBSTACLE


def is_hit(x, y, player):
    return x == player.x and y == player.y


def verify_map(game_map):
    n = len(game_map)
    if n == 0:
        return False, "0 rows in map"
    for i in range(1, n):
        row = game_map[i]
        if len(row) != len(game_map[0]):
            return False, "Length mismatch between row 0 and row %d" % i

    return True, "NP"


def read_map(file):
    with open(file) as f:
        lines = [line.strip() for line in f.readlines()]

    game_map = [list(map(int, line.split())) for line in lines]

    success, reason = verify_map(game_map)
    if success:
        return game_map
    print("MAP_PARSE_ERROR:", reason)
    return None


def get_game(players, map_file):
    game_map = read_map(map_file)
    if game_map is None:
        return None
    return Game(players, game_map)
