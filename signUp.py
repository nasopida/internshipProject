from tkinter import *
import ctypes
import setID
import json
import os
from collections import OrderedDict
from packet import *

# 회원가입을 진행하는 클래스
class SignUp:
    def __init__(self, window):
        #나중에 창을 파괴하기 위해
        self.myParent = window

        #mainFrame은 창 전체이다.
        self.mainFrame = Frame(window)
        window.title("회원 가입")
        #window.geometry("250x140")
        self.centerWindow(window)
        
        window.bind("<Return>",self.requestBtn)
        self.mainFrame.pack()

        # ID를 입력하는 라벨
        self.idFrame = Frame(self.mainFrame)
        self.idFrame.pack(expand=True, pady=5)
        self.idLabel = Label(self.idFrame,text="ID : ")
        self.idText = Entry(self.idFrame)
        self.idText.icursor(0)
        self.idText.focus_set()
        self.idLabel.pack(side=LEFT, ipadx = 13)
        self.idText.pack(side=RIGHT, padx = 30)

        # 비밀번호를 입력하는 라벨
        self.passwdFrame = Frame(self.mainFrame)
        self.passwdFrame.pack(pady = 5)
        self.passwdLabel = Label(self.passwdFrame,text = "Password : ")
        self.passwdText = Entry(self.passwdFrame,show="*")
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
    def requestBtn(self, event=None):
        if (len(self.idText.get())!= 0) and (len(self.passwdText.get()) != 0) and (len(self.nicknameText.get()) != 0):
            # 아이디를 Json파일로 생성
            self.createID()
            self.myParent.destroy()
    
    def createID(self):
        # 파일 데이터 생성
        alterPacket(self.idText.get(),self.passwdText.get(),self.nicknameText.get())
        """
        user_data = OrderedDict()

        user_data["packetType"] = "alter"
        user_data["userID"] = self.idText.get()
        user_data["userPass"] = self.passwdText.get()
        user_data["user"] = self.nicknameText.get()
        user_data["timestamp"] = ""
        # Json파일로 생성
        # 생성한 json파일을 서버에 송신해주어야 함
        with open('user.json','w',encoding="utf-8") as make_file:
            json.dump(user_data,make_file,ensure_ascii=False,indent="\t")
        
        # 서버에 보낸 이후에 실행할 문장 -> 한 컴퓨터에서 회원가입을 여러개 하기 위해 json파일을 송신 후 삭제함
        #os.remove('user.json')
        """

        # 로그인 정보 저장하기 위한 config파일(저장 버튼 추가예정)
        f = open('login.config','a',encoding='utf-8')
        f.write(self.idText.get()+'\n')
        f.write(self.passwdText.get()+'\n')
        f.write(self.nicknameText.get()+'\n')
        f.close()

    
    # 화면을 중앙으로 오게 해주는 함수
    def centerWindow(self, window):
        width = 250
        height = 140
        userScreen = ctypes.windll.user32
        screen_width = userScreen.GetSystemMetrics(0)
        screen_height = userScreen.GetSystemMetrics(1)
        x = screen_width/2 - width/2
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))