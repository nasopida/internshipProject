import guiClient
from tkinter import *
import ctypes

# 로그인 실패 창
class LoginFail:
    def __init__(self, window):
        #창 파괴를 위한 변수
        self.myParent = window

        # mainFrame
        self.mainFrame = Frame(window)
        window.title("로그인 실패!")
        #window.geometry("200x80")
        self.centerWindow(window)
        self.mainFrame.pack()

        # 로그인 실패를 출력
        self.failLabel = Label(self.mainFrame, text="로그인 실패!")
        self.failLabel.pack(fill=BOTH, padx=30, pady=10)

        # 종료 버튼
        self.endButton = Button(self.mainFrame, text="확인", command=self.endBtn)
        self.endButton.pack(pady=5)
    def endBtn(self):
        self.myParent.destroy()

    # 윈도우 창
    def centerWindow(self, window):
        width = 200
        height = 80
        userScreen = ctypes.windll.user32
        screen_width = userScreen.GetSystemMetrics(0)
        screen_height = userScreen.GetSystemMetrics(1)
        x = screen_width/2 - width/2
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))