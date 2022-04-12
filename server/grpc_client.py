import grpc
import database_pb2
import database_pb2_grpc
import traceback

grpc_server = '10.128.0.63:50051'

class GRPCClient():


    def exists(key):
        try :
            with grpc.insecure_channel(grpc_server) as channel:
                stub = database_pb2_grpc.redisOperationsStub(channel)
                data = database_pb2.Request(message=key)
                response = stub.exists(data)
                return response.message        
        except Exception as e:
            traceback.print_exc()
            return ("Error has occured "+str(e))
        
        
    def set(key,value):
        try :
            with grpc.insecure_channel(grpc_server) as channel:
                stub = database_pb2_grpc.redisOperationsStub(channel)
                data = database_pb2.Request(message=key,val=value)
                response = stub.set(data)
                return response.message    
        except Exception as e:
            traceback.print_exc()
            return ("Error has occured "+str(e))
        
    def get(key):
        try :
            with grpc.insecure_channel(grpc_server) as channel:
                stub = database_pb2_grpc.redisOperationsStub(channel)
                data = database_pb2.Request(message=key)
                response = stub.get(data)
                return response.message        
        except Exception as e:
            traceback.print_exc()
            return ("Error has occured "+str(e))
        
    def delete(key):
        try :
            with grpc.insecure_channel(grpc_server) as channel:
                stub = database_pb2_grpc.redisOperationsStub(channel)
                data = database_pb2.Request(message=key)
                response = stub.delete(data)
                return response.message        
        except Exception as e:
            traceback.print_exc()
            return ("Error has occured "+str(e))
