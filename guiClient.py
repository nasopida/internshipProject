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

suc = False

#아이디 설정 클래스
class setID:

    def __init__(self, window):
        # 창을 파괴하기 위한 myParent
        self.myParent = window
        # mainFrame은 창 전체를 뜻한다.
        self.mainFrame = Frame(window)
        window.title("로그인")
        window.geometry("250x140")
        self.mainFrame.pack(fill=X)

        # ID 프레임
        self.idFrame = Frame(self.mainFrame)
        self.idFrame.pack(expand=True,pady=5)
        self.idLabel = Label(self.idFrame,text="ID : ")
        self.idText = Entry(self.idFrame)
        self.idLabel.pack(side=LEFT, ipadx = 13)
        self.idText.pack(side=RIGHT, padx = 30)

        # 비밀번호 프레임
        self.passwdFrame = Frame(self.mainFrame)
        self.passwdFrame.pack()
        self.passwdLabel = Label(self.passwdFrame,text = "Password : ")
        self.passwdText = Entry(self.passwdFrame)
        self.passwdLabel.pack(side=LEFT)
        self.passwdText.pack(side=RIGHT, padx=10)
        
        self.loginButton = Button(window,text="로그인", command=self.signInBtn)
        #엔터키랑 연동
        #window.bind('<Return>',self.enterBtn)
        self.loginButton.pack(pady=10)

        #회원가입
        self.signUpButton = Button(window,text="회원가입", command=self.signUpBtn)
        self.signUpButton.pack(pady=10)
    # 회원가입 버튼
    def signUpBtn(self):
        signUpRoot = Tk()
        mySignUp = SignUp(signUpRoot)
        signUpRoot.mainloop()

    # 로그인 버튼
    def signInBtn(self):
        global suc
        if os.path.isfile("login.config"):
            loginFile = open('login.config', mode='rt', encoding='utf-8')
            lines = loginFile.readlines()
            #print((self.idText.get()+'\n' == lines[0]))
            #print((self.passwdText.get()+'\n' == lines[1]))
            # 저장될 때 개행문자가 들어가서 +'\n'추가하여 비교하였음
            if (self.idText.get()+'\n' == lines[0]) and (self.passwdText.get()+'\n' == lines[1]):
                suc = True
                self.myParent.destroy()
            else:
                suc = False
                failRoot = Tk()
                failWindow = loginFail(failRoot)
                failRoot.mainloop()
                
        else:
            suc = False
            failRoot = Tk()
            failWindow = loginFail(failRoot)
            failRoot.mainloop()

# 로그인 실패 창
class loginFail:
    def __init__(self, window):
        #창 파괴를 위한 변수
        self.myParent = window

        # mainFrame
        self.mainFrame = Frame(window)
        window.title("로그인 실패!")
        window.geometry("200x80")
        self.mainFrame.pack()

        # 로그인 실패를 출력
        self.failLabel = Label(self.mainFrame, text="로그인 실패!")
        self.failLabel.pack(fill=BOTH, padx=30, pady=10)

        # 종료 버튼
        self.endButton = Button(self.mainFrame, text="확인", command=self.endBtn)
        self.endButton.pack(pady=5)
    def endBtn(self):
        self.myParent.destroy()

# 회원가입을 진행하는 클래스
class SignUp:
    def __init__(self, window):
        #나중에 창을 파괴하기 위해
        self.myParent = window

        #mainFrame은 창 전체이다.
        self.mainFrame = Frame(window)
        window.title("회원 가입")
        window.geometry("250x140")
        self.mainFrame.pack()

        # ID를 입력하는 라벨
        self.idFrame = Frame(self.mainFrame)
        self.idFrame.pack(expand=True, pady=5)
        self.idLabel = Label(self.idFrame,text="ID : ")
        self.idText = Entry(self.idFrame)
        self.idLabel.pack(side=LEFT, ipadx = 13)
        self.idText.pack(side=RIGHT, padx = 30)

        # 비밀번호를 입력하는 라벨
        self.passwdFrame = Frame(self.mainFrame)
        self.passwdFrame.pack(pady = 5)
        self.passwdLabel = Label(self.passwdFrame,text = "Password : ")
        self.passwdText = Entry(self.passwdFrame)
        self.passwdLabel.pack(side=LEFT)
        self.passwdText.pack(side=RIGHT, padx=10)

        # 닉네임을 입력하는 라벨
        self.nicknameFrame = Frame(self.mainFrame)
        self.nicknameFrame.pack(pady = 5)
        self.nicknameLabel = Label(self.nicknameFrame, text="Nickname : ")
        self.nicknameText = Entry(self.nicknameFrame)
        self.nicknameLabel.pack(side=LEFT)
        self.nicknameText.pack(side=RIGHT, padx=10)

        # 가입 요청을 하는 버튼
        self.requestButton = Button(self.mainFrame, text="가입 요청",command=self.requestBtn)
        self.requestButton.pack(pady = 10)
    
    # 가입 요청을 하는 버튼
    def requestBtn(self):
        if (len(self.idText.get())!= 0) and (len(self.passwdText.get()) != 0) and (len(self.nicknameText.get()) != 0):
            f = open('login.config','w+t',encoding='utf-8')
            f.write(self.idText.get()+'\n')
            f.write(self.passwdText.get()+'\n')
            f.write(self.nicknameText.get())
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

        #채팅을 입력하는 Frame인 inputChatFrame
        self.inputChatFrame = Frame(self.mainFrame)
        self.inputChatFrame.pack(fill=X)
        self.alertLabel = Label(self.inputChatFrame,text="채팅 입력")
        self.alertLabel.pack(fill=X)
        #채팅창 입력
        self.inputText = Text(self.inputChatFrame)
        self.inputText.config(width = 45, height=15, state="disabled", yscrollcommand=self.scroll.set)
        self.inputText.pack(side=LEFT)
        self.inputBtn = Button(self.inputChatFrame, text="send", width=15, height=15, command=self.sendMessage)
        self.inputBtn.pack(side=LEFT)

    def sendMessage(self):
        print("hi")



if __name__ == '__main__':
    # 아이디 입력 창
    """
    if os.path.isfile("login.txt"):
        pass
    else:
        """
    idRoot = Tk()
    myId = setID(idRoot)
    idRoot.mainloop()  
    if suc == True:
        if os.path.isfile("login.config"):
            loginFile = open('login.config',mode='rt',encoding='utf-8')
            lines = loginFile.readlines()
            user = lines[2]
    else:
        sys.exit()

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