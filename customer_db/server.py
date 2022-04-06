import socket
import json
from atomic_broadcast import AtomicBroadcastProtocol


UDP_SOCKET_IP_LIST = ["127.0.0.1", "127.0.0.1", "127.0.0.1"]
UDP_SOCKET_PORTS_LIST = [2223, 2224, 2225]

CURRENT_SERVER_UDP_PORT = 2222
CURRENT_SERVER_IP = "0.0.0.0"


local_seq_num = 0
global_seq_num = 0
global_seq_recved = 0
local_seq_commit = {}
node_id = 0
sock = None

global_seq_send_map = {}
global_seq_recv_map = {}
recieveBuffer = []
sendBuffer = []


def socket_init():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((CURRENT_SERVER_IP, CURRENT_SERVER_UDP_PORT))

def sendBroadcastMessage(self,request):
    request_id = {"sender_id": node_id,'local_seq_num':local_seq_num}
    data = {"request_id": request_id, "data": request, 'messageType':'request_message', \
         global_seq_num:global_seq_num,'global_seq_recved':global_seq_recved}
    
    for ip,port in zip(UDP_SOCKET_IP_LIST,UDP_SOCKET_PORTS_LIST):
        try:
            print("UDP target IP: %s" % ip)
            print("UDP target port: %s" % port)
            sock.sendto(json.dumps(request).encode(), (ip, port))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    socket_init()
    atomic_broadcast = AtomicBroadcastProtocol()
    while True:
        data, addr = sock.recvfrom(1024) 
        print(data)
        data = json.loads(data.decode("utf-8"))
        
        if (data["messageType"] == "request_message"):
        	local_seq_num, global_seq_num, recieve, recieveBuffer, send = \
            atomic_broadcast.processRecieveMessage(
            	node_id, sock, data, local_seq_num, global_seq_num, global_seq_recved, 
                local_seq_commit, global_seq_send_map, global_seq_recv_map, recieveBuffer,
            	UDP_SOCKET_IP_LIST, UDP_SOCKET_PORTS_LIST)


     
            

        




