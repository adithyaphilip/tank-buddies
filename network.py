import socket


def send_init_details(conn_sock: socket.socket, game):
    data = str(len(game.players)) + ":" + str(game.map)
    conn_sock.send(data.encode("utf-8"))


def send_periodic(conn_sock: socket.socket, game):
    data = str(game.players) + ":" + str(game.bullets)
    conn_sock.send(data.encode("utf-8"))
