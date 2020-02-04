import json

if __name__ == "__main__":
    Register = {
        "packetType":"register",
        "id":"",
        "password":"",
        "NickName":"",
        "timestamp":""
    }

    alter = {
        "packetType":"alter",
        "id":"",
        "password":"",
        "NickName":"",
        "timestamp":""
    }

    Login = {
        "packetType":"login",
        "id":"",
        "password":"",
        "timestamp":""
    }

    command = {
        "packetType":"command",
        "text":"",
        "timestamp":""
    }

    message = {
        "packetType":"message",
        "text":"",
        "timestamp":""
    }

    print(json.dumps(Register))
    print(json.dumps(Login))
    print(json.dumps(command))
    print(json.dumps(message))
    print(json.dumps(alter))

