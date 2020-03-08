import tkinter.ttk as ttk
import tkinter as Tk
from ctypes import windll
    
    # 제목 표시줄 설정
class TitleBar:
    def __init__(self, window):
        self.window = window
        self.TitleBarSet()

    def TitleBarSet(self):
        #self.window.iconbitmap("./Icon/chat.ico")
        self.window.overrideredirect(True)
        self.window.after(10,self.set_window(self.window))
        
        # 요소 설정하기
        s = ttk.Style()
        s.configure("titlebar.TFrame", background="#242424")
        s.theme_use('default')
        titlebar = ttk.Frame(self.window, style="titlebar.TFrame")
        #widget = ttk.Frame(self.window)

        title = ttk.Label(titlebar,text=self.window.title(),style="titlebar.TLabel", background="#242424", foreground="#ffffff", font=("arial",15))

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
        print("ok")
        titlebar.pack(side='top', fill='x', expand='no')
        #widget.pack(side = 'bottom', fill='both', expand='yes')
        title.pack(side='left', fill='x', expand='yes')
        close.pack(side='right')
        #label.pack()

        # 요소에 함수 바인딩
        #<BUTTONPRESS-1> : 마우스 왼쪽 버튼
        #<BUTTONRElease-1> : 마우스 왼쪽 버튼
        #<Double_Button-1> : 마우스 왼쪽 더블클릭
        #<B1-Motion>: 마우스 클릭 상태로 움직임
        
        #title.bind("<ButtonPress-1>", lambda:start_move(window))
        #title.bind("<ButtonRelease-1>", lambda:stop_move(window))
        #title.bind("<B1-Motion>",lambda:on_move(window))
        title.bind("<ButtonPress-1>", self.start_move)
        title.bind("<ButtonRelease-1>", self.stop_move)
        title.bind("<B1-Motion>",self.on_move)


    #창의 제목을 클릭하여 위치를 옮기는 함수
    def start_move(self, event):
        self.window.x = event.x
        self.window.y = event.y

    # 마우스를 떼서 변수를 초기화시킴
    def stop_move(self, event):
        self.window.x = None
        self.window.y = None

    #마우스 드래그
    def on_move(self, event):
        deltax = event.x - self.window.x
        deltay = event.y - self.window.y
        x = self.window.winfo_x() + deltax
        y = self.window.winfo_y() + deltay
        self.window.geometry("+%s+%s" % (x,y))

    # 종료 버튼 함수
    def on_exit(self):
        self.window.destroy()
        
    # 윈도우 세팅
    
    def set_window(self, root):
        GWL_EXSTYLE=-20
        WS_EX_APPWINDOW=0x00040000
        WS_EX_TOOLWINDOW=0x00000080
        hwnd = windll.user32.GetParent(root.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        # re-assert the new window style
        root.wm_withdraw()
        root.wm_deiconify()
        root.after(10, lambda: root.wm_deiconify())
    ##################################################################
# 오리지널 타이틀바로, TitleBar 상속
class TitleBarOriginal(TitleBar):
    def __init__(self, window):
        TitleBar.__init__(self, window)


# 채팅만을 위한 TitleBar로, TitleBar 상속
class TitleBarChat(TitleBar):
    def __init__(self, window, client_socket):
        TitleBar.__init__(self,window)
        self.client_socket = client_socket

    def on_exit(self):
        self.window.destroy()
        self.client_socket.close()