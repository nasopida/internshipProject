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
import packet

clnt_logger = msgLogger()
port = 57270
host = "127.0.0.1"
user_list = {}
server_chat = {}
command_list = {"/quit", "/whoami", "/whattime", "/whatdate", "/dice", "/search"}

def dice():
    return str(random.randint(1,6))

def handle_receive(client_socket, user, Chat = None):
    global clnt_logger
    global user_list
    while 1:
        try:
            data = client_socket.recv(1024)
        except:
            print("연결 끊김")
            clnt_logger.addLog(msgLog("program", "연결 끊김"))
            break
        data = data.decode('utf-8')
        if not user in data: # 자신이 아닐때 출력
            clnt_logger.addLog(msgLog("program", data))
            print(data)
        server_chat[data] = client_socket

def handle_send(client_socket, user, data = None):
    global clnt_logger
    #f = open('./log/chatLog.txt', mode='at', encoding='utf-8')
    lines=[]
    try:
        if data == None:
            data=input(user+": ")
            print(name)
            client_socket.send(data.encode('utf-8'))

        #간단한 명령어기능
        if data not in command_list:
            client_socket.send(packet.msgPacket(data).encode())
        else:
            client_socket.send(packet.cmdPacket(data).encode())
       # clnt_logger.addLog(msgLog("program", data))
       # clnt_logger.record()

    except EOFError:
        print('EOF Error!')
        client_socket.close()
        clnt_logger.record()
        #f.close()
    except KeyboardInterrupt:
        print('KeyboardInterrupt Error')
        client_socket.close()
        clnt_logger.record()
        #f.close()
    data = None
                

    #client_socket.close()
    #f.close()


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
