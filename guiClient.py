import socket
import argparse
import threading
import random
import os
from tkinter import *


import client
from datetime import datetime
from logger import msgLog, msgLogger

port = 57270
host = "127.0.0.1"
clnt_logger = msgLogger()
clnt_logger.setFile("clientLogFile.txt")
clnt_logger.read()

#아이디 설정 클래스
class setID:

    def __init__(self, window):
        self.myParent = window
        self.idFrame = Frame(window)
        window.title("이름 설정")
        window.geometry("250x100")
        self.label = Label(window,text="이름 입력")
        self.text = Entry(window)
        self.button = Button(window,text="확인", command=self.enterBtn)
        #엔터키랑 연동
        #window.bind('<Return>',self.enterBtn)
        
        self.label.pack()
        self.text.pack()
        self.button.pack()

    def enterBtn(self):
        f = open('name.txt','w', encoding='utf-8')
        f.write(self.text.get())
        f.close()
        self.myParent.destroy()


# 채팅을 관리하는 클래스
class Chatting:
    def __init__(self):
        pass

if __name__ == '__main__':
    """
    parser = argparse.ArgumentParser(description="\nclient\n-p port\n-i host\n-s string")
    parser.add_argument('-p', help="port")
    parser.add_argument('-i', help="host")
    parser.add_argument('-u', help="user", required=True)

    args = parser.parse_args()
    
    user = str(args.u)
    try:
        port = int(args.p)
        host = args.i
    except:
        pass
    """
    if os.path.isfile("name.txt"):
        pass
    else:
        root = Tk()
        myId = setID(root)
        root.mainloop()
        
    
    nameFile = open('name.txt',mode='rt',encoding='utf-8')
    user = nameFile.read()

    #아이디 입력 창
    """
    clnt_logger = msgLogger()
    clnt_logger.setFile(user+"LogFile.txt")
    clnt_logger.read()
    """

    #IPv4 체계, TCP 타입 소켓 객체를 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 host와 prot를 통해 서버에 접속합니다.
    client_socket.connect((host, port))

    client_socket.send(user.encode('utf-8'))

    receive_thread = threading.Thread(target=client.handle_receive, args=(client_socket, user))
    receive_thread.daemon = True
    receive_thread.start()

    send_thread = threading.Thread(target=client.handle_send, args=(client_socket, user))
    send_thread.daemon = True
    send_thread.start()

    receive_thread.join()
    send_thread.join()

