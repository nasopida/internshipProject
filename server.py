#-*-coding: utf-8

import select
import socket
import os
import sys
import queue
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
from multiprocessing import Process
import queue
from datetime import datetime
import random

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import packet

##################################
# Debug opt
DEBUG = True

# Client Dict
Clients = {}
Clients['AllOnlineClients'] = []
Clients['msg_queues'] = {}
Clients['USERCNT'] = 0


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
        server_start['bg'] = '#424242'
        server_start['fg'] = '#ffffff'
        server_stop['bg'] = '#424242'
        server_stop['fg'] = '#ffffff'
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

def DEBUG(message):
    global DEBUG
    if DEBUG:
        print(message, file=sys.stderr)

def host(address, timeout=60):
    global Clients
    
    LoginList = []
    readSockList = []
    DEBUG("pid: {}".format(os.getpid()))
    DEBUG("address[0]: {}, address[1]: {}, timeout: {}".format(address[0], address[1], timeout))
    
    # Create TCP/IP Socket
    socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_listen.setblocking(0)

    # Bind the socket to the port
    DEBUG("starting up on {} port {}".format(address[0], address[1]))
    socket_listen.bind(address)
    socket_listen.listen(10)
    
    readSockList.append(socket_listen)

    while readSockList:
        # Wait for at least one of the sockets to be ready for processing
        DEBUG("\nwaiting for the next event")
        readable, writable, exceptional = select.select(readSockList, [], readSockList, timeout)

        # Handle "exceptional conditions"
        for s in exceptional:
            DEBUG("handling exceptional condition for" + s.getpeername())
            # Stop listening for input on the connection
            readSockList.remove(s)
            s.close()

        # Handle inputs
        DEBUG("\nHandle inputs------")
        for s in readable:
            # 이곳에 유저가 들어온 것을 처리
            if s is socket_listen:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                connection.setblocking(0)
                DEBUG("new connection from " + str(client_address))
                readSockList.append(connection)

            else:
                try:
                    data = s.recv(1024)
                # 이곳에 유저가 나간 것을 처리
                except ConnectionResetError:
                    DEBUG("closing "+ str(client_address) +" ConnectionResetError...")
                    
                    # Stop listening for input on the connection
                    if s in Clients:
                        Clients['AllOnlineClients'].remove(s)
                        del Clients['msg_queues'][s]
                        del Clients[s]
                        Clients['USERCNT'] -= 1
                    readSockList.remove(s)
                    if s in writable:
                        writable.remove(s)
                    s.close()
                    
                    break

                if data:
                    # A readable client socket has data
                    DEBUG("{} : {}".format(str(s.getpeername()), data.decode('utf-8')))

                    try:
                        parsed = packet.toPacket(data.decode('utf-8'))
                    except Exception as err:
                        DEBUG("Exception: {}".format(err))
                        print("NOT PACKET!!! -- client err")
                        continue

                    # DEBUG(parsed)

                    if parsed.packet['packetType'] == "message":
                        # 현재 소켓을 제외한 소켓으로 메세지 보내야함
                        for client in Clients['AllOnlineClients']:
                            if client != s:
                                parsed.add({'userID':Clients[s]})
                                Clients['msg_queues'][client].put(parsed)
                                writable.append(client)

                    elif parsed.packet['packetType'] == "command":
                        # 현재 소켓에 command를 실행한 결과를 보냄
                        return_msg = packet.msgPacket("")
                        return_msg.add({'userID': None})
                        
                        if parsed.packet['text'] == "whoami":
                            return_msg.add({'text': Clients[s] + "입니다."})

                        elif parsed.packet['text'] == "whattime":
                            now=datetime.now()
                            return_msg.add({'text': "{}시 {}분 {}초입니다.".format(now.hour,now.minute,now.second)})

                        elif parsed.packet['text'] == "whatdate":
                            now=datetime.now()
                            return_msg.add({'text': "{}년 {}월 {}일입니다.".format(now.year,now.month,now.day)})

                        elif parsed.packet['text'] == "dice":
                            return_msg.add({'text':str(random.randint(1,6))})
                            
                        elif parsed.packet['text'] == "user":
                            names = []
                            msg = ""
                            for s in Clients['AllOnlineClients']:
                                names.append(Clients[s])
                            
                            msg += str(names)
                            return_msg.add({'text': msg})

                        #검색기능
                        elif parsed.packet['text']=="search":   
                            return_msg.add({'text': "search"})

                        else :
                            return_msg.add({'text': "No Command Found."})
                        
                        Clients['msg_queues'][s].put(return_msg)
                        writable.append(s)

                    elif parsed.packet['packetType'] == "login":
                        # 함수로 만들어야함
                        # login.config에 등록된 유저 확인.
                        # 등록된 유저라면 
                        DEBUG("login")
                        Clients['AllOnlineClients'].append(s)
                        Clients['msg_queues'][s] = queue.Queue()
                        Clients[s] = parsed.packet['userID']
                        Clients['USERCNT'] += 1

                    elif parsed.packet['packetType'] == "alter":
                        # 함수로 만들어야함
                        pass
                
                    elif parsed.packet['packetType'] == "register":
                        # 함수로 만들어야함
                        # login.config에 유저 추가
                        pass
                    
                    else:
                        print("NOT REGISTERED PACKET!!! -- client err")
                        pass

                else:
                    # Interpret empty result as closed connection
                    DEBUG("closing "+ str(client_address) +"after reading no data")
                    
                    # Stop listening for input on the connection
                    if s in Clients:
                        Clients['AllOnlineClients'].remove(s)
                        del Clients['msg_queues'][s]
                        del Clients[s]
                        Clients['USERCNT'] -= 1
                    readSockList.remove(s)
                    if s in writable:
                        writable.remove(s)
                    s.close()
        
        # Handle outputs
        DEBUG("\nHandle outputs------")
        for s in writable:
            try:
                next_msg = Clients['msg_queues'][s].get_nowait()
            # msg = "message from server"
            except queue.Empty:
                # No messages waiting so stop checking for writability.
                DEBUG("output queue for "+Clients[s]+" is empty")
            else:
                DEBUG("writing message to "+ Clients[s])
                # if next_msg.packet['userID'] is None:
                    # DEBUG("message : {" +"\"packetType\": \"message\", \"timestamp\":"+str(next_msg.packet['timestamp'])+", \"text\": \""+ str(next_msg.packet['text'].decode('utf-8')) + "\"}\n")
                # else :
                DEBUG("message :" + str(next_msg) + "\n")
                s.send(next_msg.encode())
        
        DEBUG("\nDEBUG------")
        DEBUG("Users_num: "+str(Clients['USERCNT']))
        print("Users: ", end='', file=sys.stderr)
        for s in Clients['AllOnlineClients']:
            print(Clients[s], end=', ', file=sys.stderr)

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
    nav_buttons['background']="#1E1E1E"
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
        
    # 백그라운드 색상
    centerFrame.configure(background='#242424')

    Settings(centerFrame)
    mainScreen.mainloop()