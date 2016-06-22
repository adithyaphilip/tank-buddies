from client_models import Player
from client_models import Bullet
import json

def interpret_initial(data: str):
    #game_map=json.loads(data.split(":")[1])
    print(data)
    game_map=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    #game_map = eval(data.split(":")[1])
    return game_map


def interpret_periodic(data: str):
    try:
        players_s, bullets_s = map(eval, data.split(":"))
        players = [Player(*player) for player in players_s]
        bullets = [Bullet(*bullet) for bullet in bullets_s]
        return players, bullets
    except:
        return [],[]
