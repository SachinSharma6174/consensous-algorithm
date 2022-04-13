#!/usr/bin/python3

from unittest import result
from flask import Flask, request, Response
from product import inventory
from shopping_cart import shopping_cart
import socket 
import json
import pickle
import jsonpickle
from user_database_login import user
from helper.purchase_helper import PurchaseHelper

error_code = -1
success_code = 1
app = Flask(__name__)
class client_server():
    
    def __init__(self):
        host='0.0.0.0'
        port=1500
        app.run(host=host, port=port, debug=True)
        
    @app.route('/api/createLogin', methods=['POST'])
    def create_login():
        data = request.get_json()
        username = data['user_name']
        password = data['password']
        user_id,msg = user.create_user(username, password)
        response = {'buyer_id' : user_id, 'message' : msg}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/login',methods=['POST'])
    def login():
        data = request.get_json()
        username = data['user_name']
        password = data['password']
        user_id,msg = user.login_user(username,password)
        response = {'buyer_id' : user_id, 'message' : msg}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/searchItem', methods=['GET'])
    def search_item():
        data = request.get_json()
        category_id = data['category_id']
        keywords = data['keywords']
        product_db = inventory()
        result = product_db.search_item(category_id,keywords)
        response = {'response' : result}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/addItem', methods=['POST'])
    def add_item():
        data = request.get_json()
        buyer_id = data['buyer_id']
        item_id = data['item_id']
        quantity = data['quantity']
        if user.validate_user(buyer_id):
            cart = shopping_cart.get_db_instance()
            ret_code,result =  cart.add_item(buyer_id,item_id,quantity)
            response = {'return_code' : ret_code,'message' : result}
        else :
            response = {'return_code' : error_code, 'message' : "Invalid Buyer Id"}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
        
    
    @app.route('/api/removeItem', methods=['POST'])
    def remove_item():
        data = request.get_json()
        buyer_id = data['buyer_id']
        item_id = data['item_id']
        quantity = data['quantity']
        if user.validate_user(buyer_id):
            cart = shopping_cart.get_db_instance()
            ret_code,result = cart.remove_item(buyer_id,item_id,quantity)
            response = {'return_code' : ret_code,'message' : result}
        else :
            response = {'return_code' : error_code, 'message' : "Invalid Buyer Id"}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/clearCart', methods=['GET'])
    def clear_cart():
        data = request.get_json()
        buyer_id = data['buyer_id']
        if user.validate_user(buyer_id):
            cart = shopping_cart.get_db_instance()
            ret_code,result =  cart.clear_cart(buyer_id)
            response = {'return_code' : ret_code,'message' : result}
        else :
            response = {'return_code' : error_code, 'message' : "Invalid Buyer Id"}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/displayCart', methods=['GET'])
    def display_cart():
        data = request.get_json()
        buyer_id = data['buyer_id']
        if user.validate_user(buyer_id):
            cart = shopping_cart.get_db_instance()
            ret_code,result = cart.display_cart(buyer_id)
            response = {'return_code' : ret_code,'message' : result}
        else :
            response = {'return_code' : error_code, 'message' : "Invalid Buyer Id"}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")    
    
    @app.route('/api/printDB', methods=['GET'])
    def printDB():
        product_db = inventory.get_db_instance()
        redisDB = product_db.redisDB
        result = pickle.loads(product_db.redisDB.get("productDB"))
        response = {'response' : result}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")  
        
    @app.route('/api/logout', methods=['GET'])
    def logout():
        data = request.get_json()
        buyer_id = data["buyer_id"]
        user_id,msg = user.logout(buyer_id)
        response = {'buyer_id' : user_id, 'message' : msg}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")


    """
    /DOC
    Make purchase API, get the cart items for a buyer_id, get the total payment amount 
    for the cart items, and than calls the makePayment method. On success, the inventory is
    updated by subtracting the purchased items.

    """
    @app.route('/api/makePurchase', methods=['POST'])
    def make_purchase():
        data = request.get_json()
        buyer_id = data['buyer_id']
        # Check for whether the user id logged in or not
        if user.validate_user(buyer_id):
            cart = shopping_cart.get_db_instance()
            ret_code,result = cart.display_cart(buyer_id)

            print("Proceed To checkout: Items: ",result)
            paymentAmount = PurchaseHelper.getTotalPurchaseAmount(result)
            payment_status = PurchaseHelper.make_payment(data)
            print("Payment Status :{}".format(payment_status))
            # if payment status is TRUE, update inventory
            if(payment_status=="TRUE"):

                PurchaseHelper.updateInventory(result)

                trxns = PurchaseHelper.createTransaction(buyer_id,result)
                print("Transactions created ",trxns)
            # Log Transaction in Database
            response = {'return_code' : ret_code,'message' : result}
        else :
            response = {'return_code' : error_code, 'message' : "Invalid Buyer Id"}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")

    @app.route('/api/getItemsForFeedback', methods=['GET'])
    def getItemsForFeedback():
        data = request.get_json()
        buyer_id = data["buyer_id"]
        code,data = PurchaseHelper.getItemsForFeedback(buyer_id)
        response = {'status_code' : code, 'message' : data}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")

    @app.route('/api/postFeedback', methods=['POST'])
    def postFeedback():
        data = request.get_json()
        buyer_id = data["buyer_id"]
        code,trxns = PurchaseHelper.postFeedback(buyer_id, data["item_id"],data["feedback"] )
        response = {'status_code' : code, 'message' : trxns}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")


    @app.route('/api/getBuyerHistory', methods=['POST'])
    def getBuyerHistory():
        data = request.get_json()
        buyer_id = data["buyer_id"]
        code,trxns = PurchaseHelper.getBuyerHistory(buyer_id)
        response = {'status_code' : code, 'message' : trxns}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
 
       
if __name__=="__main__":
    print("Starting Buyer Server !!")
    c = client_server()
    print("Buyer Server is UP !!")

