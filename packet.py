import time
import json

def toPacket(jsonString):
    temp = Packet()
    temp.packetify(jsonString)
    return temp

class Packet:
    def __init__(self, packetType="", timestamp=time.time()):
        super().__init__()
        self.packet = {}
        self.packet.update({'packetType':packetType, 'timestamp':timestamp})
 
    def packetify(self, jsonString):
        self.packet.clear()
        self.packet.update(json.loads(jsonString))

    def encode(self):
        return json.dumps(self.packet, ensure_ascii=False).encode('utf-8')

    def add(self, dict):
        self.packet.update(dict)

    def __repr__(self):
        return json.dumps(self.packet, ensure_ascii=False)

class registerPacket(Packet):
    def __init__(self, userID, userPass, userName):
        super().__init__("register")
        self.packet.update({'userID':userID,'userPass':userPass,'nickName':userName})

class loginPacket(Packet):
    def __init__(self, userID, userPass):
        super().__init__("login")
        self.packet.update({'userID':userID,'userPass':userPass})

class alterPacket(Packet):
    def __init__(self, userID, userPass, userName):
        super().__init__("alter",time.time())
        self.packet.update({'userID':userID,'userPass':userPass,'nickName':userName})

class msgPacket(Packet):
    def __init__(self, text):
        super().__init__("message", time.time())
        self.packet.update({'text':text})

class cmdPacket(Packet):
    def __init__(self, text):
        super().__init__("command", time.time())
        self.packet.update({'text':text})



if __name__ == "__main__":
    reg1 = registerPacket("user", "pass", "nickname")
    log1 = loginPacket("user", "pass")
    alt1 = alterPacket("user", "pass", "nickname")
    msg1 = msgPacket("Hi! How are you?")
    cmd1 = cmdPacket("/whoami")

    print(reg1)
    print(log1)
    print(alt1)
    print(msg1)
    print(cmd1)
