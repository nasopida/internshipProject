from tkinter import *
import os
import guiClient
import loginFail
import ctypes
import signUp
#from guiClient import successCheck

#아이디 설정 클래스
class SetID:
    def __init__(self, window):
        # 창을 파괴하기 위한 myParent
        self.myParent = window
        # mainFrame은 창 전체를 뜻한다.
        self.mainFrame = Frame(window)
        window.title("로그인")
        self.centerWindow(window)
        #window.geometry("250x140")
        self.mainFrame.pack(fill=X)
        self.successCheck = False

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
        mySignUp = signUp.SignUp(signUpRoot)
        signUpRoot.mainloop()

    # 로그인 버튼
    def signInBtn(self):
        #global suc
        if os.path.isfile("login.config"):
            loginFile = open('login.config', mode='rt', encoding='utf-8')
            lines = loginFile.readlines()
            #print((self.idText.get()+'\n' == lines[0]))
            #print((self.passwdText.get()+'\n' == lines[1]))
            # 저장될 때 개행문자가 들어가서 +'\n'추가하여 비교하였음
            if (self.idText.get()+'\n' == lines[0]) and (self.passwdText.get()+'\n' == lines[1]):
                self.successCheck = True
                self.myParent.destroy()
            else:
                self.successCheck = False
                failRoot = Tk()
                failWindow = loginFail.LoginFail(failRoot)
                failRoot.mainloop()
                
        else:
            self.successCheck = False
            failRoot = Tk()
            failWindow = loginFail.LoginFail(failRoot)
            failRoot.mainloop()
            
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