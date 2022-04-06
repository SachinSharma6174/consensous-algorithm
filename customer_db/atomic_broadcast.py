import redis


class AtomicBroadcastProtocol():
    
    def __init__(self):
        self.redis_client = redis.Redis(
			host='127.0.0.1',
			port=6379,
			db=0,
			socket_timeout=None
		)
        
    def redisAction(self, message):
        response = None
        key  = message['key']
        if message['messageType'] == 'client':
            if message['function'] == 'delete':
                response = self.redis_client.delete(key)
            if message['function'] == 'set':
                val = message['value']
                response = self.redis_client.set(key,val)
        return response
    
    def processRecieveMessage(self, node_id, sock, message, local_seq_num, global_seq_num, \
        global_seq_recved, local_seq_commit, global_seq_send_map, global_seq_recv_map, \
        recieveBuffer, udpIpList, udpPortList):
        total_proc = len(udpIpList)
        
        if (global_seq_num + 1) % total_proc == node_id:
            return "ok"


	


            