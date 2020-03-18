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
import titleBar
import search

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# 로그인 관련
import login
import client
from datetime import datetime
from logger import packetLogger

import packet

port = 57270
host = "127.0.0.1"
clnt_logger = packetLogger()
#clnt_logger.setFile("./log/clientLogFile.txt")
#clnt_logger.read()

# 채팅을 관리하는 클래스
class Chatting:
    def __init__(self, window, client_socket, user):
        # 나중에 창을 파괴하기 위해
        self.myParent = window
        self.client_socket = client_socket
        self.centerWindow(window, 400, 600)
        self.darkModeOn = False
        self.user = user
        
        #창 x버튼으로 끌때를 위해
        def close():
            self.myParent.destroy()
            self.client_socket.close()
        self.myParent.protocol('WM_DELETE_WINDOW', close)

        # 타이틀바
        window.title("채팅방")
        
        self.myParent.iconbitmap("./Icon/chat.ico")
        #self.titlebar = titleBar.TitleBarChat(self.myParent, self.client_socket)

        #mainFrame은 창 전체를 뜻함
        self.mainFrame = Frame(window)
        
        #window.geometry("400x600")
        self.mainFrame.pack(fill=X)

        #접속한 사람의 이름을 띄워주는 라벨
        self.nameLabelFrame = Frame(self.mainFrame)
        self.nameLabelFrame.pack(fill = X)
        self.nameLabel = Label(self.nameLabelFrame,text="접속자 : " + user)
        self.nameLabel.pack(side=LEFT)

        #로그아웃 버튼
        self.signOutButton = Button(self.nameLabelFrame, text="Sign Out", command=lambda:self.signOut())
        self.signOutButton.pack(side=RIGHT)

        # 검색 버튼
        self.searchButton = Button(self.nameLabelFrame,text="search", command=self.search)
        self.searchButton.pack(side=RIGHT)
        self.searchWindow = 0

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
        self.lang_change = Checkbutton(self.translateFrame, text="Translate  ", variable=self.translate_check)
        self.lang_change.deselect()
        self.lang_change.pack(side=LEFT)

        # 원래 언어
        self.lang_original = ttk.Combobox(self.translateFrame,width=12)
        self.lang_original['values'] = ('English','한국어','日本語')
        self.lang_original.current(0)
        self.lang_original.configure(state='readonly')
        self.lang_original.pack(side=LEFT)

        self.translateLabel = Label(self.translateFrame,text="  ->  ")
        self.translateLabel.pack(side=LEFT)

        # 번역할 언어
        self.lang_translate = ttk.Combobox(self.translateFrame,width=12)
        self.lang_translate['values'] = ('English','한국어','日本語')
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

        self.inputText.focus_set()
        #유저 리스트를 새로 띄워주는 창
        # -> 유저가 추가될 때 마다 기존 유저에게도 추가를 해 주어야함
        userListRoot = Toplevel(self.myParent)
        self.users = userList.UserList(userListRoot, self)
        def all_user():  
            for name in client.user_list:
                if name not in self.users.user_list:
                    self.users.addUser(name)
            delete_list = []
            for name in self.users.user_list:
                if name not in client.user_list:
                    delete_list.append(name)
            for delete in delete_list:
                self.users.deleteUser(delete)
                self.users.deleteAll()
                for username in self.users.user_list:
                    self.users.addUser(username)
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
        #userListRoot.resizable(0,0)
        receive_thread.join()
    def searchWindowON(self):
        searchWindow = 1

    def searchWindowOFF(self):
        searchWindow = 0

    def delete_highlighting(self):
        self.logText.tag_delete('search')

    def highlighting(self, line, start, end):
        self.logText.see('%d.%d'%(line, start))
        self.logText.config(state = 'normal')
        self.logText.mark_set("matchStart", '%d.%d'%(line,start))
        self.logText.mark_set("matchEnd", '%d.%d'%(line,end))
        self.logText.tag_add('search', "matchStart", "matchEnd")
        self.logText.tag_config('search', background="yellow")
        self.logText.config(state = 'disable')

    def get_searchData(self):
        return self.logText.get('1.0', END)
    
    def search(self):
        if self.searchWindow == 0:
            search.search(self)
            
    def darkMode(self):
        if self.darkModeOn == False:
            self.darkModeOn = True
            self.myParent.configure(background='#242424')
            self.mainFrame.configure(background='#242424')
            
            # 이름 출력 라벨
            self.nameLabelFrame.configure(background='#242424')
            self.nameLabel['bg'] = '#242424'
            self.nameLabel['fg'] = '#ffffff'
            self.searchButton['bg'] = '#424242'
            self.searchButton['fg'] = '#ffffff'
            self.signOutButton['bg'] = "#424242"
            self.signOutButton['fg'] = "#ffffff"
            
            # 채팅 기록
            self.logText['bg'] = '#242424'
            self.logText['fg'] = '#ffffff'
            self.scroll.configure(background='#242424')
            
            # 번역기
            self.translateFrame.configure(background='#242424')
            self.translateLabel['bg'] = '#242424'
            self.translateLabel['fg'] = '#ffffff'
            self.lang_change['bg'] = '#242424'
            self.lang_change['fg'] = '#ffffff'
            self.lang_change['selectcolor'] = '#424242'

            # 채팅 입력창
            self.alertLabel['bg'] = '#242424'
            self.alertLabel['fg'] = '#ffffff'
            self.inputText['bg'] = '#242424'
            self.inputText['fg'] = '#ffffff'
            self.inputBtn['bg'] = '#424242'
            self.inputBtn['fg'] = '#ffffff'
            # 검색 버튼 내부
        else:
            self.darkModeOn = False
            self.myParent.configure(background='#f0f0f0')
            self.mainFrame.configure(background='#f0f0f0')
            
            # 이름 출력 라벨
            self.nameLabelFrame.configure(background='#f0f0f0')
            self.nameLabel['bg'] = '#f0f0f0'
            self.nameLabel['fg'] = '#000000'
            self.searchButton['bg'] = '#f0f0f0'
            self.searchButton['fg'] = '#000000'
            self.signOutButton['bg'] = "#f0f0f0"
            self.signOutButton['fg'] = "#000000"
            
            # 채팅 기록
            self.logText['bg'] = '#ffffff'
            self.logText['fg'] = '#000000'
            self.scroll.configure(background='#f0f0f0')
            
            # 번역기
            self.translateFrame.configure(background='#f0f0f0')
            self.translateLabel['bg'] = '#f0f0f0'
            self.translateLabel['fg'] = '#000000'
            self.lang_change['bg'] = '#f0f0f0'
            self.lang_change['fg'] = '#000000'
            self.lang_change['selectcolor'] = '#ffffff'

            # 채팅 입력창
            self.alertLabel['bg'] = '#f0f0f0'
            self.alertLabel['fg'] = '#000000'
            self.inputText['bg'] = '#ffffff'
            self.inputText['fg'] = '#000000'
            self.inputBtn['bg'] = '#f0f0f0'
            self.inputBtn['fg'] = '#000000'

    def sendMessage(self, event = None):
        if self.translate_check.get() == 1:
            mydata = translate.translate(self.inputText.get('1.0',INSERT),self.lang_original.get(),self.lang_translate.get())
            #mydata = translate.translate(mydata,self.lang_original.get(),self.lang_translate.get())
        else:
            mydata = self.inputText.get('1.0',INSERT)
        data = mydata.replace('\n','')
        if len(data) > 0:
            self.logText.config(width=60,height=35,state="normal",yscrollcommand=self.scroll.set)

            is_command = re.match("/", data)
            if is_command == None:
                self.logText.insert(END, '%s:'%self.user)
            self.logText.insert(END,'%s\n'%data)
            
            if data == '/search':
                search.search(self)
            self.logText.config(width=60,height=35,state="disabled",yscrollcommand=self.scroll.set)
            self.logText.see("end")
            self.inputText.delete('1.0', END)

            client.handle_send(self.client_socket, self.user, data)
    
    def centerWindow(self, window ,width, height):
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = screen_width/2 - width/2
            y = screen_height/2 - height/2
            window.geometry('%dx%d+%d+%d' %(width,height,x,y))
            
    def signOut(self):
        # self.client_socket.close() 소켓 닫으면 안되요
        # 소켓 닫는거 대신
        # /logout 보내기
        
        self.client_socket.send(packet.cmdPacket('quit').encode())
        self.myParent.destroy()
        client.is_receive = 0
        signIn(self.client_socket)
        #signOut()

