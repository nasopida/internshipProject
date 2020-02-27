import socket
import argparse
import threading
import random
import os
from tkinter import *
from tkinter import ttk
import tkinter
import userList
import sys
import translate


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 로그인 관련
import login

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
    def __init__(self, window, client_socket):
        # 나중에 창을 파괴하기 위해
        self.myParent = window
        self.client_socket = client_socket
        self.centerWindow(window)

        #창 x버튼으로 끌때를 위해
        def close():
            self.myParent.destroy()
            self.client_socket.close()
        self.myParent.protocol('WM_DELETE_WINDOW', close)

        #mainFrame은 창 전체를 뜻함
        self.mainFrame = Frame(window)
        window.title("채팅방")
        #window.geometry("400x600")
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

        # 번역 기능 프레임인 translateFrame
        self.translateFrame = Frame(self.mainFrame)
        self.translateFrame.pack(fill=X)
        #self.translateLabel = Label(self.translateFrame,text="번역 : ", foreground="orange")
        #self.translateLabel.pack(side=LEFT)

        # 체크박스
        self.translate_check = BooleanVar()
        lang_change = Checkbutton(self.translateFrame, text="번역하기  ", variable=self.translate_check)
        lang_change.deselect()
        lang_change.pack(side=LEFT)

        # 원래 언어
        self.lang_original = ttk.Combobox(self.translateFrame,width=12)
        self.lang_original['values'] = ('영어','한국어','일본어')
        self.lang_original.current(0)
        self.lang_original.configure(state='readonly')
        self.lang_original.pack(side=LEFT)

        self.translateLabel = Label(self.translateFrame,text="  ->  ")
        self.translateLabel.pack(side=LEFT)

        # 번역할 언어
        self.lang_translate = ttk.Combobox(self.translateFrame,width=12)
        self.lang_translate['values'] = ('영어','한국어','일본어')
        self.lang_translate.current(1)
        self.lang_translate.configure(state='readonly')
        self.lang_translate.pack(side=LEFT)       

        #채팅을 입력하는 Frame인 inputChatFrame
        self.inputChatFrame = Frame(self.mainFrame)
        self.inputChatFrame.pack(fill=X)
        self.alertLabel = Label(self.inputChatFrame,text="채팅 입력")
        self.alertLabel.pack(fill=X)
        #채팅창 입력
        #self.inputText = Entry(self.inputChatFrame)
        self.inputText = Text(self.inputChatFrame)
        self.inputText.config(width = 45, height=15, yscrollcommand=self.scroll.set)
        self.inputText.mark_set(INSERT,'1.0')
        self.inputText.focus_set()
        self.inputText.pack(side=LEFT)
        #self.inputText.icursor(0)
        
        self.inputBtn = Button(self.inputChatFrame, text="send", width=15, height=15, command=self.sendMessage)
        self.inputBtn.pack(side=LEFT)

        window.bind('<Return>',self.sendMessage)

        receive_thread = threading.Thread(target=client.handle_receive, args=(self.client_socket, user, self))
        receive_thread.daemon = True
        receive_thread.start()
        
        #유저 리스트를 새로 띄워주는 창
        # -> 유저가 추가될 때 마다 기존 유저에게도 추가를 해 주어야함
        userListRoot = Toplevel(self.myParent)
        self.users = userList.UserList(userListRoot)
        def all_user():
            for name in client.user_list:
                #print(name)
                if name not in self.users.user_list:
                    self.users.addUser(name)
            userListRoot.after(500,all_user)

        userListRoot.resizable(0,0)
        userListRoot.after(500,all_user)
        
        def server_receive():
            for data in client.server_chat:
                self.logText.config(width=60,height=35,state="normal",yscrollcommand=self.scroll.set)
                self.logText.insert(END, data)
                self.logText.insert(END, '\n')
                self.logText.see('end')
                self.logText.config(width=60,height=35,state="disable",yscrollcommand=self.scroll.set)
            client.server_chat = {}
            userListRoot.after(500, server_receive)
        userListRoot.after(500, server_receive)
        userListRoot.mainloop()
        receive_thread.join()

        self.inputText.focus_set()
        

    def search(self):
        search = Toplevel(self.myParent)
        frame = Frame(search)
        search.title("검색")
        search.geometry("200x50")
        word = Text(search)
        word.config(width = 20, height = 1)
        word.pack()
        def file_search(event):
            f = open('../log/logFile.bin', mode='rb')
            findtxt = []
            #read = f.read()
            
            data = word.get('1.0',INSERT)
            findtxt.append(data.strip())
            i = (len(findtxt)-1)
            print("@"*50)
            print("검색 키워드:"+findtxt[i])
            print("@"*50)
            for content in f.readlines():
                if content.find(findtxt[i].encode('utf-8')) != -1:
                    print(data)
        button = Button(search, text="검색")
        button.bind('<Button-1>', file_search)
        button.pack()
        search.resizable(0,0)

    def sendMessage(self, event = None):
        if self.translate_check.get() == 1:
            mydata = translate.translate(self.inputText.get('1.0',INSERT),self.lang_original.get(),self.lang_translate.get())
            #mydata = translate.translate(mydata,self.lang_original.get(),self.lang_translate.get())
        else:
            mydata = self.inputText.get('1.0',INSERT)
        #print(data)
        data = mydata.replace('\n','')
        print(data)
        if len(data) > 0:
            self.logText.config(width=60,height=35,state="normal",yscrollcommand=self.scroll.set)

            if data not in client.command_list:
                self.logText.insert(END, '%s:'%user)
            self.logText.insert(END,'%s\n'%data)
            """#간단한 명령어기능
            if data == "/quit":
                clnt_logger.addLog(msgLog("program", data))
                self.myParent.destroy()
                #self.myParent.quit()
                self.client_socket.close()
                return
            if data == "/whoami":
                self.logText.insert(END,data)
                self.logText.insert(END,'\n')
                self.logText.insert(END,user+"입니다")
                self.logText.insert(END, '\n')
            if data == "/whattime":
                now=datetime.now()
                self.logText.insert(END,data)
                self.logText.insert(END,'\n')
                self.logText.insert(END,"%s시 %s분 %s초입니다."%(now.hour,now.minute,now.second))
                self.logText.insert(END, '\n')
            if data == "/whatdate":
                now=datetime.now()
                self.logText.insert(END,data)
                self.logText.insert(END,'\n')
                self.logText.insert(END,"%s년 %s월 %s일입니다."%(now.year,now.month,now.day))
                self.logText.insert(END, '\n')
            if data == "/dice":
                randString = client.dice()
                self.logText.insert(END,data)
                self.logText.insert(END,'\n')
                self.logText.insert(END,randString)
                self.logText.insert(END, '\n')
            # clnt_logger.addLog(msgLog("program", data))
            # clnt_logger.record()
            if data == "/user":
                print('[')
                for name in client.user_list:
                    self.logText.insert(END, "%s\n"%name)
            
            #검색기능
            if data=="/search":
                #split = read.split()
                #self.logText.insert(END,"찾을 채팅내용을 입력하십쇼: ", end='')
                #find=input()
                self.search()
            """            
      
            self.logText.config(width=60,height=35,state="disabled",yscrollcommand=self.scroll.set)
            self.logText.see("end")
            self.inputText.delete('1.0', END)
            client.handle_send(self.client_socket, user, data)
    
    def centerWindow(self, window):
        width = 400
        height = 600
        #userScreen = window.winfo_
        #screen_width = userScreen.GetSystemMetrics(0)
        #screen_height = userScreen.GetSystemMetrics(1)
        screen_width = self.myParent.winfo_screenwidth()
        screen_height = self.myParent.winfo_screenheight()
        x = screen_width/2 - width/2
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))


