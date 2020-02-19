import socket
import argparse
import threading
import random
from datetime import datetime
from logger import msgLog, msgLogger
from tkinter import *
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

clnt_logger = msgLogger()
port = 57270
host = "127.0.0.1"
user_list = {}
server_chat = {}

def dice():
    return str(random.randint(1,6))

def handle_receive(client_socket, user, Chat = None):
    global clnt_logger
    global user_list
    user_name=client_socket.recv(1024).decode('utf-8')
    while user_name != "---- %s님이 들어오셨습니다. ----"%user:
        user_list[user_name] = client_socket
        client_socket.send('y'.encode('utf-8'))
        user_name = client_socket.recv(1024).decode('utf-8')
    while 1:
        try:
            data = client_socket.recv(1024)
        except:
            print("연결 끊김")
            clnt_logger.addLog(msgLog("program", "연결 끊김"))
            break
        data = data.decode('utf-8')
        if data == "/userin":
            data = client_socket.recv(1024).decode('utf-8')
            if data != user:
                user_list[data] = client_socket
            continue
        if data == "/userout":
            data = client_socket.recv(1024).decode('utf-8')
            del user_list[data]
            continue
        if not user in data: # 자신이 아닐때 출력
            clnt_logger.addLog(msgLog("program", data))
            print(data)
        server_chat[data] = client_socket

def handle_send(client_socket, user, data = None):
    global clnt_logger
    f = open('../log/chatLog.txt', mode='at', encoding='utf-8')
    lines=[]
    try:
        if data == None:
            data=input(user+": ")
            print(name)
            client_socket.send(data.encode('utf-8'))

        #간단한 명령어기능
        if data == "/quit":
            clnt_logger.addLog(msgLog("program", data))
            client_socket.send(data.encode('utf-8'))
            client_socket.close()
            #break
        if data!="/whoami" and data!="/whattime" and data!="/whatdate" and data!="/dice" and data!="/search":
            client_socket.send(data.encode('utf-8'))
        if data == "/whoami":
            print(user+"입니다")
        if data == "/whattime":
            now=datetime.now()
            print("%s시 %s분 %s초입니다."%(now.hour,now.minute,now.second))
        if data == "/whatdate":
            now=datetime.now()
            print("%s년 %s월 %s일입니다."%(now.year,now.month,now.day))
        if data == "/dice":
            randString = dice()
            print(randString)
       # clnt_logger.addLog(msgLog("program", data))
       # clnt_logger.record()

        """#검색기능
        if data=="/search":
            #f = open('chatLog.txt', mode='r', encoding='utf-8')
            read = f.read()
            split = read.split(';')
            print("찾을 채팅내용을 입력하십쇼: ",end='')
            find=input()
            line=1
            for i in split:
                if i == find:
                    print('%d.%s'%(line,i))
                else:
                    pass
                line=line+1"""
        if data=="/user":
            for name in user_list:
                print(name)

    except EOFError:
        print('EOF Error!')
        client_socket.close()
        clnt_logger.record()
        f.close()
    except KeyboardInterrupt:
        print('KeyboardInterrupt Error')
        client_socket.close()
        clnt_logger.record()
        f.close()
    data = None
                

    #client_socket.close()
    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="\nclient\n-p port\n-i host\n-s string")
    parser.add_argument('-p', help="port")
    parser.add_argument('-i', help="host")
    parser.add_argument('-u', help="user", required=True)

    args = parser.parse_args()
    
    user = str(args.u)
    try:
        port = int(args.p)
        host = args.i
    except:
        pass

    clnt_logger.setFile(user+"LogFile.txt")
    clnt_logger.read()

    #IPv4 체계, TCP 타입 소켓 객체를 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 지정한 host와 prot를 통해 서버에 접속합니다.
    client_socket.connect((host, port))

    client_socket.send(user.encode('utf-8'))

    receive_thread = threading.Thread(target=handle_receive, args=(client_socket, user))
    receive_thread.daemon = True
    receive_thread.start()

    send_thread = threading.Thread(target=handle_send, args=(client_socket, user))
    send_thread.daemon = True
    send_thread.start()

    receive_thread.join()
    send_thread.join()
