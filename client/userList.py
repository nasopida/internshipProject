from tkinter import *
#import client.client as client
#import client.guiClient as guiClient
import client
import guiClient

import tkinter as tk
import tkinter.ttk
from userListManage import cutOffUser
from userListManage import banUser
import titleBar
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class UserList:
    def __init__(self, window, chatWindow):
        # 자신의 창을 가리킴
        self.myParent = window

        # 타이틀바 설정
        window.title('유저 리스트')
        self.titlebar = titleBar.TitleBar(self.myParent)

        # 채팅창 윈도우를 가리킴
        self.chatWindow = chatWindow

        # 메인 프레임
        self.mainFrame = Frame(window)
        self.mainFrame.pack() 
        self.centerWindow(window)
        self.darkModeOn = False

        # 프레임 리스트
        self.frameList = []
        # 체크박스 리스트
        self.checkBoxList = []
        # 체크박스를 가리키는 유저리스트
        self.checkUserList = []
        # 유저 수 
        self.userCnt = 0
        # 유저 리스트
        self.user_list = {}

        # 유저수 출력 라벨
        self.printUserFrame = Frame(self.mainFrame)
        self.printUserFrame.pack(side=TOP, expand = True, pady = 5)
        self.printUserLabel = Label(self.printUserFrame, text="ㅎㅇ")
        self.printUserLabel.pack(side=TOP, expand=True)

        # 유저를 담는 라벨
        
        self.userFrame = tk.Frame(self.mainFrame, width=300, height=540, relief='raised',borderwidth=1)
        self.userFrame.pack(fill=BOTH, expand=True)

        self.userScrollbar = Scrollbar(self.userFrame)
        self.userScrollbar.pack(side=RIGHT, fill=BOTH)

        # 버튼들의 프레임
        self.btnFrame = tk.Frame(self.mainFrame)
        self.btnFrame.pack(fill=X, side=BOTTOM)
        # 강퇴 요청 버튼
        self.banBtn =  Button(self.btnFrame,width=13, command=self.banUser, text="강퇴 요청")
        self.banBtn.pack(side=LEFT)
        
        # 차단 버튼
        self.blackListUserBtn = Button(self.btnFrame, width=13, command=self.cutOffUser, text="차단")
        self.blackListUserBtn.pack(side=RIGHT)
        #다크모드 버튼
        self.darkModeBtn=Button(self.btnFrame,width=14,command=self.darkMode,text="다크모드")
        self.darkModeBtn.pack(side=BOTTOM)
    
    # 아래 2개 함수는 유저가 들어올때 / 나갈때 자동 호출되도록 구현
    # 유저를 추가시키는 함수
    def addUser(self, userName):
        tempVar = BooleanVar(value=False)
        tempFrame = Frame(self.userFrame)
        self.frameList.append(tempFrame)
        temp = Checkbutton(tempFrame, variable=tempVar, text = userName)
        self.checkBoxList.append(tempVar)
        self.checkUserList.append(temp)
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
        banWindow = banUser.BanUser(self.banRoot, self.user_list, self.darkModeOn)
        self.banRoot.resizable(0,0)
        self.banRoot.mainloop()

    # 유저를 차단하는 함수, 구현순위 맨 뒤
    def cutOffUser(self):
        self.cutOffRoot = Toplevel(self.myParent)
        self.cutOffRoot.grab_set()
        cutOfftWindow = cutOffUser.CutOffUser(self.cutOffRoot, self.user_list, self.darkModeOn)
        self.cutOffRoot.resizable(0,0)
        self.cutOffRoot.mainloop()

    #다크모드 함수
    def darkMode(self):
        # 채팅창 윈도우를 수정
        #print(self)
        #print(self.chatWindow)
        self.chatWindow.darkMode()
        
        if self.darkModeOn == False:
            # 유저리스트 윈도우를 수정
            self.myParent.configure(background='#242424')
            self.mainFrame.configure(background='#242424')
            self.printUserLabel['bg']='#242424'
            self.printUserLabel['fg']='#ffffff'
            self.userFrame.configure(background='#242424')
            self.banBtn['bg']='#424242'
            self.banBtn['fg']='#ffffff'
            self.blackListUserBtn['bg']='#424242'
            self.blackListUserBtn['fg']='#ffffff'
            self.darkModeBtn['bg']='#424242'
            self.darkModeBtn['fg']='#ffffff'
            for users in self.frameList:
                users.configure(background='#242424')
            for checkuser in self.checkUserList:
                checkuser['bg'] = '#242424'
                checkuser['fg'] = '#ffffff'
                checkuser['selectcolor'] = '#424242'
            self.darkModeOn = True
        else:
            self.myParent.configure(background='#f0f0f0')
            self.mainFrame.configure(background='#f0f0f0')
            self.printUserLabel['bg']='#f0f0f0'
            self.printUserLabel['fg']='#000000'
            self.userFrame.configure(background='#f0f0f0')
            self.banBtn['bg']='#f0f0f0'
            self.banBtn['fg']='#000000'
            self.blackListUserBtn['bg']='#f0f0f0'
            self.blackListUserBtn['fg']='#000000'
            self.darkModeBtn['bg']='#f0f0f0'
            self.darkModeBtn['fg']='#000000'
            for users in self.frameList:
                users.configure(background='#f0f0f0')
            for checkuser in self.checkUserList:
                checkuser['bg'] = '#f0f0f0'
                checkuser['fg'] = '#000000'
                checkuser['selectcolor'] = '#ffffff'
            self.darkModeOn = False

    #가운데로 오게 하는 함수
    def centerWindow(self, window):
        width = 300
        height = 600
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        #x = screen_width/2 - width/2 + 400
        x = screen_width / 2 + 200 + 3
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))

    