if __name__ == '__main__':
    # 아이디 입력 창
    """
    if os.path.isfile("login.txt"):
        pass
    else:
        """
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 host와 prot를 통해 서버에 접속합니다.
    client_socket.connect((host, port))

    idRoot = Tk()
    myId = login.Login(idRoot, client_socket)
    idRoot.resizable(0,0)
    idRoot.mainloop()
    #print(successCheck)
    #if successCheck == True:
    if login.Login.loginSuccess(myId) == True:
        if os.path.isfile("login.config"):
            loginFile = open('login.config',mode='rt',encoding='utf-8')
            lines = loginFile.readlines()
            #lines[2].splitlines()
            myUser = login.Login.returnID(myId)
            #user.rstrip('\n')
            #self.client_socket.send(loginPacket(self.idText.get(),self.passwdText.get()))
    else:
        sys.exit()

    print(myUser)
    user = myUser.rstrip('\n')
    
    # 채팅 창
    chatRoot = Tk()
    myChat = Chatting(chatRoot, client_socket)
    #chatRoot.resizable(0,0)
    #chatRoot.mainloop()
    
    clnt_logger = msgLogger()
    clnt_logger.setFile(user+"LogFile.txt")
    clnt_logger.read()

    #send_thread = threading.Thread(target=client.handle_send, args=(client_socket, user))
    #send_thread.daemon = True
    #send_thread.start()

    #send_thread.join()
