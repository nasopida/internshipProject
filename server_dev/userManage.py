import sys
import os
import json

### USERMANAGE
class userManage:
    def __init__(self):
        super().__init__()
        self.__path = ""
        self.userList = []
        self.userCnt = 0

    # add Users in path to userList
    # returns True when Sucess
    def fetchUsers(self):
        if self.__path == "":
            return False

        if os.path.isfile(self.__path):
            
            try:
                with open(self.__path, 'r') as f:
                    user_log_list = f.readlines()
                    for log in user_log_list:
                        self.userCnt += 1
                        self.userList.append(User.sets(json.loads(log)))
            except Exception:
                print(Exception)
                return False
        return True
    
    # add given User to userList
    def addUser(self, user):
        if user.isFull():
            self.userCnt += 1
            self.userList.append(user)

    # sets path
    # returns True when Sucess
    def setUserFile(self, path):
        if os.path.isfile(self.__path):
            self.__path = path
            return True
        return False

    # saves at path
    # returns True when Sucess
    def saveUserFile(self):
        if self.__path == "":
            return False

        if os.path.isfile(self.__path):
            try:
                with open(self.__path, 'w') as f:
                    for user in self.userList:
                        f.writelines(user)
            except Exception:
                print(Exception)
                return False
        return True


if __name__ == "__main__":
    manager = userManage()
    a = User('aID', 'aPass', 'aNick')
    manager.addUser(a)
    print(a)
    pass