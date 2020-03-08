from tkinter import *
import os
import guiClient
import loginFail
import json
import tkinter.font
import tkinter
import tkinter.ttk as ttk
from packet import *
#from guiClient import successCheck
import signUpResult
import packet
import sys
import json
from ctypes import windll
from tkinter import messagebox
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import titleBar

#close
def on_close(window):
    window.destroy()

#아이디 설정 클래스
class Login:
    def __init__(self, window, client_socket):
        # 현재 선택된 버튼을 나타냄
        self.selected = ""
        
        # 창을 파괴하기 위한 myParent
        self.myParent = window

        # 제목 표시줄 함수 -> TitleBarSet
        window.title("Sign In")
        #self.TitleBarSet()
        self.titlebar = titleBar.TitleBar(self.myParent)

        # x창 눌렀을 때 창 삭제
        self.myParent.protocol("WM_DELETE_WINDOW", lambda:self.on_close(self.myParent))

        # mainFrame은 창 전체를 뜻한다.
        self.mainFrame = Frame(window)
        #클라이언트 소켓
        self.client_socket = client_socket
        
        centerWindow(window, 300, 250)
        #window.geometry("250x140")
        self.mainFrame.pack(fill=X)
        self.successCheck = False

        #window.bind("<Return>",self.signInBtn)

        # 내 아이디&비밀번호
        self.myID = ""
        self.myNickname = ""

        #topFrame은 버튼 2개로, 로그인과 회원가입으로 변경할 수 있는 버튼이 있다.
        self.topFrame = Frame(self.mainFrame, background="#1C1C21")

        #topFrame에 들어갈 NavigationFrame
        navigationFrame = Frame(self.topFrame, background="#1E1E1E")

        #centerFrame은 로그인, 회원가입 등의 라벨 등을 출력
        self.centerFrame = Frame(self.mainFrame, width=20, height=200)

        #bottomFrame은 버튼을 놓는 프레임
        self.bottomFrame = Frame(self.mainFrame, background="#EFEFEF")

        self.topFrame.pack(fill=X, side=TOP)
        navigationFrame.pack(fill=X,side=TOP)
        self.centerFrame.pack(fill=BOTH, expand=True)
        self.bottomFrame.pack(fill=X, side=BOTTOM)

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
        self.nav_buttons['list'][0]['text'] = "Sign In"
        self.nav_buttons['list'][1]['text'] = "Sign Up"

        for i in range(self.nav_buttons['cnt']):
            #print(i)
            self.nav_buttons['list'][i].pack(side=LEFT)
        
        self.nav_buttons['list'][0]['command'] = lambda:self.sign_in(self.centerFrame)
        self.nav_buttons['list'][1]['command'] = lambda:self.sign_up(self.centerFrame)

        # default = sign_in
        self.sign_in(self.centerFrame)

        # select Language
        self.langCombobox = ttk.Combobox(self.bottomFrame,width=15, state="readonly")
        self.langCombobox['values'] = ("English","한국어","日本語")
        self.langCombobox.grid(column = 1, row=1)
        self.langCombobox.current(0)

        # 함수 연결
        #self.langCombobox.bind("<<ComboboxSelected>>",self.btnName(None,self.langCombobox.get()))
        self.langCombobox.bind("<<ComboboxSelected>>",self.langChange)

        self.langCombobox.pack(side=BOTTOM, ipady=5)
    """
        # 비밀번호 프레임
        #회원가입
        self.signUpButton = Button(window,text="회원가입", command=self.signUpBtn)
        self.signUpButton.pack(pady=10)
    """

