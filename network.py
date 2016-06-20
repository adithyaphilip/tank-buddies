import socket
from game_helper import Player


def send_init_details(player: Player, game):
    data = str(player.id) + ":" + str(game.map)
    player.socket.send(data.encode("utf-8"))


def send_periodic(conn_sock: socket.socket, game):
    data = str(game.players) + ":" + str(game.bullets)
    conn_sock.send(data.encode("utf-8"))
