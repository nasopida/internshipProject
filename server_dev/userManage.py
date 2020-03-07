import sys
from user import User
from fileManage import fileManage

### USERMANAGE
class userManage:
    fileManger = fileManage()

    def __init__(self):
        super().__init__()
        self.userList = []
        self.userCnt = 0

    # add Users in path to userList
    # returns True when Success
    def fetchUsers(self):
        if self.fileManger.isErr():
            print(self.fileManger.getErr(),file=sys.stderr)
            return False

        temp_list = []
        if not self.fileManger.load(temp_list):
            print(self.fileManger.getErr(),file=sys.stderr)
            return False

        for temp_user in temp_list:
            user = User()
            user.setUseDict(temp_user)
            self.userList.append(user)
            self.userCnt += 1
        return True
    
    # add given User to userList
    def addUser(self, user):
        if user.isFull():
            self.userCnt += 1
            self.userList.append(user)

    def getUser(self, temp_ID, temp_pass):
        for user in self.userList:
            if user.getID() == temp_ID:
                if user.getPasswd() == temp_pass:
                    return user
        return None

    # sets path
    # returns True when Success
    def setUserFile(self, path):
        if not self.fileManger.setPath(path):
            print(self.fileManger.getErr(), file=sys.stderr)
            return False
        return True

    # saves at path
    # returns True when Success
    def saveUserFile(self):
        if self.fileManger.isErr():
            print(self.fileManger.getErr(),file=sys.stderr)
            return False
        
        if not self.fileManger.save(self.userList):
            print(self.fileManger.getErr(),file=sys.stderr)
            return False
        return True

    def isUser(self, temp_ID, temp_pass):
        for user in self.userList:
            if user.getID() == temp_ID:
                if user.getPasswd() == temp_pass:
                    return True
        return False
    
    def printUserList(self):
        print('UserCnt: ' + str(self.userCnt))
        # if len(self.userList) == 0:
        #     return
        print('[')
        for user in self.userList:
            print(str(user))
        print(']')
    
    def getUserCnt(self):
        return self.userCnt

if __name__ == "__main__":
    manager = userManage()
    if not manager.setUserFile('../login.config'):
        print('userManage: setUserFile() error')
    if not manager.fetchUsers():
        print('userManage: fetchUsers() error')
    manager.printUserList()
    a = User('aID', 'aPass', 'aNick')
    b = User('bID', 'bPass', 'bNick')
    manager.addUser(a)
    manager.addUser(b)
    manager.printUserList()
    
    if not manager.saveUserFile():
        print('userManage: saveUserFile() error')