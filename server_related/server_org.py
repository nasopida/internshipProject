import select
import socket
import sys
import queue

##################################
# Debug opt
DEBUG = True
##################################

def DEBUG(message):
    global DEBUG
    if DEBUG:
        print(message, file=sys.stderr)

def host(address, timeout=60):
    inputs = []
    outputs = []
    # message_queues = {}
    
    # Create TCP/IP Socket
    socket_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_listen.setblocking(0)

    # Bind the socket to the port
    DEBUG("starting up on {} port {}".format(address[0], address[1]))
    socket_listen.bind(address)
    socket_listen.listen(10)
    
    inputs.append(socket_listen)

    while inputs:
        # Wait for at least one of the sockets to be ready for processing
        DEBUG("\nwaiting for the next event")
        readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

        # Handle "exceptional conditions"
        for s in exceptional:
            DEBUG("handling exceptional condition for" + s.getpeername())
            # Stop listening for input on the connection
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()

            # Remove message queue
            # del message_queues[s]

        # Handle inputs
        for s in readable:
            if s is socket_listen:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                DEBUG("new connection from" + str(client_address))
                connection.setblocking(0)
                inputs.append(connection)

                # Give the connection a queue for data we want to send
                # message_queues[connection] = queue.Queue()
            else:
                try:
                    data = s.recv(1024)
                except ConnectionResetError:
                    DEBUG("closing "+ str(client_address) +" ConnectionResetError...")
                    # Stop listening for input on the connection
                    if s in writable:
                        writable.remove(s)
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

                    # Remove message queue
                    # del message_queues[s]
                    break

                if data:
                    # A readable client socket has data
                    # message_queues[s].put(data.decode('utf-8'))
                    DEBUG("{} : {}".format(str(s.getpeername()), data.decode('utf-8')))
                    # Add output channel for response
                    if s not in outputs:
                        outputs.append(s)
                else:
                    # Interpret empty result as closed connection
                    DEBUG("closing "+ str(client_address) +"after reading no data")
                    # Stop listening for input on the connection
                    if s in outputs:
                        outputs.remove(s)
                    readable.remove(s)
                    writable.remove(s)
                    inputs.remove(s)
                    s.close()

                    # Remove message queue
                    # del message_queues[s]

        # Handle outputs
        for s in writable:
            # try:
                # next_msg = message_queues[s].get_nowait()
            msg = "message from server"
            # except queue.Empty:
                # No messages waiting so stop checking for writability.
                # DEBUG("output queue for "+str(s.getpeername())+"is empty")
                # outputs.remove(s)
            # else:
            DEBUG("'{}' -> {}".format(msg, str(s.getpeername())))
            s.send(msg.encode('utf-8'))
            outputs.remove(s)
                

if __name__ == "__main__":
    address = ("127.0.0.1", 57270)
    timeout = 60

    host(address, timeout)