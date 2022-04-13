import time
import redis
import json
import pickle
import database_pb2
import database_pb2_grpc
import traceback
import socket



# UDP_SOCKET_IP_LIST = ["127.0.0.1", "127.0.0.1", "127.0.0.1", "127.0.0.1"]
# UDP_SOCKET_PORTS_LIST = [2222, 2223, 2224, 2225]

class RedisOperations(database_pb2_grpc.redisOperationsServicer):

    
    def __init__(self):
        self.redis_client = redis.Redis(
            host='127.0.0.1',
            port=6379,
            db=0,
            socket_timeout=None
        )
        self.set_user_id()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = '0.0.0.0'
        self.port = 2222
    
    def set_user_id(self):
        if self.redis_client.exists("User_ID") == 0:
            self.redis_client.set("User_ID","1000")
    
    def exists(self, request, context):
        print("Exists called ",flush=True)
        print(request.message, flush=True)
        key = request.message
        val =  self.redis_client.exists(key)
        print(f'received request: {request} with context {context}', flush=True)
        return database_pb2.Reply(message=str(val))
    
    def get(self, request, context):
        print("get called ",flush=True)
        print(request.message, flush=True)
        key = request.message
        val = self.redis_client.get(key)
        print(f'received request: {request} with context {context}', flush=True)
        return database_pb2.Reply(message=str(val.decode('utf-8')))
    
    def set(self, request, context):
        print("Set called ", flush=True)
        try:
            key = request.message
            val = request.val
            client_request = {'key':key, 'value':val , 'function':'set', 'messageType':'client_message'}
            self.sock.sendto(json.dumps(client_request).encode(), (self.ip, self.port))
        except Exception as e :
            traceback.print_exc()
            print("Exception has occured {}".format(str(e)))
            
        print(f'received request: {request} with context {context}', flush=True)
        val = "OK"
        return database_pb2.Reply(message=str(val))
    
    def delete(self, request, context):
        print("Delete called ", flush=True)
        print(request.message, flush=True)
        try:
            key = request.message
            # val = self.redis_client.delete(key)
            client_request = {'key':key, 'function':'delete','messageType':'client_message'}
            self.sock.sendto(json.dumps(client_request).encode(), (self.ip, self.port))
        except Exception as e:
            traceback.print_exc()
            print("Exception has occured {}".format(str(e)))
        print(f'received request: {request} with context {context}', flush=True)
        val = "OK"
        return database_pb2.Reply(message=str(val))




