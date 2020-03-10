from tkinter import *
import os
import client
import titleBar
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

class BlackList:
    def __init__(self, window, user_list, darkModeOn):
        # 자신의 창을 가리킴
        self.myParent = window
        # 가져온 유저 리스트
        self.user_list = user_list
       
        # 타이틀바 설정
        window.title('유저 차단하기')
        self.myParent.iconbitmap("./Icon/BlackList.ico")
        #self.titlebar = titleBar.TitleBar(self.myParent)

        #메인 프레임
        self.mainFrame = Frame(window)
        self.mainFrame.pack() 

        self.centerWindow(window)
        # 가져온 유저 리스트
        self.user_list = user_list
        #유저 체크박스리스트
        self.CheckBoxVarList = []
        #상단 프레임
        self.topFrame = Frame(window)
        self.titleLabel = Label(self.topFrame, text="유저 차단")
        self.titleLabel.pack(fill=X, side=TOP)
        self.topFrame.pack(fill=X, side=TOP)

        #메인 프레임
        self.mainFrame = Frame(window)
        self.mainFrame.pack(fill=BOTH, expand=TRUE, side=TOP) 
        window.title('유저 차단')
        self.centerWindow(window)
        
        self.centerFrame = Frame(window)
        self.inputUser(darkModeOn)
        self.centerFrame.pack()

        #하단 버튼 프레임
        self.btnFrame = Frame(self.myParent)
        self.enterBtn = Button(self.btnFrame, width=20, text="차단하기", command=self.BanUser)
        self.enterBtn.pack(side=BOTTOM)
        self.btnFrame.pack(fill=BOTH, side=BOTTOM)
        self.darkMode(darkModeOn)

    def darkMode(self, darkModeOn):
        if darkModeOn == True:
            self.myParent.configure(background='#242424')
            self.topFrame.configure(background='#242424')
            self.mainFrame.configure(background='#242424')
            self.btnFrame.configure(background='#242424')
            self.titleLabel['bg'] = '#242424'
            self.titleLabel['fg'] = '#ffffff'
            self.enterBtn['bg'] = '#424242'
            self.enterBtn['fg'] = '#ffffff'
        else:
            self.myParent.configure(background='#f0f0f0')
            self.topFrame.configure(background='#f0f0f0')
            self.mainFrame.configure(background='#f0f0f0')
            self.btnFrame.configure(background='#f0f0f0')
            self.titleLabel['bg'] = '#f0f0f0'
            self.titleLabel['fg'] = '#000000'
            self.enterBtn['bg'] = '#f0f0f0'
            self.enterBtn['fg'] = '#000000'

    def BanUser(self):
        pass

    def inputUser(self, darkModeOn):
        for userName in self.user_list:
            #print("hi")
            tempVar = BooleanVar(value=False)
            tempFrame = Frame(self.mainFrame)
            temp = Checkbutton(tempFrame, variable=tempVar, text=userName)
            self.CheckBoxVarList.append(tempVar)
            if darkModeOn == True:
                tempFrame.configure(background="#242424")
                temp['bg'] = '#242424'
                temp['fg'] = '#ffffff'
                temp['selectcolor'] = '#424242'
            else:
                pass
            tempFrame.pack(side=TOP, fill=X)
            temp.pack(side=LEFT)

     #가운데로 오게 하는 함수
    def centerWindow(self, window):
        width = 300
        height = 400
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        #x = screen_width/2 - width/2 + 400
        x = screen_width / 2 - height/2 + 50
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))
