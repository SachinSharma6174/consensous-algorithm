import time
import redis
import json
import pickle
import database_pb2
import database_pb2_grpc


class RedisOperations(database_pb2_grpc.redisOperationsServicer):
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host='127.0.0.1',
            port=6379,
            db=0,
            socket_timeout=None
        )
        self.set_user_id()
    
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
        print(request.message+" check this "+request.val, flush=True)
        key = request.message
        val = request.val
        val = self.redis_client.set(key,val)
        print(f'received request: {request} with context {context}', flush=True)
        return database_pb2.Reply(message=str(val))
    
    def delete(self, request, context):
        print("Delete called ", flush=True)
        print(request.message, flush=True)
        key = request.message
        val = self.redis_client.delete(key)
        print(f'received request: {request} with context {context}', flush=True)
        return database_pb2.Reply(message=str(val))
