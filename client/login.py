from tkinter import *
import os
import guiClient
import loginFail
import ctypes
import signUp
import json
import tkinter.font
import tkinter
import tkinter.ttk as ttk
from packet import *
#from guiClient import successCheck

import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

#class Language:

#아이디 설정 클래스
class Login:
    def __init__(self, window, client_socket):
        # 현재 선택된 버튼을 나타냄
        self.selected = ""
        
        # 창을 파괴하기 위한 myParent
        self.myParent = window

        # x창 눌렀을 때 창 삭제
        self.myParent.protocol("WM_DELETE_WINDOW", lambda:self.on_close(self.myParent))

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

        #topFrame은 버튼 2개로, 로그인과 회원가입으로 변경할 수 있는 버튼이 있다.
        self.topFrame = Frame(self.mainFrame, background="#1C1C21")

        #topFrame에 들어갈 NavigationFrame
        navigationFrame = Frame(self.topFrame, background="#1E1E1E")

        #centerFrame은 로그인, 회원가입 등의 라벨 등을 출력
        self.centerFrame = Frame(self.mainFrame)

        #bottomFrame은 버튼을 놓는 프레임
        self.bottomFrame = Frame(self.mainFrame, background="#EFEFEF")

        self.topFrame.pack(fill=BOTH, expand=True, side=TOP)
        navigationFrame.pack(fill=X,side=TOP)
        self.centerFrame.pack(fill=X, expand=True)
        self.bottomFrame.pack(fill=BOTH, expand=True, side=BOTTOM)

        # setting navigation buttons
        self.nav_buttons = {}
        self.nav_buttons['cnt'] = 2
        self.nav_buttons['frame'] = navigationFrame
        self.nav_buttons['list'] = []
        self.nav_buttons['height'] = 3
        self.nav_buttons['width'] = 20
        self.nav_buttons['font'] = font.Font(size=20)
        self.nav_buttons['foreground'] = "#FFFFFF"
        self.nav_buttons['background'] = "#1E1E1E"
        self.nav_buttons['activeforeground'] = "#FFFFFF"
        self.nav_buttons['activeforeground'] = "gray15"

        for i in range(self.nav_buttons['cnt']):
            self.nav_buttons['list'].append(Button(self.nav_buttons['frame']))
            self.nav_buttons['list'][i]['foreground'] = "#FFFFFF"
            self.nav_buttons['list'][i]['background'] = "#1E1E1E"
            self.nav_buttons['list'][i]['activeforeground'] = "#FFFFFF"
            self.nav_buttons['list'][i]['activeforeground'] = "gray15"
            self.nav_buttons['list'][i]['width'] = self.nav_buttons['width']
            self.nav_buttons['list'][i]['height'] = self.nav_buttons['height']

        # add navigation Buttons
        self.nav_buttons['list'][0]['text'] = "Login"
        self.nav_buttons['list'][1]['text'] = "Sign Up"

        for i in range(self.nav_buttons['cnt']):
            print(i)
            self.nav_buttons['list'][i].pack(side=LEFT)
        
        self.nav_buttons['list'][0]['command'] = lambda:self.sign_up(self.centerFrame)
        self.nav_buttons['list'][1]['command'] = lambda:self.sign_in(self.centerFrame)

        # default = sign_up
        self.sign_up(self.centerFrame)

        # select Languate
        self.langCombobox = ttk.Combobox(self.bottomFrame,width=15, state="readonly")
        self.langCombobox['values'] = ("English","한국어","日本語")
        self.langCombobox.grid(column = 1, row=1)
        self.langCombobox.current(0)
        # 함수 연결
        #self.langCombobox.bind("<<ComboboxSelected>>",self.btnName(None,self.langCombobox.get()))
        self.langCombobox.bind("<<ComboboxSelected>>",self.langChange)

        self.langCombobox.pack(side=BOTTOM)
    """
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
    """
    # 이름 변경 함수라 다른 파일에서 사용 불가능하게 구현 예정
    def langChange(self, event):
        lang = self.langCombobox.get()
        if lang == "English":
            self.nav_buttons['list'][0]['text'] = "Login"
            self.nav_buttons['list'][1]['text'] = "Sign Up"
        elif lang == "한국어":
            self.nav_buttons['list'][0]['text'] = "로그인"
            self.nav_buttons['list'][1]['text'] = "회원가입"
        else:
            self.nav_buttons['list'][0]['text'] = "サインイン"
            self.nav_buttons['list'][1]['text'] = "サインアップ"


    # 프레임을 전부 삭제
    def cleanFrame(self, frame):
        self.selected = ""
        # 이론적으로는 pack된 slaves를 destroy
        for i in frame.pack_slaves():
            print(i)
            i.destroy()

    # 로그인 프레임
    def sign_in(self, frame):
        if self.selected != "sign_in":
            self.cleanFrame(frame)
            self.selected = "sign_in"
            testLabel = Label(frame, text="dd")
            testLabel.pack()

    # 회원가입 프레임
    def sign_up(self, frame):
        if self.selected != "sign_up":
            self.cleanFrame(frame)
            self.selected = "sign_up"
            testLabel = Label(frame, text="cc")
            testLabel.pack()

    # 회원가입 버튼
    def signUpBtn(self):
        signUpRoot = Toplevel(self.myParent)
        signUpRoot.grab_set()
        mySignUp = signUp.SignUp(signUpRoot, self.client_socket)
        signUpRoot.resizable(0,0)
        signUpRoot.mainloop()
    
    def on_close(self, window):
        window.destroy()

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
        width = 300
        height = 250
        screen_width = self.myParent.winfo_screenwidth()
        screen_height = self.myParent.winfo_screenheight()
        x = screen_width/2 - width/2
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))