import select
import socket
import sys
import queue

class HostServer:
    def __init__(self, IPaddr, port, timeout=60, DEBUG = False):
        self.__address = (IPaddr, port)
        self.__DEBUG = DEBUG
        self.__timeout = timeout
        self.inputs = []
        self.outputs = []
        self.message_queues = {}

    def DEBUG(self, message):
        if self.__DEBUG:
            print(message, file=sys.stderr)

    def initialize(self):
        # Create TCP/IP Socket
        self.socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_listen.setblocking(0)

        # Bind the socket to the port
        self.DEBUG("starting up on {} port {}".format(self.__address[0], self.__address[1]))
        self.socket_listen.bind(self.__address)
        self.socket_listen.listen(10)

        # Sockets from which we expect to read
        self.inputs.append(self.socket_listen)


    def host(self):
        while self.inputs:
            # Wait for at least one of the sockets to be ready for processing
            self.DEBUG("\nwaiting for the next event")
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, self.__timeout)
            # Handle "exceptional conditions"
            for s in exceptional:
                self.DEBUG("handling exceptional condition for" + s.getpeername())
                # Stop listening for input on the connection
                self.inputs.remove(s)
                if s in self.outputs:
                    self.outputs.remove(s)
                s.close()

                # Remove message queue
                del self.message_queues[s]

            # Handle inputs
            for s in readable:
                if s is self.socket_listen:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    self.DEBUG("new connection from" + str(client_address))
                    connection.setblocking(0)
                    self.inputs.append(connection)

                    # Give the connection a queue for data we want to send
                    self.message_queues[connection] = queue.Queue()
                else:
                    try:
                        data = s.recv(1024)
                    except ConnectionResetError:
                        self.DEBUG("closing "+ str(client_address) +" ConnectionResetError...")
                        self.DEBUG("{} : {}".format(str(s.getpeername()), data.decode('utf-8')))
                        # Stop listening for input on the connection
                        if s in writable:
                            writable.remove(s)
                        if s in self.outputs:
                            self.outputs.remove(s)
                        self.inputs.remove(s)
                        s.close()

                        # Remove message queue
                        del self.message_queues[s]
                        break

                    if data:
                        # A readable client socket has data
                        self.message_queues[s].put(data.decode('utf-8'))
                        self.DEBUG("{} : {}".format(str(s.getpeername()), data.decode('utf-8')))
                        # Add output channel for response
                        if s not in self.outputs:
                            self.outputs.append(s)
                    else:
                        # Interpret empty result as closed connection
                        self.DEBUG("closing "+ str(client_address) +"after reading no data")
                        # Stop listening for input on the connection
                        if s in self.outputs:
                            self.outputs.remove(s)
                        self.inputs.remove(s)
                        s.close()

                        # Remove message queue
                        del self.message_queues[s]

            # Handle outputs
            for s in writable:
                try:
                    next_msg = self.message_queues[s].get_nowait()
                except queue.Empty:
                    # No messages waiting so stop checking for writability.
                    self.DEBUG("output queue for "+str(s.getpeername())+"is empty")
                    self.outputs.remove(s)
                else:
                    self.DEBUG("'{}' -> {}".format(next_msg, str(s.getpeername())))
                    s.send(next_msg.encode('utf-8'))
                    

if __name__ == "__main__":
    server = HostServer("127.0.0.1", 57270, True)
    server.host()