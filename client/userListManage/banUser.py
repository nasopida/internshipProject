from tkinter import *
import os
import ctypes
import client
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

class BanUser:
    def __init__(self, window, user_list):
        # 자신의 창을 가리킴
        self.myParent = window
        # 가져온 유저 리스트
        self.user_list = user_list
        #메인 프레임
        self.mainFrame = Frame(window)
        self.mainFrame.pack() 
        window.title('유저 강퇴투표 하기')
        self.centerWindow(window)
        # 가져온 유저 리스트
        self.user_list = user_list
        #유저 체크박스리스ㅡㅌ
        self.CheckBoxVarList = []
        #상단 프레임
        self.topFrame = Frame(window)
        titleLabel = Label(self.topFrame, text="유저 차단")
        titleLabel.pack(fill=X, side=TOP)
        self.topFrame.pack(fill=X, side=TOP)

        #메인 프레임
        self.mainFrame = Frame(window)
        self.mainFrame.pack(fill=BOTH, expand=TRUE, side=LEFT) 
        window.title('유저 차단')
        self.centerWindow(window)
        
        self.centerFrame = Frame(window)
        self.inputUser()
        self.centerFrame.pack()

        #하단 버튼 프레임
        self.btnFrame = Frame(self.myParent)
        enterBtn = Button(self.btnFrame, width=20, text="차단하기", command=self.BanUser)
        enterBtn.pack(side=LEFT)
        self.btnFrame.pack(fill=BOTH, side=BOTTOM)

    def BanUser(self):
        pass

    def inputUser(self):
        for userName in self.user_list:
            #print("hi")
            tempVar = BooleanVar(value=False)
            tempFrame = Frame(self.mainFrame)
            temp = Checkbutton(tempFrame, variable=tempVar, text=userName)
            self.CheckBoxVarList.append(tempVar)
            tempFrame.pack(side=TOP, fill=X)
            temp.pack(side=LEFT)

     #가운데로 오게 하는 함수
    def centerWindow(self, window):
        width = 300
        height = 400
        userScreen = ctypes.windll.user32
        screen_width = userScreen.GetSystemMetrics(0)
        screen_height = userScreen.GetSystemMetrics(1)
        #x = screen_width/2 - width/2 + 400
        x = screen_width / 2 - height/2 + 50
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))
