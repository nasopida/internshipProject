
import select
import socket
import os
import sys
import queue
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from multiprocessing import Process

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import packet

##################################
# Debug opt
DEBUG = True

# Client Dict
# Clients = {}

# Users Count
USRCNT = 0
SELECTED = ""
SERVER = None

##################################

def clean(frame):
    global SELECTED
    SELECTED = ""
    for slave in frame.pack_slaves():
        slave.destroy()

def Stats(frame):
    global SELECTED
    if SELECTED != "Stats":
        clean(frame)
        SELECTED = "Stats"

def Users(frame):
    global SELECTED
    if SELECTED != "Users":
        clean(frame)
        SELECTED = "Users"

def Logs(frame):
    global SELECTED
    if SELECTED != "Logs":
        clean(frame)
        SELECTED = "Logs"

def Settings(frame):
    global SELECTED
    if SELECTED != "Settings":
        clean(frame)
        SELECTED = "Settings"
        server_start = Button(frame, text="start server", command=start_server)
        server_stop = Button(frame, text="stop server", command=stop_server)
        server_start.pack()
        server_stop.pack()

def start_server():
    global SERVER
    if SERVER is None:
        SERVER = Process(target=host, args=(("127.0.0.1", 57270),))
        # SERVER = subprocess.Popen(host, stdout=subprocess.PIPE, shell=True)
        print("Server Created...")
        SERVER.start()
        print("Server Started")

def stop_server():
    global SERVER
    if SERVER is not None:
        print("Stopping Server...")
        SERVER = SERVER.kill()
        print("Server Stopped")

def on_close(root):
    stop_server()
    root.destroy()

def NewConnection():
    pass

def CloseConnection():
    pass

def DEBUG(message):
    global DEBUG
    if DEBUG:
        print(message, file=sys.stderr)

def host(address, timeout=60):
    global USRCNT
    
    listSock = []
    DEBUG("pid: {}".format(os.getpid()))
    DEBUG("address[0]: {}, address[1]: {}, timeout: {}".format(address[0], address[1], timeout))
    
    # Create TCP/IP Socket
    socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_listen.setblocking(0)

    # Bind the socket to the port
    DEBUG("starting up on {} port {}".format(address[0], address[1]))
    socket_listen.bind(address)
    socket_listen.listen(10)
    
    listSock.append(socket_listen)

    while listSock:
        # Wait for at least one of the sockets to be ready for processing
        DEBUG("\nwaiting for the next event")
        readable, writable, exceptional = select.select(listSock, [], [], timeout)

        # Handle inputs
        for s in readable:
            # 이곳에 유저가 들어온 것을 처리
            if s is socket_listen:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                connection.setblocking(0)
                DEBUG("new connection from " + str(client_address))

                USRCNT += 1

                listSock.append(connection)

            else:
                try:
                    data = s.recv(1024)
                # 이곳에 유저가 나간 것을 처리
                except ConnectionResetError:
                    DEBUG("closing "+ str(client_address) +" ConnectionResetError...")
                    
                    # Stop listening for input on the connection
                    listSock.remove(s)
                    s.close()
                    
                    break

                if data:
                    # A readable client socket has data
                    DEBUG("{} : {}".format(str(s.getpeername()), data.decode('utf-8')))

                    ###
                    # parsed = packet.toPacket(data.decode('utf-8'))
                    # print(parsed['packetType'])
                    # print(parsed['timestamp'])

                else:
                    # Interpret empty result as closed connection
                    DEBUG("closing "+ str(client_address) +"after reading no data")
                    
                    # Stop listening for input on the connection
                    listSock.remove(s)
                    s.close()

# if __name__ == "__main__":
#     address = ("127.0.0.1", 57270)
#     timeout = 60

#     host(address, timeout)

if __name__ == "__main__":
    # MAIN
    # MainFrame initialization
    MAIN_PID = os.getpid()
    mainScreen = Tk()
    mainScreen.title("유저 관리")
    mainScreen.protocol("WM_DELETE_WINDOW", lambda:on_close(mainScreen))

    w = 1280 # width for the Tk mainScreen
    h = 720 # height for the Tk mainScreen

    # get screen width and height
    ws = mainScreen.winfo_screenwidth() # width of the screen
    hs = mainScreen.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk mainScreen window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    mainScreen.geometry('%dx%d+%d+%d' % (w, h, x, y))


    # MainFrame Multiplexing
    mainFrame = Frame(mainScreen)
    NaviFrame = Frame(mainFrame, background="BLACK")
    centerFrame = Frame(mainFrame, background="WHITE")
    
    mainFrame.pack(fill=BOTH, expand=True)
    NaviFrame.pack(fill=X, side=TOP)
    centerFrame.pack(fill=BOTH, expand=True)


    # Frame Updates
    nav_buttons = {}
    nav_buttons['cnt'] = 4
    nav_buttons['frame'] = NaviFrame
    nav_buttons['list'] = []
    nav_buttons['height'] = 3
    nav_buttons['width'] = 10
    nav_buttons['font'] = font.Font(size=20)
    nav_buttons['foreground']="white"
    nav_buttons['background']="black"
    nav_buttons['activeforeground']="white"
    nav_buttons['activebackground']="gray15"

    for i in range(nav_buttons['cnt']):
        nav_buttons['list'].append(Button(nav_buttons['frame']))
        nav_buttons['list'][i]['activebackground'] = "gray15"
        nav_buttons['list'][i]['activeforeground'] = "white"
        nav_buttons['list'][i]['background'] = "black"
        nav_buttons['list'][i]['foreground'] = "white"
        nav_buttons['list'][i]['width'] = nav_buttons['width']
        nav_buttons['list'][i]['height'] = nav_buttons['height']

        
    nav_buttons['list'][0]['text'] = "Stats"
    nav_buttons['list'][1]['text'] = "Users"
    nav_buttons['list'][2]['text'] = "Logs"
    nav_buttons['list'][3]['text'] = "Settings"

    for i in range(nav_buttons['cnt']-1):
        nav_buttons['list'][i].pack(side=LEFT)
    nav_buttons['list'][nav_buttons['cnt']-1].pack(side=RIGHT)

    nav_buttons['list'][0]['command'] = lambda:Stats(centerFrame)
    nav_buttons['list'][1]['command'] = lambda:Users(centerFrame)
    nav_buttons['list'][2]['command'] = lambda:Logs(centerFrame)
    nav_buttons['list'][3]['command'] = lambda:Settings(centerFrame)
        
    ####
    mainScreen.mainloop()