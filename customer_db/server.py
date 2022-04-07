from platform import node
import socket
import json
from atomic_broadcast import AtomicBroadcastProtocol

# TODO : Filter SELF IP while sending 
UDP_SOCKET_IP_LIST = ["127.0.0.1","127.0.0.1", "127.0.0.1", "127.0.0.1"]
UDP_SOCKET_PORTS_LIST = [2222,2223, 2224, 2225]

CURRENT_SERVER_UDP_PORT = 2222
CURRENT_SERVER_IP = "0.0.0.0"

# Meta data to send 
global_seq_num = -1
global_seq_recved = -1
# To check before assigning global seq number 
local_seq_commit = [-1,-1,-1,-1]
last_global_seq_recvd = [-1,-1,-1,-1]

local_seq_num = -1
node_id = 0
sock = None

global_seq_to_req_map = {}
request_id_to_msg_map = {}
recieveBuffer = []

def process_seq_message(data):
    global recieveBuffer, global_seq_num, global_seq_recved, local_seq_commit, local_seq_num, node_id
    global global_seq_to_req_map, request_id_to_msg_map, last_global_seq_recvd
    global_seq_num, global_seq_recved, global_seq_to_req_map, local_seq_commit, 
    last_global_seq_recvd, recieveBuffer = atomic_broadcast.processSequenceMessage(
        node_id, sock, data, local_seq_num, global_seq_num, global_seq_recved, 
        local_seq_commit, global_seq_to_req_map, request_id_to_msg_map, last_global_seq_recvd,
        recieveBuffer, UDP_SOCKET_IP_LIST, UDP_SOCKET_PORTS_LIST)

def process_recvd_message(data):
    global recieveBuffer, global_seq_num, global_seq_recved, local_seq_commit, local_seq_num, node_id
    global global_seq_to_req_map, request_id_to_msg_map, last_global_seq_recvd
    request_id_to_msg_map[data['request_id']] = data
    recieveBuffer.append(data)
    last_global_seq_recvd, global_seq_to_req_map, recieveBuffer = atomic_broadcast.processRecieveMessage(
            	node_id, sock, data, local_seq_num, global_seq_num, global_seq_recved, 
                local_seq_commit, global_seq_to_req_map, request_id_to_msg_map, last_global_seq_recvd,
            	recieveBuffer, UDP_SOCKET_IP_LIST, UDP_SOCKET_PORTS_LIST)
    
    
def process_retransmit_message(data):
    return 

def process_req_retransmit_message(data):
    #data = {'request_id':key,'messageType':message_type,'requestor_id':node_id}
    key = key = data['request_id']
    #TODO : make a new req type and write code to process it 
    if key in request_id_to_msg_map:
        send_node_id = data['requestor_id']
        sock.sendto(json.dumps(request_id_to_msg_map[key]).encode(),
                    (UDP_SOCKET_IP_LIST[send_node_id], UDP_SOCKET_PORTS_LIST[send_node_id])) 

def process_seq_retransmit_message(data):
    #data = {'global_seq_num':key,'messageType':message_type,'requestor_id':node_id}
    key = data['global_seq_num'] 
    #TODO : make a new req type and write code to process it 
    if key in global_seq_to_req_map:
        send_node_id = data['requestor_id']
        sock.sendto(json.dumps(global_seq_to_req_map[key]).encode(),
                    (UDP_SOCKET_IP_LIST[send_node_id], UDP_SOCKET_PORTS_LIST[send_node_id])) 

def socket_init():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((CURRENT_SERVER_IP, CURRENT_SERVER_UDP_PORT))

def sendBroadcastMessage(self,request):
    global local_seq_num
    request_id = {"sender_id": node_id,'local_seq_num':local_seq_num}
    data = {"request_id": request_id, "data": request, 'messageType':'request_message', \
         'global_seq_num':global_seq_num,'global_seq_recved':global_seq_recved}
    
    for ip,port in zip(UDP_SOCKET_IP_LIST,UDP_SOCKET_PORTS_LIST):
        try:
            print("UDP target IP: %s" % ip)
            print("UDP target port: %s" % port)
            sock.sendto(json.dumps(request).encode(), (ip, port))
        except Exception as e:
            print(e)
    process_recvd_message(data)
    local_seq_num = local_seq_num + 1


if __name__ == "__main__":
    socket_init()
    atomic_broadcast = AtomicBroadcastProtocol()
    while True:
        data, addr = sock.recvfrom(1024) 
        print(data)
        data = json.loads(data.decode("utf-8"))
        
        #Different message type samples 
        #sequence_msg = {'global_seq_num': global_seq, 'request_id': request_id,'messageType':'sequence_message'}
        ## data = {'request_id':key,'messageType':'retransmit_message','requestor_id':node_id}
        
        
        if (data["messageType"] == "request_message"):
            process_recvd_message(data)
        if (data["messageType"] == "sequence_message"):
            process_seq_message(data)
        if (data["messageType"] == "request_retransmit_message"):
            process_req_retransmit_message(data)
        if (data["messageType"] == "sequence_restransmit_message"):
            process_seq_retransmit_message(data)
        if (data["messageType"] == "process_restransmit_message"):
            process_retransmit_message(data)
            
     
            

        




