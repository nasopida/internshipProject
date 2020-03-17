import os
import json
import time
import packet
from datetime import date


# 메세지 로그를 파일에 저장하거나 읽어온다.
# 
class packetLogger:
    def __init__(self, fp = None, logList = []):
        self.__fp = fp
        self.__logList = logList

    # 저장하거나 읽어올 파일을 설정한다
    def setPath(self, fp):
        self.__fp = fp

    # 파일에 로그를 전부 저장한다
    def record(self):
        if self.__fp == None:
            return

        with open(self.__fp, "w") as file:
            for temp in self.__logList:
                file.write(temp)

    # 파일에 저장된 로그를 전부 읽어온다.
    def read(self):
        if self.__fp == None:
            return

        if not os.path.isfile(self.__fp):
            return

        with open(self.__fp, "r") as file:
            self.__logList = file.readlines()

        self.__logList = list(map(packet.toPacket, map(str.rstrip, self.__logList)))

    # 메세지 로그를 추가한다.
    def addLog(self, temp):
        self.__logList.append(temp)

    def getLogList(self):
        return self.__logList

    def __repr__(self):
        tempStr = map(repr, self.__logList)
        return '\n'.join(tempStr)
    
    def __str__(self):
        tempStr = map(str, self.__logList)
        return '\n'.join(tempStr)

if __name__ == "__main__":
    logger = packetLogger()
    # logger.read()
    reg1 = packet.registerPacket("user", "pass", "nickname")
    log1 = packet.loginPacket("user", "pass")
    alt1 = packet.alterPacket("user", "pass", "nickname")
    msg1 = packet.msgPacket("Hi! How are you?")
    cmd1 = packet.cmdPacket("/whoami")

    logger.addLog(reg1)
    logger.addLog(log1)
    logger.addLog(alt1)
    logger.addLog(msg1)
    logger.addLog(cmd1)

    print(logger)
    # logger.record()
