#!/usr/bin/python3

success_code = 1
error_code = -1
class shopping_cart():
    cart = None
    __instance = None
    
    
    @staticmethod
    def get_db_instance():
        if shopping_cart.__instance == None:
            shopping_cart()
        return shopping_cart.__instance
    
    def __init__(self) -> None:
        if shopping_cart.__instance != None:
            raise Exception("This is a singleton class")
        else:
            shopping_cart.__instance = self
        self.cart = {'item':'nothing'}
        print("Shopping cart called")
    
    def add_item(self,buyer_id,item_id,quantity):
        try :
            if buyer_id in self.cart:
                item_dict = self.cart[buyer_id]
                item_dict[item_id] = quantity
            else:
                self.cart[buyer_id] = {item_id:quantity}
            return (success_code,"Added item to cart")
        except Exception as e:
            return (error_code,str(e))
        
    def remove_item(self,buyer_id,item_id,quantity):
        try:
            print("Remove item function called")
            if buyer_id in self.cart:
                item_dict = self.cart[buyer_id]
                item_dict[item_id] = quantity
            else:
                self.cart[buyer_id] = {item_id:quantity}
            return (success_code,"Removed item from cart")
        except Exception as e:
            return (error_code,str(e))
    
    def clear_cart(self,buyer_id):
        try:
            print("Clear cart function called")
            if buyer_id in self.cart:
                del self.cart[buyer_id]
                return (success_code,"cleared cart")
            else:
                return (success_code,"cart is empty")
        except Exception as e:
            return (error_code,str(e))
    
    def display_cart(self,buyer_id):
        try:
            print("Display cart function called")
            if buyer_id in self.cart:
                return (success_code,self.cart[buyer_id])
            else:
                return (success_code,"empty cart")
        except Exception as e:
            return (error_code,str(e))
    

    