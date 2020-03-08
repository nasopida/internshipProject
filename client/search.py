import guiClient
from tkinter import *
import tkinter
searchWord = None
import titleBar

def search(self):
    search_window = tkinter.Toplevel(self.myParent)
    #검색창으로 화면 고정
    search_window.grab_set()
    frame = Frame(search_window)
    search_window.title("검색")
    self.titlebar = titleBar.TitleBar(search_window)
    self.centerWindow(search_window,200,70)
    #search_window.geometry("200x50")
    word = Text(search_window)
    word.config(width = 20, height = 1)
    word.pack()
    self.searchWindowON()

    #word로 창 이동
    word.focus_set()

    def close():
        self.searchWindowOFF()
        search_window.destroy()
        self.delete_highlighting()
        return;
    search_window.protocol('WM_DELETE_WINDOW', close)
    def search_button(event):
        global searchWord
        self.delete_highlighting()
        if searchWord != word.get('1.0', END):
            searchWord = word.get('1.0', END)
        search_word = searchWord.rstrip('\n')
        line = 1
        data = self.get_searchData()
        line_div = []
        for div in re.finditer('\n', data):
            if div not in line_div:
                line_div.append(div.end())
        if len(search_word) > 0:
            for match in re.finditer(search_word, data):
                s = match.start()
                e = match.end()
                tempS = s
                tempE = e
                for line_num in line_div:
                    if s >= line_num:
                        line = line + 1
                        tempS = s - line_num
                        tempE = tempS + e - s
                self.highlighting(line, tempS, tempE)
                line = 1
    button = Button(search_window, text = "검색")
    button.bind('<Button-1>', search_button)
    button.pack()

    #다크모드 관련
    if self.darkModeOn == True:
        search_window.configure(background='#242424')
        button['bg'] = '#424242'
        button['fg'] = '#ffffff'
    else:
        frame.configure(background='#242424')
        button['bg'] = '#f0f0f0'
        button['fg'] = '#000000'
    search_window.resizable(0,0)

