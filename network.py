import socket
import struct
import json
from server_models import Player


def send_data(conn_sock: socket.socket, data):
    length = len(data)
    conn_sock.send(struct.pack("h", length) + data.encode("utf-8"))


def send_init_details(player: Player, game):
    data = str(player.id) + ":" + json.dumps(game.map)
    send_data(player.socket, data)


def send_periodic(conn_sock: socket.socket, game):
    data = str(game.players) + ":" + str(game.bullets) # both players and bullets are json serializable by default
    send_data(conn_sock, data)
