import socket
import argparse
import threading
import time
from logger import msgLog, msgLogger
from tkinter import *
import time

def window():
    chat_num = Tk()
    def change():
        num.config(text="인원 : %d/ %d"%(len(user_list), max_user))
    num = Button(chat_num, text="인원 : %d/ %d"%(len(user_list), max_user), command=change)
    num.grid(row=0, column=0)
    def num_change(event):
        num.config(text="인원 : %d/ %d"%(len(user_list), max_user))
    num.config(text="인원 : %d/ %d"%(len(user_list), max_user))
    num.bind('<Button-1>', num_change)
    num.mainloop()

host = "127.0.0.1"
port = 57270
user_list = {}
notice_flag = 0
max_user = 100
serv_logger = msgLogger()

# 메세지 펑션 -> 메세지를 서버에 출력해주고 클라이언트에게 메세지를 보내준다.
# 메세지가 가지 않을 경우 소켓이 비정상적 종료가 된 것 
def msg_func(msg):
    print(msg)
    for con in user_list.values():
        try:
            con.send(msg.encode('utf-8'))
        except:
            print("연결이 비 정상적으로 종료된 소켓 발견")

# 클라이언트가 접속하였을 떄 공지를 보내준다.
def notice():
    # 전역 변수를 지역 변수에서 사용할 떄 global 키워드 사용
    global max_user
    global user_list
    msg = "인원 : %d"%len(user_list)
    msg += " / %d"%max_user
    msg += "\n매너있는 채팅을 합시다!\n"
    msg += "채팅방 나가기 : /quit\n"
    msg += "명령어 보기 : /help\n"
    return msg
# 
def handle_receive(client_socket, addr, user):
    global serv_logger
    msg = "---- %s님이 들어오셨습니다. ----"%user
    serv_logger.addLog(msgLog("server", msg))
    # 접속한 사람에게 보내는 메세지
    # client_socket.send(notice().encode('utf-8'))
    msg_func(msg)
    print("msgDONE")
    # 메세지를 입력받는지 계속 체크해주면서 quit가 입력되면 탈출, 아니면 msg_func로 메세지 출력
    while 1:
        try:
            data = client_socket.recv(1024)
            string = data.decode('utf-8')
            if "/quit" in string:
                msg = "---- %s님이 나가셨습니다. ----"%user
                serv_logger.addLog(msgLog("server", msg))
                serv_logger.record()
                #유저 목록에서 방금 종료한 유저의 정보를 삭제
                del user_list[user]
                msg_func("인원 : %d"%len(user_list))
                msg_func(msg)
                break
            string = "%s : %s"%(user, string)
            serv_logger.addLog(msgLog(user, string))
            serv_logger.record()
            msg_func(string)
        # 강제 종료시 대응하는 예외처리
        except ConnectionResetError:
            msg = "---- %s님이 나가셨습니다. ----"%user
            serv_logger.addLog(msgLog("server", msg))
            serv_logger.record()
            #유저 목록에서 방금 종료한 유저의 정보를 삭제
            del user_list[user]
            msg_func("인원 : %d"%len(user_list))
            msg_func(msg)
            break
    client_socket.close()
    serv_logger.record()

def handle_notice(client_socket, addr, user):
    pass

def accept_func():
    global serv_logger
    #IPv4 체계, TCP 타입 소켓 객체를 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #포트를 사용 중 일때 에러를 해결하기 위한 구문
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #ip주소와 port번호를 함께 socket에 바인드 한다.
    #포트의 범위는 1-65535 사이의 숫자를 사용할 수 있다.
    server_socket.bind((host, port))

    #서버가 최대 5개의 클라이언트의 접속을 허용한다.
    server_socket.listen(max_user)
    chatnum_thread = threading.Thread(target=window, args=())
    chatnum_thread.daemon = True
    chatnum_thread.start()
    while 1:        
        try:
            #클라이언트 함수가 접속하면 새로운 소켓을 반환한다.
            client_socket, addr = server_socket.accept()    
        except KeyboardInterrupt:
            for user, con in user_list:
                con.close()
            server_socket.close()
            print("Keyboard interrupt")
            break
        user = client_socket.recv(1024).decode('utf-8')
        user_list[user] = client_socket

        #로그를 보내준다
        #serv_logger.read()
        # user_list[user].send(str(serv_logger).encode()) #로그를 보내줘야 한다.


        #accept()함수로 입력만 받아주고 이후 알고리즘은 핸들러에게 맡긴다.
        notice_thread = threading.Thread(target=handle_notice, args=(client_socket, addr, user))
        notice_thread.daemon = True
        notice_thread.start()

        receive_thread = threading.Thread(target=handle_receive, args=(client_socket, addr,user))
        receive_thread.daemon = True
        receive_thread.start()
        

if __name__ == '__main__':
    #parser와 관련된 메서드 정리된 블로그 : https://docs.python.org/ko/3/library/argparse.html
    #description - 인자 도움말 전에 표시할 텍스트 (기본값: none)
    #help - 인자가 하는 일에 대한 간단한 설명.
    parser = argparse.ArgumentParser(description="\nJoo's server\n-p port\n")
    parser.add_argument('-p', help="port")

    args = parser.parse_args()
    try:
        port = int(args.p)
    except:
        pass
    accept_func()

"""
#쓰레드에서 실행되는 코드
#접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 한다.
def threaded(client_socket, addr):
    print("Connected by : ",addr[0],':',addr[1])

    #클라이언트가 접속을 끊을 때 까지 반복한다.
    while True:
        try:
            #데이터가 수신되면 클라이언트에 다시 전송
            data = client_socket.recv(1024)

            #데이터가 없을 경우 연결이 끊김이다.
            if not data:
                print('Disconnected by ' + addr[0],':',addr[1])
                break
            
            # 클라이언트로부터 받은 메세지를 decode해준다.
            print('Received from' + addr[0],':',addr[1],data.decode())
            
            client_socket.send(data)
        # 예외처리로 Connect가 강제로 끊겼을 떄 처리
        except ConnectionRefusedError as e:
            print('Disconnected by ' + addr[0],':',addr[1])
            break

    client_socket.close()

HOST = '127.0.0.1'
PORT = 57270

# 소켓 연결 socket/bind/listen, setsockopt는 오류방지
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind((HOST,PORT))
server_socket.listen()

print('server start')

#클라이언트가 접속하면 accept함수가 새로운 소켓을 생성한다.
while True:
    print('wait')

    # 클라이언트와 주소를 accept하고 새 쓰레드에 넘겨준다.
    client_socket, addr = server_socket.accept()
    start_new_thread(threaded,(client_socket,addr))

server.socket.close()
"""
