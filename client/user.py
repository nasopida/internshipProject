class User:
    def __init__(self, id, pw, nickname):
        self.ID = id
        self.Passwd = pw
        self.nickname = nickname

    def getID(self):
        return self.ID

    def getPasswd(self):
        return self.Passwd

    def getNickname(self):
        return self.nickname