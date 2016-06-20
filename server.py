import socket
import threading
import server_models
from server_models import Player
from constants import GAME_INTERVAL
from constants import Direction
import network
import select

game = None

BUFFER_SIZE = 1024


def start_listening_for_input(player: Player):
    if player not in game.players:
        return
    threading.Timer(GAME_INTERVAL, start_listening_for_input, (player,)).start()
    ready = select.select([player.socket], [], [], GAME_INTERVAL)
    if ready[0]:
        move = int(player.socket.recv(1024).decode("utf-8"))
        print("Read move", move, "from player", player.id)
        server_models.lock.acquire()
        server_models.Move(move).make_move(player, game)
        server_models.lock.release()


def start_periodic_sending(player: Player):
    threading.Timer(GAME_INTERVAL, start_periodic_sending, (player, )).start()
    server_models.lock.acquire()
    network.send_periodic(player.socket, game)
    server_models.lock.release()


def start_simulation():
    threading.Timer(GAME_INTERVAL, start_simulation).start()
    server_models.lock.acquire()
    game.next_instance()
    server_models.lock.release()


def handle_player(player):
    network.send_init_details(player, game)
    start_listening_for_input(player)
    start_periodic_sending(player)


def main():
    server_port = int(input("Desired server port: "))
    num_pl = int(input("Desired number of players: "))
    map_file = input("Enter desired map: ")

    if num_pl > 4:
        print("Players limited to 4 right now, until pos is changed to support more starting positions")

    game_map = server_models.read_map(map_file)

    if game_map is None:
        print("Failed to create game map, exiting")
        exit(1)

    pos = [(0, 0), (0, len(game_map) - 1), (len(game_map[0]) - 1, 0), (len(game_map[0]) - 1, len(game_map) - 1)]

    server_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('', server_port))

    players = []

    for i in range(num_pl, 0, -1):
        print("Waiting for %d more player%s to join" % (i, '' if i == 1 else 's'))
        server_sock.listen(1)
        conn_sock, addr = server_sock.accept()
        player = Player(conn_sock, num_pl - i)
        x, y = pos.pop()
        player.setup(x, y, Direction.LEFT)
        players.append(player)

    print("Beginning game!")

    global game
    game = server_models.get_game(players, map_file)

    player_threads = [threading.Thread(target=handle_player, args=(player,)) for player in players]
    for thread in player_threads:
        thread.start()

    start_simulation()


main()
