from tkinter import *
import login

class SignUpResult:
    def closeButton(self, event=None):
        print("hi")
        self.myParent.destroy()
    
    def __init__(self, window, resultText):
        self.myParent = window
        
        printLabel = Label(self.myParent,text=resultText,font=("맑은 고딕",20))
        printLabel.pack()
        printLabel.focus_set()
        exitBtn = Button(self.myParent, text="확인", command=lambda:self.closeButton())
        exitBtn.pack()
        login.centerWindow(window, 200, 100)
        self.myParent.bind('<Return>',lambda x :self.closeButton())
        exitBtn.pack()

