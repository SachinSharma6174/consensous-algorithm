#!/usr/bin/python3
import json
import pickle
from grpc_client import  GRPCClient
import traceback

error_code = -1
class user():
    
    def create_user(user_name, password):
        print("Create User called for {}".format(user_name))
        try :
            exists = GRPCClient.exists(user_name)   
            if exists == "0":
                user_id = GRPCClient.get("User_ID")
                # user_id = 100
                print("user_id ", user_id)
                data = {'user_id' : user_id , 'password' :password}
                GRPCClient.set(user_name,str(data))
                val = int(user_id) + 1
                GRPCClient.set("User_ID", str(val))
                return (user_id,"Ok")
            else :
                return (error_code,"Username already exists")
        except Exception as e:
            traceback.print_exc()
            return (error_code,"Error has occured "+str(e))
        
    def login_user(user_name, password):
        print("Login called for {}".format(user_name))
        try :
            exists = GRPCClient.exists(user_name)
            if exists == "0":
                return (error_code,"No such user")
            else :
                val = GRPCClient.get(user_name)
                val = val.replace("\'", "\"")
                val = json.loads(val)
                print(val)
                if val['password'] == password:
                    GRPCClient.set(val['user_id'],"True")
                    return (val['user_id'],"Ok")
                else :
                    return (error_code,"Incorrect Password")
        except Exception as e:
            traceback.print_exc()
            return (error_code,"Error has occured" +str(e))
        
    def logout(user_id):
        try:
            exists = GRPCClient.exists(user_id)
            if exists == "1":
                GRPCClient.delete(user_id)
                return (user_id,"Ok")
            else:
                return (error_code,"no such user")
        except Exception as e:
            return (error_code,"Error has occured" +str(e))
    
    def validate_user(user_id):
        try:
            exists = GRPCClient.exists(user_id)
            if exists == "0":
                return False
            else :
                return True
        except Exception as e:
            print (str(e))
            return False
        
                    
