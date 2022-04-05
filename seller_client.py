#!/usr/bin/python3
import requests
import json
import time


HOST = '127.0.0.1'
PORT = 1200
addr = f"http://{HOST}:{PORT}"

def create_user(username,password):
    data = {'user_name': username, 'password': password}
    url = addr+"/api/createLogin"
    response = call_seller_sever(data,"post",url)
    print(response)
    return response

def login_user(username,password):
    data = {'user_name': username, 'password': password}
    url = addr+"/api/login"
    response = call_seller_sever(data,"post",url)
    print(response)
    return response

def put_item(seller_id,item):
    data = {'item':item,'seller_id':seller_id}
    url = addr+"/api/putItem"
    response = call_seller_sever(data,"post",url)
    return response

def update_price(seller_id,item_id,price):
    data = {'seller_id':seller_id,'item_id':item_id,'price':price}
    url = addr+"/api/updatePrice"
    print(call_seller_sever(data,"post",url))

def remove_item(seller_id,item_id,quantity):
    data = {'seller_id':seller_id,'item_id':item_id,'quantity':quantity}
    url = addr+"/api/removeItem"
    print(call_seller_sever(data,"post",url))
    
def display_item(seller_id): 
    data = {'seller_id':seller_id}
    url = addr+"/api/displayItem"
    print(call_seller_sever(data,"get",url))

def get_seller_feedback(seller_id): 
    data = {'seller_id':seller_id}
    url = addr+"/api/getSellerFeedback"
    print(call_seller_sever(data,"get",url))


def printProductDB():
    data = {'operation':'printDB'}
    url = addr+"/api/printDB"
    print(call_seller_sever(data,"get",url))

    
def logout(seller_id):
    data = {'seller_id':seller_id}
    url = addr+"/api/logout"
    print(call_seller_sever(data,"get",url))


def call_seller_sever(data,operation,url):
    data = json.dumps(data)
    headers = {'content-type': 'application/json'}
    if operation == "post":
        response = requests.post(url, data=data,headers=headers)
        print("Response code "+ str(response))
        return json.loads(response.text)
    else:
        response = requests.get(url, data=data,headers=headers)
        print("Response code "+ str(response))
        return json.loads(response.text)
    
def main():
    
    #response = create_user("nisha","test")
    
    response = login_user("nisha","test")
    
    seller_id = response['seller_id']
    
    item = [{"name":"Pen","category_id":0,"keywords":["pen","stationary","ink","pencil","school supplies"],"condition":"new","sale_price":2.5,'quantity':5},\
        {"name":"Pencil","category_id":0,"keywords":["pencil","stationary","ink","pencil","school supplies"],"condition":"new","sale_price":1,'quantity':10}]
    
    #response = put_item(seller_id,item)
   
    update_price(seller_id,1,2)

    remove_item(seller_id,0,3)

    #printProductDB()

    display_item(seller_id)
    
    logout(seller_id)

  
if __name__=="__main__":
    main()

   



