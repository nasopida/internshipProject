#-*-coding: utf-8

import select
import socket
import os
import sys
from multiprocessing import Process
import queue

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import packet

class conn_manage:

    def DEBUG(self, message):
        if self.debug:
            print(message, file=sys.stderr)

    def __init__(self, address, debug=False):
        self.debug = debug
        self.client_socket = None
        self.address = address
        self.input = queue.Queue()
        self.output = queue.Queue()
        self.connection = None

    def create(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        DEBUG("connecting on {} port {}".format(address[0], address[1]))
        try:
            self.client_socket.connect(self.address)
        except Exception:
            return False
        return True

    def reconnect(self):
        for i in range(5):
            if self.connect():
                return True
        return False

    def disconnect(self):
        self.client_socket.close()

    # sends packet
    def send(self, message):
        self.output.put(message.encode())

    # returns recieved packet
    def recv(self):
        # return message
        try:
            parsed_packet = self.input.get_nowait()
        except queue.Empty:
            return None
        return parsed_packet

    def start(self):
        self.create()
        self.connect()
        if self.connection == None:
            self.connection = Process(target=self.__start, args=(self.address,))
        self.DEBUG("connection to server successfully established...")

    def stop(self):
        if self.connection != None:
            self.connection.kill()
        self.DEBUG("connection to server successfully stopped...")

    def __start(self, timeout=60):
        readSockList = []
        writeSockList = []
        
        writeSockList.append(client_socket)

        while writeSockList:
            # Wait for at least one of the sockets to be ready for processing
            DEBUG("\nwaiting for the next event")
            readable, writable, exceptional = select.select(readSockList, writeSockList, readSockList, timeout)

            # Handle "exceptional conditions"
            for s in exceptional:
                DEBUG("handling exceptional condition for" + s.getpeername())
                # Stop listening for input on the connection
                if not self.reconnect:
                    self.disconnect()

            # Handle outputs
            DEBUG("\nHandle outputs------")
            for s in writable:
                try:
                    next_msg = self.output.get_nowait()
                except queue.Empty:
                    # No messages waiting so stop checking for writability.
                    # DEBUG("output queue for "+Clients[s]+" is empty")
                    continue
                else:
                    DEBUG("writing message to server")
                    DEBUG("message :" + str(next_msg))
                    s.send(next_msg.encode())

            # Handle inputs
            DEBUG("\nHandle inputs------")
            for s in readable:
                try:
                    data = s.recv(1024)
                # 이곳에 유저가 나간 것을 처리
                except ConnectionResetError:
                    DEBUG("ConnectionResetError!!")
                    break

                if data:
                    # A readable client socket has data
                    DEBUG("{} : {}".format(str(s.getpeername()), data.decode('utf-8')))

                    try:
                        parsed = packet.toPacket(data.decode('utf-8'))
                    except Exception as err:
                        DEBUG("Exception: {}".format(err))
                        print("NOT PACKET!!! -- client err")
                        continue

                    self.input.put(parsed)

                else:
                    # Interpret empty result as closed connection
                    if not self.reconnect:
                        self.disconnect()