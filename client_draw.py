def draw(game_map, players, bullets):
    print(chr(27) + "[2J")
    for y in range(len(game_map)):
        for x in range(len(game_map[0])):
            print("[", end='')
            printed = False
            for player in players:
                if player.x == x and player.y == y:
                    print(player.id, end='')
                    printed = True
                    break
            for bullet in bullets:
                if bullet.x == x and bullet.y == y:
                    print("*", end='')
                    printed = True
                    break
            if not printed:
                print(" ", end='')
            print("]", end='')
        print()
