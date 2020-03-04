# fileManage.py
#     setPath메소드로 경로 설정가능합니다. 경로에 이상이 없을경우 True를 반환합니다.
#     load메소드로 설정된 경로의 각줄(json)을 dict로 변환하여 주어진 list에 추가합니다. 이상이 없을 경우 True를 반환합니다.
#     save메소드로 설정된 경로에 주어진 list의 각 노드들의 repr를 json으로 dump시킵니다. 이상이 없을 경우 True를 반환합니다.
#     위 함수들에서 이상이 있었을 경우에 isErr메소드는 True를 반환합니다.
#     에러 메세지를 보고 싶은경우 getErr메소드를 출력하면 됩니다.


import sys
import os
import json
import traceback

class fileManage:
    def __init__(self):
        super().__init__()
        self.__path = ""
        self.__error = "fileManager: path not set."

    def isErr(self):
        if self.__error != None:
            return True
        return False
    
    def getErr(self):
        return self.__error

    def setPath(self, path):
        if not os.path.exists(path):
            try:
                f = open(path, 'w')
            except IOError:
                self.__error = "fileManager: path is not accessible."
                return False
            except Exception:
                self.__error = traceback.format_exc()
                return False
            self.__path = path
            self.__error = None
            return True
        if not os.path.isfile(path):
            self.__error = "fileManager: path is not a file."
            return False
        self.__path = path
        self.__error = None
        return True
        
    # saves list to path
    def save(self, list):
        if self.__error != None:
            return False
        
        try:
            with open(self.__path, 'w') as f:
                for item in list:
                    f.write(json.dumps(item.__repr__())+'\n')
        except Exception:
            self.__error = traceback.format_exc()
            return False
        
        self.__error = None
        return True
        
    def load(self, list):
        if self.__error != None:
            return False
        
        try:
            with open(self.__path, 'r') as f:
                temp_list = f.readlines()
                for temp_node in temp_list:
                    list.append(json.loads(temp_node))
                print(temp_list)
                print(list)
        except Exception:
                self.__error = traceback.format_exc()
                return False 
        return True
    
