import socket
import argparse
import threading
import random
import os
from tkinter import *


import client
from datetime import datetime
from logger import msgLog, packetLogger

port = 57270
host = "127.0.0.1"
clnt_logger = packetLogger()
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
        if len(self.text.get())!=0:
            f = open('name.txt','w', encoding='utf-8')
            f.write(self.text.get())
            f.close()
            self.myParent.destroy()


# 채팅을 관리하는 클래스
class Chatting:
    def __init__(self, window):
        # 나중에 창을 파괴하기 위해
        self.myParent = window
        
        #mainFrame은 창 전체를 뜻함
        self.mainFrame = Frame(window)
        window.title("채팅방")
        window.geometry("400x600")
        self.mainFrame.pack(fill=X)

        #접속한 사람의 이름을 띄워주는 라벨
        self.nameLabelFrame = Frame(self.mainFrame)
        self.nameLabelFrame.pack(fill = X)
        self.nameLabel = Label(self.nameLabelFrame,text="접속자 : " + user)
        self.nameLabel.pack(fill=X)

        #채팅 내용을 담는 Frame은 chatLogFrame
        self.chatLogFrame = Frame(self.mainFrame)
        self.chatLogFrame.pack(fill=X)
        #logText는 채팅방 로그 (채팅창)
        self.logText = Text(self.chatLogFrame)
        self.scroll = Scrollbar(self.chatLogFrame)
        self.scroll.pack(side=RIGHT, fill=Y)
        self.logText.config(width=60,height=35,state="disabled",yscrollcommand=self.scroll.set)
        self.logText.pack(side=LEFT, fill=BOTH, expand=YES)
        self.scroll.config(command=self.logText.yview)
        #client.handle_receive(client_socket,user)

        #채팅을 입력하는 Frame인 inputChatFrame
        self.inputChatFrame = Frame(self.mainFrame)
        self.inputChatFrame.pack(fill=X)
        self.alertLabel = Label(self.inputChatFrame,text="채팅 입력")
        self.alertLabel.pack(fill=X)
        #채팅창 입력
        #self.inputText = Text(self.inputChatFrame)
        #self.inputText=Entry(self.inputChatFrame)
        self.inputText.config(width = 45, height=15, state="disabled", yscrollcommand=self.scroll.set)
        self.inputText.pack(side=LEFT)
        self.inputBtn = Button(self.inputChatFrame, text="send", width=15, height=15, command=self.sendAndShowMessage)
        self.inputBtn.pack(side=LEFT)

    def sendAndShowMessage(self):
        #print('hi')
        #client.handle_receive(client_socket,user)
        global index=0
        self.logText.insert(index,'hi')
        index=index+1
    
    #def showMessage(self):




if __name__ == '__main__':
    # 아이디 입력 창
    if os.path.isfile("name.txt"):
        pass
    else:
        idRoot = Tk()
        myId = setID(idRoot)
        idRoot.mainloop()  
    
    nameFile = open('name.txt',mode='rt',encoding='utf-8')
    user = nameFile.read()

    # 채팅 창
    chatRoot = Tk()
    myChat = Chatting(chatRoot)
    chatRoot.mainloop()

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