def signOut():
    #myWindow.client_socket.close()
    #myWindow.destroy()

    #print(client_socket)
    signIn()

    # 로그인 실행 함수
    ## 접속 유저 이름 정하는곳.
def signIn(client_socket):
    idRoot = Tk()
    myId = login.Login(idRoot, client_socket)
    idRoot.resizable(0,0)
    idRoot.mainloop()
    #print(successCheck)
    #if successCheck == True:
    myUser = ""
    if login.Login.loginSuccess(myId) == True:
        #if os.path.isfile("login.config"):
        #   loginFile = open('login.config',mode='rt',encoding='utf-8')
        #    lines = loginFile.readlines()
            #lines[3].splitlines()
        myUser = login.Login.returnNickname(myId)
        print(client.is_receive)
        client.is_receive = 1
            #user.rstrip('\n')
            #self.client_socket.send(loginPacket(self.idText.get(),self.passwdText.get()))  
    else:
        sys.exit()
    user = myUser.rstrip('\n')
    
    # 채팅 창
    chatRoot = Tk()
    myChat = Chatting(chatRoot, client_socket, user)

if __name__ == '__main__':
    #IPv4 체계, TCP 타입 소켓 객체를 생성\
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # 지정한 host와 prot를 통해 서버에 접속합니다.
    client_socket.connect((host, port))
    print(client_socket)

    signIn(client_socket)
    #chatRoot.resizable(0,0)
    #chatRoot.mainloop()
