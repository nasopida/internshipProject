from tkinter import *
from tkinter import messagebox

USRCNT = 0
CheckBoxVarList = []

def printDebug(window):
    global CheckBoxVarList
    print(CheckBoxVarList)
    FrameList = window.pack_slaves()
    num = 0
    for Frame in FrameList: 
        for chkButton in Frame.pack_slaves():
            print(str(num) + " : " +chkButton.cget("text")+ " : "+ str(chkButton.cget("variable")) +" :" + str(CheckBoxVarList[num].get()))
            num += 1

# Fundamental Funcs

def addCheckBox(window, userName):
    global CheckBoxVarList, USRCNT
    tempVar = BooleanVar(value=False)
    tempFrame = Frame(window, background="WHITE")
    temp = Checkbutton(tempFrame, variable=tempVar, text=userName, background="WHITE", activebackground="WHITE")
    CheckBoxVarList.append(tempVar)
    tempFrame.pack(side=TOP, fill=X)
    temp.pack(side=LEFT)
    USRCNT += 1
    topLabel["text"] ="유저수 : "+ str(USRCNT) +"\n"
    
def delCheckBox(Frame, index):
    global CheckBoxVarList, USRCNT
    CheckBoxVarList.pop(index)
    Frame.destroy()
    USRCNT -= 1
    topLabel["text"] ="유저수 : "+ str(USRCNT) +"\n"


# Compound Funcs

def delSelectedCheckBox(window):
    global CheckBoxVarList, USRCNT
    if USRCNT == 0:
        return
    if not messagebox.askyesno('Verify', 'Really Delete?'):
        return
    num = 0
    while True:
        if num >= len(CheckBoxVarList):
            break
        if CheckBoxVarList[num].get() == True:
            FrameList = window.pack_slaves()
            delCheckBox(FrameList[num+1], num)
            num -= 1
        num += 1

def addUserDialogue():
    DialogueBox = Toplevel()
    DialogueBox.title("유저 추가")
    DialogueBox.geometry("200x150")

    DialogueBoxcenterFrame = Frame(DialogueBox, background="WHITE")
    DialogueBoxbottomFrame = Frame(DialogueBox, background="WHITE")

    DialogueBoxcenterFrame.pack(fill=BOTH, expand=True)
    DialogueBoxbottomFrame.pack(fill=X, side=BOTTOM)

    userLabel = Label(DialogueBoxcenterFrame, text="유저이름: ", background="WHITE")
    userEntry = Entry(DialogueBoxcenterFrame)
    tempButtonList = [
        Button(DialogueBoxbottomFrame, state=DISABLED, highlightthickness=0, bd=0, background="WHITE"),
        Button(DialogueBoxbottomFrame, state=DISABLED, highlightthickness=0, bd=0, background="WHITE"),
        Button(DialogueBoxbottomFrame, state=DISABLED, highlightthickness=0, bd=0, background="WHITE")
    ]
    okButton = Button(DialogueBoxbottomFrame, text="OK", command=lambda: addCheckBox(centerFrame, userEntry.get().strip()))
    cancelButton = Button(DialogueBoxbottomFrame, text="Cancel", command=lambda: DialogueBox.destroy())

    userLabel.pack(expand=True, fill=X, side=LEFT)
    userEntry.pack(expand=True, fill=X, side=LEFT)
    tempButtonList[0].pack(expand=True, fill=BOTH, side=LEFT)
    okButton.pack(expand=True, fill=BOTH, side=LEFT)
    tempButtonList[1].pack(expand=True, fill=BOTH, side=LEFT)
    cancelButton.pack(expand=True, fill=BOTH, side=LEFT)
    tempButtonList[2].pack(expand=True, fill=BOTH, side=LEFT)


# MAIN

if __name__ == "__main__":

    # MainFrame initialization
    mainScreen = Tk()
    mainScreen.title("유저 관리")
    mainScreen.geometry("400x600")

    mainFrame = Frame(mainScreen)

    # MainFrame Multiplexing
    topFrame = Frame(mainFrame, background="WHITE")
    centerFrame = Frame(mainFrame, background="WHITE")
    bottomFrame = Frame(mainFrame, background="WHITE")
    bottom_topFrame = Frame(bottomFrame)
    bottom_bottomFrame = Frame(bottomFrame)
    topFrame.pack(fill=X, side=TOP)
    mainFrame.pack(fill=BOTH, expand=True)
    centerFrame.pack(fill=BOTH, expand=True)
    bottomFrame.pack(fill=X, side=BOTTOM)
    bottom_topFrame.pack(fill=X, expand=True, side=TOP)
    bottom_bottomFrame.pack(fill=X, expand=True, side=BOTTOM)

    # Frame Updates
    topLabel = Label(topFrame, text="유저수 : 0\n", background="WHITE")
    scroll = Scrollbar(centerFrame)
    KickButton = Button(bottom_topFrame, text="강퇴투표")
    addButton = Button(bottom_bottomFrame, text="추가", command=lambda: addUserDialogue())
    delButton = Button(bottom_bottomFrame, text="삭제", command=lambda: delSelectedCheckBox(centerFrame))
    modButton = Button(bottom_bottomFrame, text="변경")
    topLabel.pack(expand=True)
    scroll.pack(side=RIGHT, fill=Y)
    KickButton.pack(fill=BOTH, expand=True)
    addButton.pack(expand=True, fill=BOTH, side=LEFT)
    delButton.pack(expand=True, fill=BOTH, side=LEFT)
    modButton.pack(expand=True, fill=BOTH, side=LEFT)

    ####
    addCheckBox(centerFrame, "user1")
    addCheckBox(centerFrame, "user2")
    addCheckBox(centerFrame, "user3")
    addCheckBox(centerFrame, "user4")
    addCheckBox(centerFrame, "user5")


    mainScreen.mainloop()