##############################################################
    # 제목 표시줄 설정
    def TitleBarSet(self):
        self.myParent.overrideredirect(True)
        self.myParent.iconbitmap("./Icon/chat.ico")
        self.myParent.after(0,self.set_window)
        
        # 요소 설정하기
        s = ttk.Style()
        s.configure("titlebar.TFrame", background="#242424")
        s.theme_use('default')
        titlebar = ttk.Frame(self.myParent, style="titlebar.TFrame")
        widget = ttk.Frame(self.myParent)

        title = ttk.Label(titlebar,text=self.myParent.title(),style="titlebar.TLabel", background="#242424", foreground="#ffffff", font=("arial",15))

        s.configure("TButton", font=("arial", 8))
        s.configure("TButton", background='#424242')
        s.configure("TButton", foreground="white")
        
        s.map(
            "TButton",
            foreground=[('pressed','red'),('active','white')],
            background=[('pressed','#242424'),('active','#242424')]
        )
        close = ttk.Button(titlebar, text='X', takefocus=False, command=self.on_exit, width=4)
        #label = ttk.Label(widget, text="위젯 영역")

        # 요소 배치하기
        
        titlebar.pack(side='top', fill='x', expand='no')
        widget.pack(side = 'bottom', fill='both', expand='yes')
        title.pack(side='left', fill='x', expand='yes')
        close.pack(side='right')
        #label.pack()

        # 요소에 함수 바인딩
        #<BUTTONPRESS-1> : 마우스 왼쪽 버튼
        #<BUTTONRElease-1> : 마우스 왼쪽 버튼
        #<Double_Button-1> : 마우스 왼쪽 더블클릭
        #<B1-Motion>: 마우스 클릭 상태로 움직임
        title.bind("<ButtonPress-1>", self.start_move)
        title.bind("<ButtonRelease-1>", self.stop_move)
        title.bind("<B1-Motion>",self.on_move)

    #창의 제목을 클릭하여 위치를 옮기는 함수
    def start_move(self, event):
        self.myParent.x = event.x
        self.myParent.y = event.y

    # 마우스를 떼서 변수를 초기화시킴
    def stop_move(self, event):
        self.x = None
        self.y = None

    #마우스 드래그
    def on_move(self, event):
        deltax = event.x - self.myParent.x
        deltay = event.y - self.myParent.y
        x = self.myParent.winfo_x() + deltax
        y = self.myParent.winfo_y() + deltay
        self.myParent.geometry("+%s+%s" % (x,y))

    # 종료 버튼 함수
    def on_exit(self):
        self.myParent.destroy()
    
    # 윈도우 세팅
    def set_window(self):
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000000
        hwnd = windll.user32.GetParent(self.myParent.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd,GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd,GWL_EXSTYLE,style)
        self.myParent.wm_withdraw()
        self.myParent.after(0, lambda:self.myParent.wm_deiconify())

