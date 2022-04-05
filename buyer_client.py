#!/usr/bin/python3
from re import S
import requests
import json
from subprocess import call
from unicodedata import category 
import pickle
import time



HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1500      # The port used by the server
addr = f"http://{HOST}:{PORT}"

def create_user(username,password):
    data = {'user_name': username, 'password': password}
    url = addr+"/api/createLogin"
    response = call_buyer_sever(data,"post",url)
    return response

def login_user(username,password):
    data = {'user_name': username, 'password': password}
    url = addr+"/api/login"
    response = call_buyer_sever(data,"post",url)
    return response

def search_item(category_id,keywords):
    print("\n Buyer Client :: Search Items")
    data = {'category_id':category_id,'keywords':keywords}
    url = addr+"/api/searchItem"
    response = call_buyer_sever(data,"get",url)
    print("\nSearch Item RESPONSE",response)
    return response
    
def add_item_to_cart(buyer_id,item_id,quantity):
    data = {'buyer_id':buyer_id,'item_id':item_id,'quantity':quantity}
    url = addr+"/api/addItem"
    return call_buyer_sever(data,"post",url)
    
    
def remove_item(buyer_id,item_id,quantity): 
    data = {'buyer_id':buyer_id,'item_id':item_id,'quantity':quantity} 
    url = addr+"/api/removeItem"
    return call_buyer_sever(data,"post",url)
    
def clear_cart(buyer_id):
    data = {'buyer_id':buyer_id}
    url = addr+"/api/clearCart"
    return call_buyer_sever(data,"get",url)
    
    
def display_cart(buyer_id):
    print("\nDisplay Cart for Buyer Id {}".format(buyer_id))
    data = {'operation':'display_cart','buyer_id':buyer_id}
    url = addr+"/api/displayCart"
    return call_buyer_sever(data,"get",url)

def make_purchase(buyer_id,data):
    print("making purchase for buyer_id",buyer_id)
    data = {'buyer_id':buyer_id, 'data':data}
    url = addr+"/api/makePurchase"
    return call_buyer_sever(data,"post",url)

def get_items_for_feedback(buyer_id):
    print("Getting Items for feedback",buyer_id)
    data = {'buyer_id':buyer_id}
    url = addr+"/api/getItemsForFeedback"
    return call_buyer_sever(data,"get",url)

def post_feedback(buyer_id,item_id,feedback):
    print("Post feedback by {} for item_Id {} with feedback {}".format(buyer_id,item_id,feedback))
    data = {'buyer_id':buyer_id, "item_id": item_id, "feedback": feedback}
    url = addr+"/api/postFeedback"
    return call_buyer_sever(data,"post",url)


def display_all_items():
    data = {'operation':'display_all_items'}
    url = addr+"/api/printDB"
    return call_buyer_sever(data,"get",url)

def logout(buyer_id):
    data = {'buyer_id':buyer_id}
    url = addr+"/api/logout"
    print(call_buyer_sever(data,"get",url))

def get_buyer_history(buyer_id):
    data = {'buyer_id':buyer_id}
    url = addr+"/api/getBuyerHistory"
    print(call_buyer_sever(data,"post",url))


def call_buyer_sever(data,operation,url):
    data = json.dumps(data)
    headers = {'content-type': 'application/json'}
    if operation == "post":
        response = requests.post(url, data=data,headers=headers)
    else:
        response = requests.get(url, data=data,headers=headers)
    print("Response code "+ str(response))
    return json.loads(response.text)




"""
Inside main we have defined several test cases for testing out several buyer test cases

"""
def main():

    # response = create_user("sachin","test")
    response = login_user("sachin","test")
    
    buyer_id = response['buyer_id']
    items = search_item(0,["stationary","Pen"])
    
    print(add_item_to_cart(buyer_id,0,"1"))
    data  = {'buyer_id':buyer_id,'Name':'sachin','card_number':'4032678965432201' , 'expiration_date':'02022025'}
    make_purchase(buyer_id,data)

    # print(remove_item(buyer_id,0,"2"))

    # print(display_cart(buyer_id))

    # print(clear_cart(buyer_id))
    
    # print(logout(buyer_id))
    get_items_for_feedback(buyer_id)
    get_buyer_history(buyer_id)


def testWSDL():
        url = "http://b564-2601-281-8080-2ef0-4cfd-ef63-fee8-4002.ngrok.io/ws"
        xml = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:gs="http://spring.io/guides/gs-producing-web-service">
                    <soapenv:Header/>
                    <soapenv:Body>
                        <gs:transactionRequest>
                            <gs:name>Sachin</gs:name>
                            <gs:cardNumber>2341234341</gs:cardNumber>
                            <gs:expiryDate>{expiry_date}</gs:expiryDate>
                        </gs:transactionRequest>
                    </soapenv:Body>
                </soapenv:Envelope>"""
        headers = {'Content-Type': 'text/xml'}
        response = requests.post(url, data=xml.format(name,card_number,expiration_date), headers=headers)
        return response.text





if __name__=="__main__":
    main()
