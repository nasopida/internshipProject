from tkinter import *
import ctypes
import setID

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