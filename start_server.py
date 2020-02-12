import server_related.serverGUI as serverGUI
import server_related.server_mod as server_mod
from multiprocessing import Process
import sys
import os

def startServer(host_addr, port, DEBUG=False):
    Server = server_mod.HostServer(host_addr, port, DEBUG)
    Server.host()

def startGUI():
    GUI = serverGUI.ServerGUI()
    GUI.initialize()

def DEBUG(message):
    print(message,file=sys.stderr)

if __name__ == "__main__":
    host_addr = "127.0.0.1"
    port = 57270

    DEBUG("Create Process...")
    GUI = Process(target=startGUI)
    SERVER = Process(target=startServer, args=("127.0.0.1", 57270, True))

    DEBUG("Start Process...")
    SERVER.start()
    GUI.start()

    DEBUG("Join Process...")
    GUI.join()
    SERVER.join()