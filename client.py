import client_nw
import client_draw
import socket
import threading

game_map = []


def start_drawing(conn_sock: socket.socket):
    while True:
        data = conn_sock.recv(4096).decode("utf-8")
        players, bullets = client_nw.interpret_periodic(data)
        client_draw.draw(game_map, players, bullets)


def main():
    ip = input("Server IP: ")
    port = int(input("Server Port: "))
    conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_sock.connect((ip, port))

    global game_map
    game_map = client_nw.interpret_initial(conn_sock.recv(4096).decode("utf-8"))

    threading.Thread(target=start_drawing, args=(conn_sock,)).start()

    while True:
        conn_sock.send(input().encode("utf-8"))

main()
