"""This file contains all the functions that serve as controller"""

#imports



#cglobal 



#code

#class

class User:
    def __init__(self, account_id , username, password  ):
        # sql statement to fetch userdata and assign the attributes
        self.account_id=account_id
        self.username=username
        self.password=password

class Customer(User):
    pass

class Employee():
    pass

class Menu:
    def __init__(self, itemcode, name, description, ingredients, price):
        # run an sql command to fetch the data
        self.itemcode=itemcode
        self.name=name
        self.description=description
        self.ingredients=ingredients
        self.price=price

