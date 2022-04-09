import redis
import json
import socket

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
    
    def retransmit_message(self,sender_id, key, node_id, message_type, udpIpList, udpPortList):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if message_type == 'request_retransmit_message':
            data = {'request_id':key,'messageType':message_type,'requestor_id':node_id}
            sock.sendto(json.dumps(data).encode(), (udpIpList[sender_id], udpPortList[sender_id]))
        elif message_type == 'sequence_restransmit_message':
            data = {'global_seq_num':key,'messageType':message_type,'requestor_id':node_id}
            sock.sendto(json.dumps(data).encode(), (udpIpList[sender_id], udpPortList[sender_id]))
        return
    
    def send_sequence_message(self, global_seq, request_id, udpIpList, udpPortList):
        sequence_msg = {'global_seq_num': global_seq, 'request_id': request_id,'messageType':'sequence_message'}
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for ip,port in zip(udpIpList,udpPortList):
            try:
                if port == 2222:
                    continue
                print("Called from send_sequence message : {}".format(str(sequence_msg)))
                print("UDP target IP: %s" % ip)
                print("UDP target port: %s" % port)
                sock.sendto(json.dumps(sequence_msg).encode(), (ip, port))
            except Exception as e:
                print(e)
                
    def calculate_majority(self,last_global_seq_recvd, global_seq_num):
        num_of_true = 0
        total_node = len(last_global_seq_recvd)
        for i in last_global_seq_recvd:
            if int(i) < global_seq_num:
                num_of_true = num_of_true + 1
        if num_of_true > (total_node/2):
            return True
        return False
    
    def delete_request(self, buffer, request_id):
        for i in buffer:
            if i['request_id'] == request_id:
                buffer.remove(i)
                return buffer
    
    def process_seq_message(self, node_id, message, local_seq_num, global_seq_num, \
        global_seq_recved, local_seq_commit, global_seq_to_req_map, request_id_to_msg_map, \
        last_global_seq_recvd, recieveBuffer, udpIpList, udpPortList):
        total_proc = len(udpIpList)
        
        #Message type
        #sequence_msg = {'global_seq_num': global_seq, 'request_id': request_id,'messageType':'sequence_message'}
        
        global_seq_curr = message['global_seq_num']
        global_seq_to_req_map[global_seq_curr] = message['request_id']
        sender = message['request_id']['sender_id']
        #Check if the last one
        if global_seq_curr == global_seq_recved + 1:
            global_seq_recved = global_seq_curr
        # check if its the next one 
        if last_global_seq_recvd[sender] + 1 == global_seq_curr:
            last_global_seq_recvd[sender]  = global_seq_curr
        
        while  global_seq_num  <= global_seq_curr :
            # calculate majority global seq number
            if (self.calculate_majority(last_global_seq_recvd, global_seq_num)):
                if (global_seq_num + 1) in global_seq_to_req_map: 
                    request_id = global_seq_to_req_map[global_seq_num + 1]
                    if request_id in request_id_to_msg_map: 
                        client_req = request_id_to_msg_map[request_id]
                        self.redisAction(client_req['data'])
                        req_messg_sender = request_id['sender_id']
                        req_local_seq_sender = request_id['local_seq_num']
                        # Update global seq number and last commited local sequence number
                        # of the sender using client request ID 
                        global_seq_num = global_seq_num + 1
                        local_seq_commit[req_messg_sender] = req_local_seq_sender
                        # Delete the req from the receive buffer queue 
                        recieveBuffer = self.delete_request(recieveBuffer,request_id)
                    else: 
                        # Ask for retransmit of request message
                        self.retransmit_message(request_id['sender_id'], request_id, node_id, 
                                                "request_retransmit_message", sock, udpIpList, udpPortList)
                else :
                    # Ask for retransmit for global seq message 
                    global_seq_holder_node = (global_seq_num + 1) % total_proc
                    self.retransmit_message(global_seq_holder_node, global_seq_num + 1, node_id, 
                                                "sequence_restransmit_message", udpIpList, udpPortList)
        return global_seq_num, global_seq_recved, global_seq_to_req_map, local_seq_commit, last_global_seq_recvd, recieveBuffer
    
    def processRecieveMessage(self, node_id, message, local_seq_num, global_seq_num, \
        global_seq_recved, local_seq_commit, global_seq_to_req_map, request_id_to_msg_map, \
        last_global_seq_recvd, recieveBuffer, udpIpList, udpPortList):
        total_proc = len(udpIpList)
        
        
        # data = {"request_id": request_id, "data": request, 'messageType':'request_message', \
        # 'global_seq_num':global_seq_num,'global_seq_recved':global_seq_recved}
        
        # Update meta data info 
        sender_id = message['request_id']['sender_id']
        last_global_seq_recvd[sender_id] = message['global_seq_recved']
        
        if (global_seq_num + 1) % total_proc == node_id:
            # The first message in the queue 
            data = recieveBuffer.pop(0)
            # Then this process has to assign global seq number 
            sender_id = data['request_id']['sender_id']
            sender_seq = data['request_id']['local_seq_num']
            # check if its the next global seq number to be committed 
            # if global_seq_num > -1 and (global_seq_num) in global_seq_to_req_map.keys():
            #     # check if its the next local seq number for the sender 
            if sender_seq == local_seq_commit[sender_id] + 1:
                # send Sequence message for sender_seq 
                self.send_sequence_message(global_seq_num+1, data['request_id'], udpIpList, udpPortList)
            else : 
                # check if the next_seq exists in buffer 
                next_seq = local_seq_commit[sender_id] + 1
                key = {'sender_id' : sender_id, 'local_seq_num': next_seq}
                print("Check the dict ")
                print(str(request_id_to_msg_map))
                if key in request_id_to_msg_map.keys():
                    self.send_sequence_message(global_seq_num+1, key, udpIpList, udpPortList)
                    global_seq_to_req_map[global_seq_num+1] = key
                else:
                    # Ask for restransmit of next seq
                    self.retransmit_message(sender_id, key, node_id, "request_retransmit_message",
                                            udpIpList, udpPortList)
                    # Add the one you don't have but don't increment the global_seq_num 
                    global_seq_to_req_map[global_seq_num+1] = key
                # add the data back to the queue as it wasn't processed
                recieveBuffer.insert(0,data)
        return last_global_seq_recvd, global_seq_to_req_map,recieveBuffer
                
            
            
# TODO : Figure out in case of retransmission for a request message 
# that wasn't there but should be assigned global seq number
