
docker pull redis
docker run -d -p 6379:6379 --name redis-server redis
# To access Redis CLI running on docker
# docker exec -it redis-server redis-cli

# TO start to Buyer Server side socket connection
python3 buyer_server.py

# TO start to Seller Server side socket connection
python3 seller_server.py

