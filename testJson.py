import json

if __name__ == "__main__":
    Register = {
        "packetType":"register",
        "userID":"",
        "userPass":"",
        "nickName":"",
        "timestamp":""
    }

    alter = {
        "packetType":"alter",
        "userID":"",
        "userPass":"",
        "nickName":"",
        "timestamp":""
    }

    Login = {
        "packetType":"login",
        "userID":"",
        "userPass":"",
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

