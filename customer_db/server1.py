from email import message
import socket
import json
from atomic_broadcast import AtomicBroadcastProtocol


class udp_server():
    # TODO : Filter SELF IP while sending 
    # UDP_SOCKET_IP_LIST = ["127.0.0.1","127.0.0.1", "127.0.0.1", "127.0.0.1"]
    UDP_SOCKET_IP_LIST = ["0.0.0.0","0.0.0.0"]
    # UDP_SOCKET_PORTS_LIST = [2222,2223, 2224, 2225]
    UDP_SOCKET_PORTS_LIST = [2222,2223]

    CURRENT_SERVER_UDP_PORT = 2223
    CURRENT_SERVER_IP = "0.0.0.0"

    # Meta data to send 
    global_seq_num = -1
    global_seq_recved = -1
    # To check before assigning global seq number 
    local_seq_commit = [-1,-1]
    last_global_seq_recvd = [-1,-1]

    local_seq_num = 0
    node_id = 1
    abcast = None

    global_seq_to_req_map = {}
    request_id_to_msg_map = {}
    recieveBuffer = []
    abcast = AtomicBroadcastProtocol()
        

    def heart_beat_message(self):
        print("Exchanging heart beat message ")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = {'last_global_seq_recvd': self.last_global_seq_recvd, 'messageType':'heartbeat_message'}
        for ip,port in zip(self.UDP_SOCKET_IP_LIST,self.UDP_SOCKET_PORTS_LIST):
            try:
                if port == self.CURRENT_SERVER_UDP_PORT:
                    continue
                print("Sending the heartbeat message data {}".format(data))
                print("UDP target IP: %s" % ip)
                print("UDP target port: %s" % port)
                sock.sendto(json.dumps(data).encode(), (ip, port))
            except Exception as e:
                print(e)

    def process_seq_message(self,data):
        print("Process seq message {}".format(str(data)))
        self.global_seq_num, self.global_seq_recved, self.global_seq_to_req_map, self.local_seq_commit, self.last_global_seq_recvd, self.recieveBuffer = self.abcast.process_seq_message(
        self.node_id, data, self.local_seq_num, self.global_seq_num, self.global_seq_recved, 
        self.local_seq_commit, self.global_seq_to_req_map, self.request_id_to_msg_map, self.last_global_seq_recvd,
        self.recieveBuffer, self.UDP_SOCKET_IP_LIST, self.UDP_SOCKET_PORTS_LIST)
        print("Should call heartbeat message now. {}".format(data))
        if (data["messageType"] == "sequence_message"):
            print("Global seq recieved value . {}".format(self.global_seq_recved))
            self.heart_beat_message()

    def process_recvd_message(self, data):
        print("Process req message {}".format(str(data)))
        request_id = data['request_id']
        print("request id {}".format(str(request_id)))
        self.request_id_to_msg_map[str(request_id)] = data
        print("Chck the dict {}".format(str(self.request_id_to_msg_map)))
        self.recieveBuffer.append(data)
        self.last_global_seq_recvd, self.global_seq_to_req_map, self.recieveBuffer = self.abcast.processRecieveMessage(
                    self.node_id, data, self.local_seq_num, self.global_seq_num, self.global_seq_recved, 
                    self.local_seq_commit, self.global_seq_to_req_map, self.request_id_to_msg_map, self.last_global_seq_recvd,
                    self.recieveBuffer, self.UDP_SOCKET_IP_LIST, self.UDP_SOCKET_PORTS_LIST)
    
    def process_retransmit_message(self,data):  
        if self.global_seq_to_req_map['request_id'] == data['request_id']:
            # send_sequence_message(self, global_seq, request_id, udpIpList, udpPortList, node_id)
            self.abcast.send_sequence_message(self.global_seq_num+1, data['request_id'],
                                                self.UDP_SOCKET_IP_LIST, self.UDP_SOCKET_PORTS_LIST, self.node_id)

    def process_req_retransmit_message(self,data):
        # data = {'request_id':key,'messageType':message_type,'requestor_id':node_id}
        key = data['request_id']
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # TODO : make a new req type and write code to process it 
        if str(key) in self.request_id_to_msg_map:
            send_node_id = data['requestor_id']
            message = self.request_id_to_msg_map[key]
            message['messageType'] = 'missing_req_msg'
            sock.sendto(json.dumps(message).encode(),
                        (self.UDP_SOCKET_IP_LIST[send_node_id], self.UDP_SOCKET_PORTS_LIST[send_node_id])) 

    def process_seq_retransmit_message(self,data):
        # data = {'global_seq_num':key,'messageType':message_type,'requestor_id':node_id}
        key = data['global_seq_num'] 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # TODO : make a new req type and write code to process it 
        if key in self.global_seq_to_req_map:
            self.udp_serversend_node_id = data['requestor_id']
            message = self.global_seq_to_req_map[key]
            sock.sendto(json.dumps(message).encode(),
                        (self.UDP_SOCKET_IP_LIST[self.send_node_id], self.UDP_SOCKET_PORTS_LIST[self.send_node_id])) 
 
    def sendBroadcastMessage(self,request):
        request_id = {"sender_id": self.node_id,'local_seq_num':self.local_seq_num}
        data = {"request_id": request_id, "data": request, 'messageType':'request_message', \
            'global_seq_num':self.global_seq_num,'global_seq_recved':self.global_seq_recved}
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for ip,port in zip(self.UDP_SOCKET_IP_LIST,self.UDP_SOCKET_PORTS_LIST):
            try:
                print("Sending Broadcase message {}".format(data))
                print("UDP target IP: %s" % ip)
                print("UDP target port: %s" % port)
                sock.sendto(json.dumps(data).encode(), (ip, port))
            except Exception as e:
                print(e)
        print("calling process recieved message ")
        self.local_seq_num = self.local_seq_num + 1


if __name__ == "__main__":

    server = udp_server()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server.CURRENT_SERVER_IP, server.CURRENT_SERVER_UDP_PORT))
    while True:
        data, addr = sock.recvfrom(1024) 
        data = json.loads(data.decode("utf-8"))
        
        # Different message type samples 
        # sequence_msg = {'global_seq_num': global_seq, 'request_id': request_id,'messageType':'sequence_message'}
        # data = {'request_id':key,'messageType':'retransmit_message','requestor_id':node_id}
        
        print("Message {} recieved from UDP server ".format(str(data)))
        if (data["messageType"] == 'client_message'):
            server.sendBroadcastMessage(data)
        if (data['messageType'] == 'request_message'):
            server.process_recvd_message(data)
        if (data["messageType"] == "sequence_message"):
            server.process_seq_message(data)
        if (data["messageType"] == "request_retransmit_message"):
            server.process_req_retransmit_message(data)
        if (data["messageType"] == "sequence_restransmit_message"):
            server.process_seq_retransmit_message(data)
        if (data["messageType"] == "missing_req_msg" ):
            server.process_retransmit_message(data)
        if (data["messageType"] == "heartbeat_message"):
            server.process_seq_message(data)
            
     
            

        




