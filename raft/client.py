import sys, requests


def redirectToLeader(server_address, path , message):
    type = message["type"]
    # path = server_address
    # looping until someone tells he is the leader
    while True:
        # switching between "get" and "put"
        if type == "get":
            try:
                response = requests.get(server_address,
                                        json=message,
                                        timeout=1)
            except Exception as e:
                return e
        else:
            try:
                response = requests.put(server_address,
                                        json=message,
                                        timeout=1)
            except Exception as e:
                return e

        # if valid response and an address in the "message" section in reply
        # redirect server_address to the potential leader
        if response.status_code == 200 and "payload" in response.json():
            payload = response.json()["payload"]
            if "message" in payload:
                server_address = payload["message"] + path
            else:
                break
        else:
            break
    # if type == "get":
    return response.json()
    # else:
    #     return response


# client put request
def put(addr, key, value):
    server_address = addr + "/request"
    payload = {'key': key, 'value': value}
    message = {"type": "put", "payload": payload}
    # redirecting till we find the leader, in case of request during election
    return redirectToLeader(server_address, "/request" ,message)


# client get request
def get(addr, key):
    server_address = addr + "/request"
    payload = {'key': key}
    message = {"type": "get", "payload": payload}
    # redirecting till we find the leader, in case of request during election
    return redirectToLeader(server_address, "/request" , message)

def exists(addr, key):
    server_address = addr + "/request/exists"
    payload = {'key': key}
    message = {"type": "get", "payload": payload}
    # redirecting till we find the leader, in case of request during election
    return redirectToLeader(server_address, "/request/exists", message)

def delete(addr, key):
    server_address = addr + "/request/delete"
    payload = {'key': key, 'flag':'delete'}
    message = {"type": "put", "payload": payload}
    # redirecting till we find the leader, in case of request during election
    return redirectToLeader(server_address,"/request/delete" , message)


if __name__ == "__main__":
    # addr, key
    # get
    addr = "http://127.0.0.1:5001"
    # addr = sys.argv[1]
    key = "Nisha"
    val = 1000
    print("Put Response", put(addr, key, val))
    print("Get Response", get(addr, key))
    print("Exist Response", exists(addr, key))
    print("Delete Response", delete(addr, key))
    print("Exist-2 Response", exists(addr, key))
    # addr, key value
    # put
    
    # else:
    #     print("PUT usage: python3 client.py address 'key' 'value'")
    #     print("GET usage: python3 client.py address 'key'")
    #     print("Format: address: http://ip:port")