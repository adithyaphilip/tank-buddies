class Player:
    def __init__(self, player_id, x, y, direction):
        self.id = int(player_id)
        self.x = int(x)
        self.y = int(y)
        self.direction = int(direction)


class Bullet:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
