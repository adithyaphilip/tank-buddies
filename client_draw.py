from PIL import  Image,ImageTk

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



def draw2_initial(game_map,game_window):
    for index,row in enumerate(game_map):
        for index2,column in enumerate(row):
            print(column)
            if(column==1):
                game_window.create_rectangle(index*75,index2*75,(index+1)*75,(index2+1)*75,fill="brown")
remove_list=[]
def draw2(game_map,players,bullets,game_window):
    f=0
    global remove_list
    for item in remove_list:
        game_window.delete(item)
    remove_list=[]
    for player in players:
        remove_list.append(game_window.create_rectangle(player.x*75,player.y*75,(player.x+1)*75,(player.y+1)*75,fill="red"))

    for bullet in bullets:
        remove_list.append(game_window.create_rectangle(bullet.x*75,bullet.y*75,(bullet.x+1)*75,(bullet.y+1)*75,fill="pink"))


