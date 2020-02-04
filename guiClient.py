import socket
import argparse
import threading
import random
import os
from tkinter import *

# 로그인 관련
import setID

import client
from datetime import datetime
from logger import msgLog, msgLogger

port = 57270
host = "127.0.0.1"
clnt_logger = msgLogger()
clnt_logger.setFile("./log/clientLogFile.txt")
clnt_logger.read()

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
        self.nameLabel = Label(self.nameLabelFrame,text="접속자 : " + user.rstrip('\n'))
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

        #채팅을 입력하는 Frame인 inputChatFrame
        self.inputChatFrame = Frame(self.mainFrame)
        self.inputChatFrame.pack(fill=X)
        self.alertLabel = Label(self.inputChatFrame,text="채팅 입력")
        self.alertLabel.pack(fill=X)
        #채팅창 입력
        self.inputText = Text(self.inputChatFrame)
        self.inputText.config(width = 45, height=15, yscrollcommand=self.scroll.set)
        self.inputText.pack(side=LEFT)
        self.inputBtn = Button(self.inputChatFrame, text="send", width=15, height=15, command=self.sendMessage)
        self.inputBtn.pack(side=LEFT)
        #self.myParent.bind('<Return>',self.sendMessage)

    def sendMessage(self, event = None):
        data = self.inputText.get('1.0', END)
        print(data)
        if data=='a':
            print(1)
        #간단한 명령어기능
        if data == "/quit":
            clnt_logger.addLog(msgLog("program", data))
        if data == "/whoami":
            print(user+"입니다")
        if data == "/whattime":
            now=datetime.now()
            print("%s시 %s분 %s초입니다."%(now.hour,now.minute,now.second))
        if data == "/whatdate":
            now=datetime.now()
            print("%s년 %s월 %s일입니다."%(now.year,now.month,now.day))
        if data == "/dice":
            randString = client.dice()
            print(randString)
        # clnt_logger.addLog(msgLog("program", data))
        # clnt_logger.record()
        
        #print(data)
        if len(data) > 0:
            self.logText.config(width=60,height=35,state="normal",yscrollcommand=self.scroll.set)
            if data!="/quit" and data!="/whoami" and data!="/whattime" and data!="/whatdate" and data!="/dice":
                self.logText.insert(END, '[%s]: '%user)
            self.logText.insert(END, data)
            self.logText.insert(END, '\n')
            #간단한 명령어기능
            if data == "/quit":
                clnt_logger.addLog(msgLog("program", data))
            if data == "/whoami":
                self.logText.insert(END,user+"입니다")
            if data == "/whattime":
                now=datetime.now()
                self.logText.insert(END,"%s시 %s분 %s초입니다."%(now.hour,now.minute,now.second))
            if data == "/whatdate":
                now=datetime.now()
                self.logText.insert(END,"%s년 %s월 %s일입니다."%(now.year,now.month,now.day))
            if data == "/dice":
                randString = client.dice()
                self.logText.insert(END,randString)
            # clnt_logger.addLog(msgLog("program", data))
            # clnt_logger.record()
            
            """#검색기능
            if data=="/search":
                f = open('chatLog.txt', mode='r', encoding='utf-8')
                read = f.read()
                split = read.split(';')
                self.logText.insert(END,"찾을 채팅내용을 입력하십쇼: ", end='')
                find=input()
                line=1
                for i in split:
                    if i == find:
                        self.logText.insert(END,'%d.%s'%(line,i))
                    else:
                        pass
                    line=line+1
                    """

      
            self.logText.config(width=60,height=35,state="disabled",yscrollcommand=self.scroll.set)
            self.logText.see("end")
            self.inputText.delete('1.0', END)

if __name__ == '__main__':
    # 아이디 입력 창
    """
    if os.path.isfile("login.txt"):
        pass
    else:
        """
    idRoot = Tk()
    myId = setID.SetID(idRoot)
    idRoot.mainloop() 
    #print(successCheck)
    #if successCheck == True:
    if setID.SetID.successCheck(myId) == True:
        if os.path.isfile("login.config"):
            loginFile = open('login.config',mode='rt',encoding='utf-8')
            lines = loginFile.readlines()
            #lines[2].splitlines()
            user = setID.SetID.returnNickname(myId)
            #user.rstrip('\n')
    else:
        sys.exit()

    print(user)

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