##################################################################

    # 이름 변경 함수라 다른 파일에서 사용 불가능하게 구현 예정
    def langChange(self, event=None):
        lang = self.langCombobox.get()
        if lang == "English":
            self.myParent.title = "Sign in"
            self.nav_buttons['list'][0]['text'] = "Sign in"
            self.nav_buttons['list'][1]['text'] = "Sign Up"
            if self.selected == "sign_in":
                self.loginButton.configure(text="Sign in")
            else:
                self.requestButton.configure(text="Sign Up")
        elif lang == "한국어":
            self.myParent.title = "로그인"
            self.nav_buttons['list'][0]['text'] = "로그인"
            self.nav_buttons['list'][1]['text'] = "회원가입"
            if self.selected == "sign_in":
                self.loginButton.configure(text="로그인")
            else:
                self.requestButton.configure(text="회원 가입")
        else:
            self.myParent.title = "サインイン"
            self.nav_buttons['list'][0]['text'] = "サインイン"
            self.nav_buttons['list'][1]['text'] = "サインアップ"
            if self.selected == "sign_in":
                self.loginButton.configure(text="サインイン")
            else:
                self.requestButton.configure(text="サインアップ")


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

            # ID를 담는 라벨
            self.idFrame = Frame(frame)
            self.idFrame.pack(expand=True,pady=5)
            self.idLabel = Label(self.idFrame,text="ID : ")
            self.idText = Entry(self.idFrame)
            self.idText.icursor(0)
            self.idText.focus_set()
            self.idLabel.pack(side=LEFT, ipadx = 13)
            self.idText.pack(side=RIGHT, padx = 20)

            # pw를 담는 라벨
            self.passwdFrame = Frame(frame)
            self.passwdFrame.pack(pady=5)
            self.passwdLabel = Label(self.passwdFrame,text = "Password : ")
            self.passwdText = Entry(self.passwdFrame,show="*")
            self.passwdLabel.pack(side=LEFT)
            self.passwdText.pack(side=RIGHT, padx=20)

            # 로그인 데이터 체크 버튼
            self.loginDataFrame = Frame(frame)
            self.loginDataFrame.pack(pady=5)
            self.login_check = BooleanVar()

            self.loginData = tkinter.Checkbutton(self.loginDataFrame, text="Stay signed in",variable=self.login_check)
            self.loginData.deselect()
            self.loginData.pack(side=BOTTOM, padx=20)

            self.loginButton = Button(frame,text="Sign in", command=self.signInBtn)
            #엔터키랑 연동
            self.myParent.bind('<Return>',self.signInBtn)
            self.loginButton.pack(pady=10)
            self.loginDataLoad()

    # 로그인 데이터 불러오기 함수
    def loginDataLoad(self):
        # 로그인.config가 있을 경우
        if os.path.isfile("loginData.config"):
            print("1")
            loginFile = open('loginData.config',mode='rt',encoding='utf-8')
            lines = loginFile.readlines()
            lines[2].splitlines()
            data = lines[0].rstrip('\n')
            if data == 'True':
                #print("ee"+lines[1])
                self.login_check.set(True)
                self.idText.insert(0,lines[1].rstrip('\n'))
                self.passwdText.insert(0,lines[2].rstrip('\n'))

        # 없으면 아무것도 안함
        else:
            pass

    # 회원가입 프레임
    def sign_up(self, frame):
        if self.selected != "sign_up":
            self.cleanFrame(frame)
            self.selected = "sign_up"
            self.myParent.bind("<Return>",self.signUpBtn)

            # ID를 입력하는 라벨
            self.idFrame = Frame(frame)
            self.idFrame.pack(expand=True, pady=5)
            self.idLabel = Label(self.idFrame,text="ID : ")
            self.idText = Entry(self.idFrame)
            self.idText.icursor(0)
            self.idText.focus_set()
            self.idLabel.pack(side=LEFT, ipadx = 13)
            self.idText.pack(side=RIGHT, padx = 20)

            # 비밀번호를 입력하는 라벨
            self.passwdFrame = Frame(frame)
            self.passwdFrame.pack(pady = 5)
            self.passwdLabel = Label(self.passwdFrame,text = "Password : ")
            self.passwdText = Entry(self.passwdFrame,show="*")
            self.passwdLabel.pack(side=LEFT)
            self.passwdText.pack(side=RIGHT, padx=20)

            # 닉네임을 입력하는 라벨
            self.nicknameFrame = Frame(frame)
            self.nicknameFrame.pack(pady = 5)
            self.nicknameLabel = Label(self.nicknameFrame, text="Nickname : ")
            self.nicknameText = Entry(self.nicknameFrame)
            self.nicknameLabel.pack(side=LEFT)
            self.nicknameText.pack(side=RIGHT, padx=20)

            # 가입 요청을 하는 버튼
            self.requestButton = Button(frame, text="Sign Up",command=self.signUpBtn)
            self.requestButton.pack(pady = 10)

    # 회원가입 요청을 하였을 때 실행
    def signUpBtn(self, event=None):
        # 빈 문자열인지 확인
        if (len(self.idText.get())!= 0) and (len(self.passwdText.get()) != 0) and (len(self.nicknameText.get()) != 0):
            self.createID()
        """
        resultScreen = Toplevel(self.myParent)
        #resultScreen.protocol("WM_DELETE_WINDOW", lambda:on_close(resultScreen))
        resultScreen.grab_set()
        
        # 조건 체크부분, 나중에 서버에서 비교하여 체크 필요
        if (len(self.idText.get())!= 0) and (len(self.passwdText.get()) != 0) and (len(self.nicknameText.get()) != 0):
            # 아이디를 Json파일로 생성
            self.createID()
            result = signUpResult.SignUpResult(resultScreen, "회원가입 성공")
            resultScreen.resizable(0,0)
            result.title = "회원가입 성공"
            resultScreen.mainloop()         

            self.sign_in(self.centerFrame)
        else:        
            resultScreen.title("회원가입 실패!")   
            result = signUpResult.SignUpResult(resultScreen, "회원가입 실패")
            resultScreen.resizable(0,0)
            resultScreen.mainloop()
        """

    def exitBtn(self, window, event=None):
        window.destroy()

    # id를 생성
    def createID(self):
        # 파일 데이터 생성
        #################### 필독 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # id와 패스워드와 닉네임이 사용가능한 문자열인지 무조건 확인 필요.(에러 예방)
        # 서버에서 보내는 ChkPacket{'packetType':'Chk', 'Chk': True}의 loginChk 여부에 따라 회원가입 성공, 실패
        self.client_socket.send(registerPacket(self.idText.get(),self.passwdText.get(),self.nicknameText.get()).encode())
        try:
            result = self.client_socket.recv(1024)
            parsed = Packet()
            parsed.packetify(result)
            try:
                # 회원가입 성공
                if parsed.packet['Chk'] == True:
                    messagebox.showinfo('Success!','Success in Sign Up')
                # 회원가입 실패
                else:
                    messagebox.showerror('Fail!','Fail to Sign Up')
            except Exception as err:
                messagebox.showerror('Fail!','{}'.format(err))
        except Exception as err:
            messagebox.showerror('fail','{}'.format(err))
                    
    
    def on_close(self, window):
        window.destroy()

    # ID,PW반환
    def returnNickname(self):
        return self.myNickname

    def returnID(self):
        return self.myID

    # 로그인 실행
    def signInCheck(self):
        # if os.path.isfile("loginData.config"):
        #     # 이부분은 아이디 불러오기 체크박스 기능에 추가할 예정
        #     # 나중에는 서버에서 json파일을 불러와서 처리
        #     loginFile = open('loginData.config', mode='rt', encoding='utf-8')
        #     lines = loginFile.readlines()
        #     max = len(lines)
            
        #     # 저장될 때 개행문자가 들어가서 +'\n'추가하여 비교하였음
        #     # 아이디 여러개 저장 가능 -> 삭제 예정
        #     # 이부분은 나중에 서버에서 처리
        #     for i in range(0,max-1,3):
        #         if (self.idText.get()+'\n' == lines[i]) and (self.passwdText.get()+'\n' == lines[i+1]):
        #             self.successCheck = True
        #             
        #             self.myNickname = lines[i+2]
                    
        #             self.myParent.destroy()
        #             break

        # # 전부 틀릴경우 로그인실패 출력
        # if self.successCheck == False:
        #     print("loginFail")
        #     # 탑레벨로 묶고 grab_set으로 고정
        #     self.failRoot = Toplevel(self.myParent)
        #     self.failRoot.grab_set()
        #     self.failWindow = loginFail.LoginFail(self.failRoot)
        #     self.failRoot.resizable(0,0)
        #     self.failRoot.mainloop()

        #################### 필독 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # 서버에서 보내는 loginChkPacket{'packetType':'loginChk', 'loginChk': True}의 loginChk 여부에 따라 로그인 성공, 실패
        
        self.client_socket.send(loginPacket(self.idText.get(),self.passwdText.get()).encode())
        #print("data : " + self.client_socket.recv(1024).decode('utf-8'))
        try :
            result = self.client_socket.recv(1024)
            #print(result)

            parsed = Packet()
            parsed.packetify(result)
            
            try:               
                print(parsed.packet['Chk'])
                if parsed.packet['Chk'] == True:
                    print("success")
                    self.myID = self.idText.get()
                    self.successCheck = True
                    # 체크박스 체크여부와 실행 시 데이터 확인
                    self.loginDataSave()
                    self.myNickname = (parsed.packet['nickName'])
                    self.client_socket.send(Packet('OnlineClients').encode())
                    self.myParent.destroy()
                    return
                else:
                    self.loginFailed()
            except Exception as er:
                #messagebox.showerror('Fail!','Fail to Sign Up')                print('{}'.format(er))
                self.loginFailed()
        except Exception as err:
            #messagebox.showerror('Fail!','Fail to Sign Up')
            print('{}'.format(err))
            self.loginFailed()

    # 로그인 데이터 저장 함수
    def loginDataSave(self):
        print("1")
        if self.login_check.get() == True:
            loginFile = open('loginData.config',mode='w',encoding='utf-8')
            loginFile.write('True\n')
            loginFile.write(self.idText.get()+'\n')
            loginFile.write(self.passwdText.get()+'\n')
            #loginFile.write(self.nicknameText.get()+'\n')
        # 저장 버튼이 off일경우 파일 삭제
        else:
            if os.path.isfile('loginData.config'):
                os.remove('loginData.config')


    # 로그인 실패
    def loginFailed(self):
        print("loginFail")
        # 탑레벨로 묶고 grab_set으로 고정
        self.failRoot = Toplevel(self.myParent)
        self.failRoot.grab_set()
        self.failWindow = loginFail.LoginFail(self.failRoot)
        self.failRoot.resizable(0,0)
        self.failRoot.mainloop()


    # 로그인 버튼 -> 로그인 체크만 수행한다.
    def signInBtn(self, event=None):
        self.signInCheck()
                    
    def loginSuccess(self):
        if(self.successCheck == True):
            return True
        else:
            return False

    # 창을 정 중앙에 위치
def centerWindow(window ,width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = screen_width/2 - width/2
        y = screen_height/2 - height/2
        window.geometry('%dx%d+%d+%d' %(width,height,x,y))
