import os
import json
import time
from datetime import datetime


# 메세지 로그를 파일에 저장하거나 읽어온다.
# 
class msgLogger:
    def __init__(self, fp = "logFile.txt", logList = []):
        super().__init__()
        self.__fp = fp
        self.__logList = logList

    # 저장하거나 읽어올 파일을 설정한다
    def setFile(self, fp):
        self.__fp = fp

    # 파일에 로그를 전부 저장한다
    def record(self):
        with open(self.__fp, "w") as file:
            file.write(self.__repr__())

    # 파일에 저장된 로그를 전부 읽어온다.
    def read(self):
        if not os.path.isfile(self.__fp):
            return
        with open(self.__fp, "r") as file:
            self.__logList = file.readlines()
        self.__logList = list(map(msgLog.toLog, map(str.rstrip, self.__logList)))

    # 메세지 로그를 추가한다.
    def addLog(self, msgLog):
        self.__logList.append(msgLog)

    def getLogList(self):
        return self.__logList

    def __repr__(self):
        tempStr = map(repr, self.__logList)
        return '\n'.join(tempStr)
    
    def __str__(self):
        tempStr = map(str, self.__logList)
        return '\n'.join(tempStr)

class msgLog:
    def __init__(self, userName = "<empty>", msg = "<empty>", timestamp = time.time()):
        super().__init__()
        self.__user = userName
        self.__time = timestamp
        self.__msg = msg

    #### needs exception handler
    @classmethod
    def toLog(cls, string):
        firstclosingSuareBracketIndex = string.find(']')
        secondOpeningSquareBracketIndex = string.find('[', firstclosingSuareBracketIndex)
        secondClosingSquareBracketIndex = string.find(']', secondOpeningSquareBracketIndex)
        userName = string[1:firstclosingSuareBracketIndex]
        timestamp = float(string[secondOpeningSquareBracketIndex+1: secondClosingSquareBracketIndex])
        msg = string[secondClosingSquareBracketIndex+1:].lstrip()
        return cls(userName, msg, timestamp)


    def setTime(self, timestamp):
        self.__time = timestamp

    def getTime(self):
        return str(self.__time)

    def setUserName(self, userName):
        self.____user = userName
    
    def getUserName(self):
        return self.____user

    def setMsg(self, message):
        self.__msg = message

    def getMsg(self):
        return self.__msg

    def __repr__(self):
        name = "["+self.__user+"]"
        time = "["+str(self.__time)+"]"
        content = self.__msg
        return name + " " + time + " " + content

    def __str__(self):
        name = "["+self.__user+"]"
        time = "["+str(datetime.fromtimestamp(self.__time).strftime('%H:%M'))+"]"
        content = self.__msg
        return name + " " + time + " " + content

if __name__ == "__main__":
    logger = msgLogger()
    logger.read()
    testLog1 = msgLog("user1", "test message1")
    testLog2 = msgLog("user2", "test message2")
    testLog3 = msgLog("user3", "test message3")

    logger.addLog(testLog1)
    logger.addLog(testLog2)
    logger.addLog(testLog3)

    print(logger)
    logger.record()
