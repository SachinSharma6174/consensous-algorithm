# Consensous-Algorithm
Distributed architecture and consensous-algorithm

## Replication of product database using RAFT:

In this application we have used Raft's Vasper implementation in python language.
Our Raft group consists of 5 nodes. 
Each server is initialized with an index and an ip_list.txt. The list of IPs of the servers in the ip_list.txt file is used to determine, the consensus majority based on the  "number of servers" in this file. Each node is started using the below command.

 ```
 python3 server.py <id> ip_list.txt
 ```

We can test a simple RAFT application using the raft/client.py. It perform GET, PUT, EXIST, DELETE request from the command line.
Product  database  is replicated over  5  servers (as the ips mentioned in the IP List file) using  Raft. The GRPC server which is acting as the prodcut database communicates with Raft servers. The server starts the election on init and waits for the vote from all other fellow servers. Current Implementations stores data in-memory in Raft servers and can periodically presist data to Redis. But since it is given that the node will not fail, there is no need to presisting it to redis or any persistent data storage.

## Metric

#### Average response time for each client function when one product database replica (not the leader) fails. 



| Product Database API                      |  TAT (ms) |
|-------------------------------------------|-----------|
| GET - Search API TAT         |  113.91 ms  |
| POST - Add Item API TAT     | 167.92989 ms   |
| POST - Remove Items API TAT   | 154.9091 ms  |
| POST - Put item API TAT         | 162.1950 ms  |
| POST - Update price API TAT     | 173.9192 ms  |
| GET - ProductDB STATE API TAT  | 91.145 ms  |
| GET - Display Item API TAT     | 86.163 ms  |


#### Average response time for each client function when the product database replica acting as leader fails. 

 

| Product Database API                      |  TAT (ms) |
|-------------------------------------------|-----------|
| GET - Search API TAT         |  116.01 ms  |
| POST - Add Item API TAT     | 169.989 ms   |
| POST - Remove Items API TAT   | 155.9091 ms  |
| POST - Put item API TAT         | 161.10 ms  |
| POST - Update price API TAT     | 177.92 ms  |
| GET - ProductDB STATE API TAT  | 101.174 ms  |
| GET - Display Item API TAT     | 91.136 ms  |




## Consensous of customer database using Rotating Sequencer Atomic Broadcast Protocol :

GRPC server recieves the request from the seller/buyer side interface. A UDP server is running on all the replicas of database. The server that recieves the client request broadcasts this to all the replicas. On receiving a request from a client, a group member sends a Request message to every group member. This message includes a unique request id  <sender id, local seq number>, the client request and some additional meta data.
For each Request message, one of the group members assigns a global sequence number to this Request message 
and  sends  out  a  Sequence  message  to  all  group  members. 
The task of assigning global sequence numbers and sending Sequence messages is shared by all group members as 
follows: A Sequence message with global sequence number k is sent out by the group member whose member id is 
k mod n. This group member assigns this global sequence number to a Request message with request message id  <sid, seq#>.
Group members use negative acknowledgement technique to recover from message losses. They send a Retransmit 
request message whenever they detect a missing Request message or a Sequence message. The Retransmit request 
message is sent to the sender of the missing message. 

### Datastructures for Implementation protocol

Meta data to send 
```
    global_seq_num = -1 - node server global sequence tracker
    global_seq_recved = -1 -  node server global sequence received till now tracker
     
    local_seq_commit = [-1,-1,-1,-1] - local seq per proc id used to check before assigning global seq number tracker
    last_global_seq_recvd = [-1,-1,-1,-1] - local seq per proc id recieved used to check before assigning global seq number tracker 

    local_seq_num = 0  -node server local sequence tracker
    node_id = 0 - node id
    abcast = None - type of message

    global_seq_to_req_map = {} - A map of global_seq and the actual request_id
    request_id_to_msg_map = {} - A map of request_id and the actual request message
    recieveBuffer = [] - Queue to buffer message out of commit sequence.

```


## Metric

#### Average response time for each client function when all replicas run normally (no failures). 


