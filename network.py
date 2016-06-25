import socket
import struct
import json
from server_models import Player


def send_data_udp(server_sock: socket.socket, data, addr):
    length = len(data)
    server_sock.sendto(struct.pack("h", length) + data.encode("utf-8"), addr)


def send_data(conn_sock: socket.socket, data):
    length = len(data)
    conn_sock.send(struct.pack("h", length) + data.encode("utf-8"))


def send_init_details(player: Player, game):
    data = str(player.id) + ":" + json.dumps(game.map)
    send_data(player.socket, data)


#
#
# def send_periodic(conn_sock: socket.socket, game):
#     data = str(game.players) + ":" + str(game.bullets)  # both players and bullets are json serializable by default
# #     send_data(conn_sock, data)
#
# def send_periodic(conn_sock: socket.socket, game):
#     data = str(game.players) + ":" + str(game.bullets)  # both players and bullets are json serializable by default
#     send_data(conn_sock, data)

def send_periodic(server_sock: socket.socket, game, addr):
    data = str(game.players) + ":" + str(game.bullets)  # both players and bullets are json serializable by default
    send_data_udp(server_sock, data, addr)


def listen_for_udp_reg(server_sock: socket.socket, addr_list, num_conn: int):
    # TODO: PHILAD SECURITY VULNERABILITY - some sort of validation for correct user connecting to socket
    for i in range(num_conn):
        data, addr = server_sock.recvfrom(1024)
        print("Registering addr", addr, "for udp")
        addr_list.append(addr)
        server_sock.sendto(addr, "1".encode("utf-8"))
