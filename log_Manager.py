import logger
import time
import os

class log_Manager:
    def __init__(self, folder = "./Logs"):
        self.__folder = folder # 파일 저장될 폴더 위치
        self.__file = time.strftime('%Y_%m_%d', time.localtime(time.time())) # 현재 파일 이름 (현재 날짜)
        self.__absfp = self.__folder + self.__file
        self.__logger = logger.logger(self.__absfp)

    def addLog(self, temp):
        # 현재 파일에 temp 추가
        self.__logger.addLog(temp)
        pass

    def changeTime(self):
        # 파일 명 변환
        if self.__logger != None:
            self.__logger.record()

        self.__file = time.strftime('%Y_%m_%d', time.localtime(time.time())) # 현재 파일 이름 (현재 날짜)
        self.__absfp = self.__folder + self.__file
        self.__logger = logger.logger(self.__absfp)

        if os.path.isfile(self.__absfp):
            self.__logger.read()

    def record(self):
        # 파일에 저장
        self.__logger.record()

    def read(self):
        # 파일을 읽어옴
        self.__logger.read()

    def list(self):
        # 파일 명을 읽어서 리스트로 반환
        return os.listdir(self.__folder)

    def get(self, temp):
        logs = []
        if type(temp) == type(list):
            # 파일 명들이 들어왔을때
            # 각 파일을 읽어서 로그로 변환
            # 로그들을 리스트로 저장후 리스트를 반환
            for name in temp:
                t = logger.packetLogger(self.__absfp+name)
                t.read()
                logs.append(t.getLogList)
        elif type(temp) == type(str):
            # 파일 명이 들어왔을때
            # 해당 파일을 읽어서 로그로 변환
            # 로그를 리스트로 저장후 리스트 반환
            t = logger.packetLogger(self.__absfp+temp)
            t.read()
            logs.append(t.getLogList)
        return logs
