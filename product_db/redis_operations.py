import time
from urllib import response
# import redis
import json
import pickle
import database_pb2
import database_pb2_grpc
import sys, requests


class RedisOperations(database_pb2_grpc.redisOperationsServicer):
    
    def __init__(self):
        # self.redis_client = redis.Redis(
        #     host='127.0.0.1',
        #     port=6379,
        #     db=0,
        #     socket_timeout=None
        # )
        self.addr = 'http://127.0.0.1:5000'
        self.set_user_id()
    
    def set_user_id(self):
        if self.exists__raft(self.addr,"User_ID") == 0:
            self.put__raft(self.addr,"User_ID","1000")
    
    def exists(self, request, context):
        print("Exists called ",flush=True)
        print(request.message, flush=True)
        key = request.message
        # val =  self.redis_client.exists(key)
        val = self.exists__raft(self.addr, key)
        print(f'received request: {request} with context {context}', flush=True)
        return database_pb2.Reply(message=str(val))
    
    def get(self, request, context):
        print("get called ",flush=True)
        print(request.message, flush=True)
        key = request.message
        # val = self.redis_client.get(key)
        val = self.get__raft(self.addr, key)
        print(f'received request: {request} with context {context}', flush=True)
        return database_pb2.Reply(message=str(val))
        # return database_pb2.Reply(message=str(val.decode('utf-8')))
    
    def set(self, request, context):
        print("Set called ", flush=True)
        print(request.message+" check this "+request.val, flush=True)
        key = request.message
        val = request.val
        # val = self.redis_client.set(key,val)
        val = self.put__raft(self.addr, key, val)
        print(f'received request: {request} with context {context}', flush=True)
        return database_pb2.Reply(message=str(val))
    
    def delete(self, request, context):
        print("Delete called ", flush=True)
        print(request.message, flush=True)
        key = request.message
        # val = self.redis_client.delete(key)
        val = self.delete__raft(self.addr, key)
        print(f'received request: {request} with context {context}', flush=True)
        return database_pb2.Reply(message=str(val))


#  New Logic to Use Raft instead of REDIS

    def redirectToLeader(self,server_address,path, message):
        type = message["type"]
        # looping until someone tells he is the leader
        while True:
            # switching between "get" + "exists",and  "put", "delete"

            if type == "get" or  type == "exists" :
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


    def delete_raft(self,addr, key, value):
        server_address = addr + "/request/delete"
        payload = {'key': key, 'flag':'delete'}
        message = {"type": "put", "payload": payload}
        # redirecting till we find the leader, in case of request during election
        response = self.redirectToLeader(server_address,"/request/delete" ,message)
        print(response)
        status = response['code']
        return status


    def exists__raft(self,addr, key):
        server_address = addr + "/request/exists"
        payload = {'key': key}
        message = {"type": "get", "payload": payload}
        # redirecting till we find the leader, in case of request during election
        response = self.redirectToLeader(server_address, "/request/exists" ,message)
        db_status = response['payload']['value']
        print(response)
        return db_status

    def put__raft(self,addr, key, value):
        server_address = addr + "/request"
        payload = {'key': key, 'value': value}
        message = {"type": "put", "payload": payload}
        # redirecting till we find the leader, in case of request during election
        response = self.redirectToLeader(server_address, "/request" ,message)
        status = response['code']
        print(response)
        return status

    def get__raft(self,addr, key):
        server_address = addr + "/request"
        payload = {'key': key}
        message = {"type": "get", "payload": payload}
        # redirecting till we find the leader, in case of request during election
        response = self.redirectToLeader(server_address, "/request",message)
        print(response)
        val = response['payload']['value']
        return val


    # def testRaft(self):
    #     addr = "127.0.0.1"
    #     key = "item"
    #     self.get(addr, key)
    #     self.put(addr, key)
    #     self.exists(addr, key)
    #     self.delete(addr, key)


# Put Response {'code': 'success'}
# Get Response {'code': 'success', 'payload': {'key': 'Nisha', 'value': 1000}}
# Exist Response {'code': 'success', 'payload': {'key': 'Nisha', 'value': True}}
# Delete Response {'code': 'success'}
# Exist-2 Response {'code': 'success', 'payload': {'key': 'Nisha', 'value': False}}