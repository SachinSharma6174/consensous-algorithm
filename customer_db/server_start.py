import grpc
import database_pb2_grpc
from redis_operations import RedisOperations
from concurrent import futures

class Server(database_pb2_grpc.redisOperationsServicer):

   @staticmethod
   def serve():
       server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
       database_pb2_grpc.add_redisOperationsServicer_to_server(RedisOperations(), server)
       server.add_insecure_port('[::]:50051')
       print('started listening on 50051...', flush=True)
       server.start()
       server.wait_for_termination()
       print('finished the termination', flush=True)


if __name__ == '__main__':
#def main():
    Server.serve()
