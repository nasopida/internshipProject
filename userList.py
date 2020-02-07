from tkinter import *
import guiClient
import ctypes

class UserList:
    def __init__(self, window):
        # 자신의 창을 가리킴
        self.myParent = window
        #메인 프레임
        self.mainFrame = Frame(window)
        self.mainFrame.pack() 
        window.title('유저 리스트')
        self.centerWindow(window)

        # 체크박스 리스트
        self.checkBoxList = []
        # 유저 수 
        self.userCnt = 0

        #유저수 출력 라벨
        self.printUserFrame = Frame(self.mainFrame)
        self.printUserFrame.pack(expand = True, pady = 5)
        self.printUserLabel = Label(self.printUserFrame, text="ㅎㅇ")
        self.printUserLabel.pack(expand = True)

        #유저를 담는 라벨
        self.userFrame = Frame(self.mainFrame)
        self.userFrame.pack(fill=X, side=LEFT)

        self.addUser('안녕')


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
    
    # 아래 2개 함수는 유저가 들어올때 / 나갈때 자동 호출되도록 구현
    # 유저를 추가시키는 함수
    def addUser(self, userName):
        tempVar = BooleanVar(value=False)
        tempFrame = Frame(self.userFrame, background="WHITE")
        temp = Checkbutton(tempFrame, variable=tempVar, text=userName, background="WHITE", activebackground="WHITE")
        self.checkBoxList.append(tempVar)
        temp.pack(fill=X,side=LEFT)
        tempFrame.pack(fill=X,side=LEFT)
        self.userCnt += 1
        self.printUserLabel["text"] = "user : " + str(self.userCnt)

    # 유저를 제거하는 함수
    def deleteUser(self, userName):
        pass

    # 유저를 차단하는 함수, 구현순위 맨 뒤
    def blackUser(self, userName):
        pass

