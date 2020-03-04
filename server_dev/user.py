# user.py 
#     setter 추가했습니다.
#     setUseDict함수로 dictionary형을 user로 변환 가능합니다.
#     setUseArgs함수로 init처럼 사용할수 있습니다.
#     repr함수로 dict를 받아올수 있습니다.
#     str함수를 추가했습니다. 이제 출력시에 dict 형태로 출력이 됩니다.
#     isFull메소드는 ID, PASSWD, NICKNAME이 있을시에 True를 반환합니다.

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
        self.ID = temp['id']
        self.Passwd = temp['Passwd']
        self.nickname = temp['nickname']

    def __repr__(self):
        temp = {'id':self.ID,'Passwd':self.Passwd,'nickname':self.nickname}
        return temp
    
    def __str__(self):
        return str(self.__repr__())

    def isFull(self):
        if self.ID == "":
            return False
        if self.Passwd == "":
            return False
        if self.nickname == "":
            return False
        return True
