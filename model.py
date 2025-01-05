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
        # run an sqlthe data command to fetch 
        self.itemcode=itemcode
        self.name=name
        self.description=description
        self.ingredients=ingredients
        self.price=price

class Admin:
    def __init__(self, admin_id, name, phone, email, password):
    
        self.admin_id = admin_id
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password


class Review:
    def __init__(self, review_id, customer_id, date, content):
        
        self.review_id = review_id
        self.customer_id = customer_id
        self.date = date
        self.content = content

class Customer:
    def __init__(self, customer_id, name, birthdate, phone, email, allergens, height, weight, address, preferred_ingredients, level_of_masala):
        
        self.customer_id = customer_id
        self.name = name
        self.birthdate = birthdate
        self.phone = phone
        self.email = email
        self.allergens = allergens
        self.height = height
        self.weight = weight
        self.address = address
        self.preferred_ingredients = preferred_ingredients
        self.level_of_masala = level_of_masala


class Employee:
    def __init__(self, employee_id, name, birthdate, phone, email, job_title, department, hired, address, slots, shift_date):
        
        self.employee_id = employee_id
        self.name = name
        self.birthdate = birthdate
        self.phone = phone
        self.email = email
        self.job_title = job_title
        self.department = department
        self.hired = hired
        self.address = address
        self.slots = slots
        self.shift_date = shift_date


class Order:
    def __init__(self, order_id, customer_id, order_datetime, total_amount, employee_id, status):
    
        self.order_id = order_id
        self.customer_id = customer_id
        self.order_datetime = order_datetime
        self.total_amount = total_amount
        self.employee_id = employee_id
        self.status = status


class Reservation:
    def __init__(self, reservation_id, customer_id, date, time, number_of_guests):
        
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.date = date
        self.time = time
        self.number_of_guests = number_of_guests



def registeruser():
    # sql to add user to db
    # sql to add userrname and password to user table
    # sql to add username': username,
            # 'email': email,
            # 'phone': phone,
            # 'dob': dob,
            # 'height': height,
            # 'weight': weight,
            # to the database
    
    return 1
    return 0
    pass