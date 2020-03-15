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
        self.DEBUG("connecting on {} port {}".format(self.address[0], self.address[1]))
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
        try:
            parsed_packet = self.input.get_nowait()
        except queue.Empty:
            return None
        return parsed_packet

    # returns number of packets left in queue
    def get_recv_queue_num(self):
        return self.input.len()

    def start(self):
        self.create()
        self.connect()
        if self.connection == None:
            self.connection = Process(target=self.__start, args=(self.address, 60))
            try:
                self.connection.start()
                self.DEBUG("connection to server successfully established...")
            except Exception:
                
                self.DEBUG("connection not established...")

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
            self.DEBUG("\nwaiting for the next event")
            readable, writable, exceptional = select.select(readSockList, writeSockList, readSockList, timeout)

            # Handle "exceptional conditions"
            for s in exceptional:
                self.DEBUG("handling exceptional condition for" + s.getpeername())
                # Stop listening for input on the connection
                if not self.reconnect:
                    self.disconnect()

            # Handle outputs
            self.DEBUG("\nHandle outputs------")
            for s in writable:
                try:
                    next_msg = self.output.get_nowait()
                except queue.Empty:
                    # No messages waiting so stop checking for writability.
                    # DEBUG("output queue for "+Clients[s]+" is empty")
                    continue
                else:
                    self.DEBUG("writing message to server")
                    self.DEBUG("message :" + str(next_msg))
                    s.send(next_msg.encode())

            # Handle inputs
            self.DEBUG("\nHandle inputs------")
            for s in readable:
                try:
                    data = s.recv(1024)
                # 이곳에 유저가 나간 것을 처리
                except ConnectionResetError:
                    self.DEBUG("ConnectionResetError!!")
                    break

                if data:
                    # A readable client socket has data
                    self.DEBUG("{} : {}".format(str(s.getpeername()), data.decode('utf-8')))

                    try:
                        parsed = packet.toPacket(data.decode('utf-8'))
                    except Exception as err:
                        self.DEBUG("Exception: {}".format(err))
                        print("NOT PACKET!!! -- client err")
                        continue

                    self.input.put(parsed)

                else:
                    # Interpret empty result as closed connection
                    if not self.reconnect:
                        self.disconnect()