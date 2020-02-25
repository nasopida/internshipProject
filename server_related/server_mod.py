import select
import socket
import sys
import queue

##################################
# Debug opt
DEBUG = True

# Client Dict
# Clients = {}

# Users Count
USRCNT = 0

##################################

def NewConnection():
    pass

def CloseConnection():
    pass

def DEBUG(message):
    global DEBUG
    if DEBUG:
        print(message, file=sys.stderr)

def host(address, timeout=60):
    global USRCNT
    
    listSock = []
    
    # Create TCP/IP Socket
    socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_listen.setblocking(0)

    # Bind the socket to the port
    DEBUG("starting up on {} port {}".format(address[0], address[1]))
    socket_listen.bind(address)
    socket_listen.listen(10)
    
    listSock.append(socket_listen)

    while listSock:
        # Wait for at least one of the sockets to be ready for processing
        DEBUG("\nwaiting for the next event")
        readable, writable, exceptional = select.select(listSock, [], [], timeout)

        # Handle inputs
        for s in readable:
            if s is socket_listen:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                connection.setblocking(0)
                DEBUG("new connection from " + str(client_address))

                USRCNT += 1

                listSock.append(connection)

            else:
                try:
                    data = s.recv(1024)
                except ConnectionResetError:
                    DEBUG("closing "+ str(client_address) +" ConnectionResetError...")
                    
                    # Stop listening for input on the connection
                    listSock.remove(s)
                    s.close()
                    
                    break

                if data:
                    # A readable client socket has data
                    DEBUG("{} : {}".format(str(s.getpeername()), data.decode('utf-8')))
                else:
                    # Interpret empty result as closed connection
                    DEBUG("closing "+ str(client_address) +"after reading no data")
                    
                    # Stop listening for input on the connection
                    listSock.remove(s)
                    s.close()

if __name__ == "__main__":
    address = ("127.0.0.1", 57270)
    timeout = 60

    host(address, timeout)