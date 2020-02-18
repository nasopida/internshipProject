from tkinter import *
#import client.client as client
#import client.guiClient as guiClient
import client
import guiClient

import ctypes
import tkinter as tk
import tkinter.ttk
from userListManage import cutOffUser
from userListManage import banUser

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class UserList:
    def __init__(self, window):
        # 자신의 창을 가리킴
        self.myParent = window
        #메인 프레임
        self.mainFrame = Frame(window)
        self.mainFrame.pack() 
        window.title('유저 리스트')
        self.centerWindow(window)

        # 프레임 리스트
        self.frameList = []
        # 체크박스 리스트
        self.checkBoxList = []
        # 유저 수 
        self.userCnt = 0
        # 유저 리스트
        self.user_list = {}

        #유저수 출력 라벨
        self.printUserFrame = Frame(self.mainFrame)
        self.printUserFrame.pack(side=TOP, expand = True, pady = 5)
        self.printUserLabel = Label(self.printUserFrame, text="ㅎㅇ")
        self.printUserLabel.pack(side=TOP, expand=True)

        #유저를 담는 라벨
        
        self.userFrame = tk.Frame(self.mainFrame, width=300, height=540, relief='raised',borderwidth=1)
        self.userFrame.pack(fill=BOTH, expand=True)

        self.userScrollbar = Scrollbar(self.userFrame)
        self.userScrollbar.pack(side=RIGHT, fill=Y)


        #버튼들의 프레임
        self.btnFrame = tk.Frame(self.mainFrame)
        self.btnFrame.pack(fill=X, side=BOTTOM)
        # 강퇴 요청 버튼
        self.banBtn =  Button(self.btnFrame,width=20, command=self.banUser, text="강퇴 요청")
        self.banBtn.pack(side=LEFT)
        # 차단 버튼
        self.blackListUserBtn = Button(self.btnFrame, width=20, command=self.cutOffUser, text="차단")
        self.blackListUserBtn.pack(side=RIGHT)     
    
    # 아래 2개 함수는 유저가 들어올때 / 나갈때 자동 호출되도록 구현
    # 유저를 추가시키는 함수
    def addUser(self, userName):
        tempVar = BooleanVar(value=False)
        tempFrame = Frame(self.userFrame)
        self.frameList.append(tempFrame)
        temp = Checkbutton(tempFrame, variable=tempVar, text = userName)
        self.checkBoxList.append(tempVar)
        tempFrame.pack(side=TOP, fill=X)
        temp.pack(side=LEFT)
        self.user_list[userName] = self.userCnt
        self.userCnt += 1
        self.printUserLabel["text"] = "user : " + str(self.userCnt)
        
    # 유저가 나갔을 때 실행되는 함수
    def deleteUser(self, userName):
        pass

    # 강퇴투표 함수
    def banUser(self):
        self.banRoot = Toplevel(self.myParent)
        self.banRoot.grab_set()
        banWindow = banUser.BanUser(self.banRoot, self.user_list)
        self.banRoot.resizable(0,0)
        self.banRoot.mainloop()

    # 유저를 차단하는 함수, 구현순위 맨 뒤
    def cutOffUser(self):
        self.cutOffRoot = Toplevel(self.myParent)
        self.cutOffRoot.grab_set()
        cutOfftWindow = cutOffUser.CutOffUser(self.cutOffRoot, self.user_list)
        self.cutOffRoot.resizable(0,0)
        self.cutOffRoot.mainloop()

    #가운데로 오게 하는 함수
    def centerWindow(self, window):
        width = 300
        height = 600
        userScreen = ctypes.windll.user32
        screen_width = userScreen.GetSystemMetrics(0)
        screen_height = userScreen.GetSystemMetrics(1)
        #x = screen_width/2 - width/2 + 400
        x = screen_width / 2 + 200 + 3
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))
