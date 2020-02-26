from tkinter import *
import os
import guiClient
import loginFail
import ctypes
import signUp
import json
from packet import *
#from guiClient import successCheck

import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#아이디 설정 클래스
class SetID:
    def __init__(self, window, client_socket):
        # 창을 파괴하기 위한 myParent
        self.myParent = window
        # mainFrame은 창 전체를 뜻한다.
        self.mainFrame = Frame(window)
        #클라이언트 소켓
        self.client_socket = client_socket

        window.title("로그인")
        self.centerWindow(window)
        #window.geometry("250x140")
        self.mainFrame.pack(fill=X)
        self.successCheck = False

        window.bind("<Return>",self.signInBtn)

        # 내 아이디&비밀번호
        self.myNickname = ""

        # ID 프레임
        self.idFrame = Frame(self.mainFrame)
        self.idFrame.pack(expand=True,pady=5)
        self.idLabel = Label(self.idFrame,text="ID : ")
        self.idText = Entry(self.idFrame)
        self.idText.icursor(0)
        self.idText.focus_set()
        self.idLabel.pack(side=LEFT, ipadx = 13)
        self.idText.pack(side=RIGHT, padx = 30)

        # 비밀번호 프레임
        self.passwdFrame = Frame(self.mainFrame)
        self.passwdFrame.pack()
        self.passwdLabel = Label(self.passwdFrame,text = "Password : ")
        self.passwdText = Entry(self.passwdFrame,show="*")
        self.passwdLabel.pack(side=LEFT)
        self.passwdText.pack(side=RIGHT, padx=10)
        
        
        self.loginButton = Button(window,text="로그인", command=self.signInBtn, relief=RIDGE)
        #엔터키랑 연동
        #window.bind('<Return>',self.enterBtn)
        self.loginButton.pack(pady=10)

        #회원가입
        self.signUpButton = Button(window,text="회원가입", command=self.signUpBtn)
        self.signUpButton.pack(pady=10)
    # 회원가입 버튼

    def signUpBtn(self):
        signUpRoot = Toplevel(self.myParent)
        signUpRoot.grab_set()
        mySignUp = signUp.SignUp(signUpRoot, self.client_socket)
        signUpRoot.resizable(0,0)
        signUpRoot.mainloop()

    # ID,PW반환
    def returnNickname(self):
        return self.myNickname

    # 로그인 버튼
    def signInBtn(self, event=None):
        #global suc
        if os.path.isfile("login.config"):
            # 이부분은 아이디 불러오기 체크박스 기능에 추가할 예정
            # 나중에는 서버에서 json파일을 불러와서 처리
            loginFile = open('login.config', mode='rt', encoding='utf-8')
            lines = loginFile.readlines()
            max = len(lines)
            
            # 저장될 때 개행문자가 들어가서 +'\n'추가하여 비교하였음
            # 아이디 여러개 저장 가능 -> 삭제 예정
            # 이부분은 나중에 서버에서 처리
            for i in range(0,max-1,3):
                if (self.idText.get()+'\n' == lines[i]) and (self.passwdText.get()+'\n' == lines[i+1]):
                    self.successCheck = True
                    self.myNickname = lines[i+2]
                    self.client_socket.send(loginPacket(self.idText.get(),self.passwdText.get()).encode())
                    
                    self.myParent.destroy()
                    break
        # 전부 틀릴경우 로그인실패 출력
        if self.successCheck == False:
            print("loginFail")
            # 탑레벨로 묶고 grab_set으로 고정
            self.failRoot = Toplevel(self.myParent)
            self.failRoot.grab_set()
            self.failWindow = loginFail.LoginFail(self.failRoot)
            self.failRoot.resizable(0,0)
            self.failRoot.mainloop()
            
    def successCheck(self):
        if(self.successCheck == True):
            return True
        else:
            return False
        

    # 창을 정 중앙에 위치
    def centerWindow(self, window):
        width = 250
        height = 140
        userScreen = ctypes.windll.user32
        screen_width = userScreen.GetSystemMetrics(0)
        screen_height = userScreen.GetSystemMetrics(1)
        x = screen_width/2 - width/2
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))