| CUSTOMER DB API                           | TAT |
|-------------------------------------------|-----|
| POST- create_user API TAT                       |  152.988912 ms  |
| POST- make_purchase API TAT                     |   190.1278 ms  |
| POST- login_user API TAT                        |  149.9999812 ms   |
| POST- make_purchase API TAT                     |    170.1278 ms  |
| GET- get_seller_feedback API TAT               |  83.19632 ms   |
| POST- create_user seller API TAT                |  162.90662 ms    |


#### Average response time for each client function when one server-side sellers interface replica and one server-side buyers interface to which some of the clients are connected fail.


| CUSTOMER DB API                           | TAT |
|-------------------------------------------|-----|
| POST- create_user API TAT                       |  172.9892 ms  |
| POST- make_purchase API TAT                     |   192.128 ms  |
| POST- login_user API TAT                        |  159.9912 ms   |
| POST- make_purchase API TAT                     |    169.1278 ms  |
| GET- get_seller_feedback API TAT               |  83.1962 ms   |
| POST- create_user seller API TAT                |  181.962 ms    |



System Design Without Raft and Atomic Broadcast Protocol:

<img width="626" alt="Screen Shot 2022-02-21 at 10 37 29 PM" src="https://user-images.githubusercontent.com/26001477/155069969-5123fb98-a5b2-4e90-965a-d5287af26904.png">


The application consists of 6 components:

1. Seller side Server Interface -  The seller server interface is running on google cloud and is acting as Rest server for the seller client. We have used python flask to implement the rest server


2. Seller side Client Interface - Seller Client is a replication of the frontend that interacts with the seller server. It talks to the seller server via rest api calls. 

3. Buyer side Server Interface - The Buyer server interface is running on google cloud and is acting as Rest server for the buyer client. We have used python flask to implement the rest server. 

4. Buyer side Client Interface - Buyer Client is a replication of the frontend that interacts with the buyer server. It talks to the buyer server via rest api calls. 

5. Customer GRPC server -  We have a Customer GRPC server which is acting as a point of contact for all our customer related queries like login, logout, create username password. Internally the GRPC server uses Redis to persist the data/

6. Product GRPC server: We have a product GRPC server which is acting as a point of contact for all our product related queries like search items, put item, update item, purchase item, update feedback.etc


7. Payment API (Using WSDL/SOAP) -  We have created JAVA spring appliations in intellij ide, that use .XSD file to define the WSDL request response and then we have defined a spring service which compiles the .XSD file and genereates the request - response.  The service can be tested by sending a soap request to http://localhost:8080/ws.





# WORKING COMPONENTS:

### RAFT
- [x] Consistent Replication
- [x] Leader Election
- [x] Random Timeouts

### ATOMIC BROADCAST
- [x] Consistent Replication
- [x] Total Ordering across the network
- [x] Total Ordering inside a server
- [x] Consistent write 

### Client-side sellers interface
- [x] Create an account: sets up username and password 
- [x] Login: provide username and password 
- [x] Logout 
- [x] Get seller rating 
- [x] Put an item for sale: provide all item characteristics and quantity 
- [x] Change the sale price of an item: provide item id and new sale price 
- [x] Remove an item from sale: provide item id and quantity 
- [x] Display items currently on sale put up by this seller

### Client-side buyers interface 

Create an account: sets up username and password 
- [x] Login: provide username and password 
- [x] Logout 
- [x] Search items for sale: provide an item category and up to five keywords 
- [x] Add item to the shopping cart: provide item id and quantity 
- [x] Remove item from the shopping cart: provide item id and quantity 
- [x] Clear the shopping cart 
- [x] Display shopping cart 
- [x] Make purchase: credit card details (name, number, expiration date) 
- [x] Provide feedback: thumbs up or down for each item purchased, at most one feedback per purchased item 
- [x] Get seller rating: provide buyer id 
- [x] Get buyer history 
- [x] Run all server components as separate instances in cloud.
- [x] Implement a very  simple  prototype  of  this  component.  It  receives a request (user  name,  credit card  number)  and 
returns Yes (95% pro
