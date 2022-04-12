#!/usr/bin/python3
from flask import Flask, request, Response
from product import inventory
import requests
import json
import pickle
import jsonpickle
from user_database_login import user

error_code = -1
success_code = 1
app = Flask(__name__)
class seller_server:
    
    def __init__(self):
        host='0.0.0.0'
        port=1200
        app.run(host=host, port=port, debug=True)
    
    @app.route('/api/createLogin', methods=['POST'])
    def create_login():
        data = request.get_json()
        username = data['user_name']
        password = data['password']
        user_id,msg = user.create_user(username, password)
        response = {'seller_id' : user_id, 'message' : msg}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/login',methods=['POST'])
    def login():
        data = request.get_json()
        username = data['user_name']
        password = data['password']
        user_id,msg = user.login_user(username,password)
        response = {'seller_id' : user_id, 'message' : msg}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/putItem', methods=['POST'])
    def put_item():
        data = request.get_json()
        seller_id = data['seller_id']
        item = data['item']
        if user.validate_user(seller_id):
            product_db = inventory()
            ret_code,result = product_db.put_item(item,seller_id)
            response = {'return_code' : ret_code,'message' : result}
        else :
            response = {'return_code' : error_code, 'message' : "Invalid Seller Id"}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/updatePrice', methods=['POST'])
    def update_price():
        data = request.get_json()
        seller_id = data['seller_id']
        item_id = data['item_id']
        price = data['price']
        if user.validate_user(seller_id):
            product_db = inventory()
            ret_code,result =  product_db.update_item(item_id,key='sale_price',value=price)  
            response = {'return_code' : ret_code,'message' : result}
        else :
            response = {'return_code' : error_code, 'message' : "Invalid Seller Id"}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
        
    @app.route('/api/removeItem', methods=['POST'])
    def remove_item():
        data = request.get_json()
        seller_id = data['seller_id']
        item_id = data['item_id']
        quantity = data['quantity']
        if user.validate_user(seller_id):
            product_db = inventory()
            ret_code,result =  product_db.update_item(item_id,key='quantity',value=quantity)
            response = {'return_code' : ret_code,'message' : result}
        else :
            response = {'return_code' : error_code, 'message' : "Invalid Seller Id"}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/displayItem', methods=['GET'])    
    def display_item():
        data = request.get_json()
        print("Here okay")
        seller_id = data['seller_id']
        if user.validate_user(seller_id):
            product_db = inventory()
            ret_code,result = product_db.get_item_by_seller_id(seller_id)
            response = {'return_code' : ret_code,'message' : result}
        else :
            response = {'return_code' : error_code, 'message' : "Invalid Seller Id"}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    
    @app.route('/api/printDB', methods=['GET'])
    def printDB():
        product_db = inventory()
        redisDB = product_db.redisDB
        val = pickle.loads(product_db.redisDB.get("productDB"))
        #print(val)
        response = { 'response' : val}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
        
    @app.route('/api/logout', methods=['GET'])
    def logout():
        data = request.get_json()
        seller_id = data["seller_id"]
        user_id,msg = user.logout(seller_id)
        response = {'seller_id' : user_id, 'message' : msg}
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")


    @app.route('/api/getSellerFeedback', methods=['GET'])
    def getSellerFeedback():
        data = request.get_json()
        seller_id = data['seller_id']
        product_db = inventory()
        SUCCESS_CODE,rating =product_db.getSellerOverallFeedback(seller_id)
        response = { 'SUCCESS_CODE':SUCCESS_CODE,'response': rating }
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
  
  
if __name__=="__main__":
    print("Starting Seller Server !!")
    s = seller_server()
    print("Seller Server is UP !!")

                

