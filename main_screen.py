import tkinter as tk
from PIL import  Image,ImageTk
import socket
import client_nw
import threading
import client_draw

def start_drawing(conn_sock: socket.socket,w:tk.Canvas):
    while True:
        data = conn_sock.recv(4096).decode("utf-8")
        print("RECV",data)
        players, bullets = client_nw.interpret_periodic(data)
        client_draw.draw2(game_map, players, bullets,w)

def key_handler(event):
    conn_sock.send(event.char.encode("utf-8"))
    print("pressed",repr(event.char))

def callback():
    ip=server_name.get()
    port=int(server_port.get())
    root.destroy()
    global conn_sock
    conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_sock.connect((ip, port))
    game_window=tk.Tk()

    global game_map

    game_map = client_nw.interpret_initial(conn_sock.recv(4096).decode("utf-8"))

    print(game_map,len(game_map),len(game_map[0]))
    w=tk.Canvas(game_window,width=len(game_map)*75,height=len(game_map[0])*75)
    game_window.bind("<Key>",key_handler)
    game_window.focus_set()
    w.pack()
    client_draw.draw2_initial(game_map,w)
    threading.Thread(target=start_drawing, args=(conn_sock,w)).start()
    game_window.mainloop()

root=tk.Tk()
root.geometry("600x500")
image=Image.open("./resources/logo.png")
photo=ImageTk.PhotoImage(image)
logo=tk.Label(image=photo)
logo.pack()
server_name=tk.StringVar()
server_port=tk.StringVar()
name=tk.Label(root,text="Enter server IP",font=("Helvetica", 20))
port=tk.Label(root,text="Enter server Port",font=("Helvetica", 20))
name.pack()
e = tk.Entry(root, textvariable=server_port,font=("Helvetica", 20))
e1 = tk.Entry(root, textvariable=server_name,font=("Helvetica", 20))

e1.pack()
port.pack()
e.pack()
root.focus_set()

play_image=Image.open("./resources/play.png")
play_photo=ImageTk.PhotoImage(play_image)
playButton=tk.Button(image=play_photo,command=callback)
playButton.pack(side=tk.BOTTOM)
root.mainloop()