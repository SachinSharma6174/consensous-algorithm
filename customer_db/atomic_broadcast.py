
class AtomicBroadcastProtocol():
	def __init__(self):
        self.redis_client = redis.Redis(
            host='127.0.0.1',
            port=6379,
            db=0,
            socket_timeout=None
        )
 

	def redisAction(self,message):
		response=None
		key  = message['key']
		if message['messageType'] == 'client':
			if message['function'] == 'delete':
				response = self.redis_client.delete(key)
			if message['function'] == 'set':
				val = message['value']
				response = self.redis_client.set(key,val)
		return response



	def processRecieveMessage(self, node_id, sock, message, local_seq_num, global_seq_num, \
					global_seq_send_map, global_seq_recv_map, recieveBuffer, udpIpList, \
					udpPortList):
		# message = json.loads(message.decode("utf-8"))

		#  Implementation for Handling Request_message
		return "ok"