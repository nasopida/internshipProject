import socket
import argparse
import threading
import random
from datetime import datetime
from logger import msgLog, msgLogger

port = 57270
host = "127.0.0.1"

def dice():
    return str(random.randint(1,6))

def handle_receive(client_socket, user):
    global clnt_logger
    while 1:
        try:
            data = client_socket.recv(1024)
        except:
            print("연결 끊김")
            clnt_logger.addLog(msgLog("program", "연결 끊김".encode('utf-8')))
            break
        data = data.decode('utf-8')
        if not user in data: # 자신이 아닐때 출력
            clnt_logger.addLog(msgLog("program", data))
            print(data)

def handle_send(client_socket):
    global clnt_logger
    f = open('chatLog.txt', mode='at', encoding='utf-8')
    lines=[]
    while 1:
        try:
            data=input(user+": ")
            client_socket.send(data.encode('utf-8'))
            
            if data == "/quit":
                clnt_logger.addLog(msgLog("program", data))
                break
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
            clnt_logger.addLog(msgLog("program", data))
            clnt_logger.record()

            #검색은 미완성
            if data=="/search":
                text=f.read()
                lines=text.split(';')
                print("찾을 채팅내용을 입력하십쇼: ",end='')
                find=input()
                for i in lines:
                    if find in lines:
                        print(i)
                    else:
                        pass

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
                

    client_socket.close()
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

    clnt_logger = msgLogger()
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

    send_thread = threading.Thread(target=handle_send, args=(client_socket,))
    send_thread.daemon = True
    send_thread.start()

    receive_thread.join()
    send_thread.join()
