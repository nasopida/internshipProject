import json

### USER
class User:
    ## INIT
    def __init__(self, id="", pw="", nickname=""):
        self.ID = id
        self.Passwd = pw
        self.nickname = nickname

    ## SETTERS
    def setID(self, id):
        self.ID = id

    def setPasswd(self, pw):
        self.Passwd = pw

    def setNickname(self, nickname):
        self.nickname = nickname

    ## GETTERS
    def getID(self):
        return self.ID

    def getPasswd(self):
        return self.Passwd

    def getNickname(self):
        return self.nickname
    
    ## OTHERS
    def setUseArgs(self, id="", pw="", nickname=""):
        self.ID = id
        self.Passwd = pw
        self.nickname = nickname

    def setUseDict(self, temp):
        self.ID = temp.id
        self.Passwd = temp.pw
        self.nickname = temp.nickname

    def __repr__(self):
        temp = {'id':self.ID,'Passwd':self.Passwd,'nickname':self.nickname}
        return json.dumps(temp)

    def isFull(self):
        if self.ID == "":
            return False
        if self.Passwd == "":
            return False
        if self.nickname == "":
            return False
        return True
