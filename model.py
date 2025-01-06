"""This file contains all the functions that serve as controller"""

#imports
import mysql.connector
from mysql.connector import Error



#cglobal 



# connection to database
def connect_to_database():
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="aesthetic_res"
        )
        
        if connection.is_connected():
            print("Connected to MySQL database!")
            # Fetch and print server information
            db_info = connection.get_server_info()
            print(f"MySQL Server version: {db_info}")
            
            # Create a cursor to execute SQL queries
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            print(f"Connected to database: {db_name[0]}")

            return connection

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None



# Call the function to connect
db_connection = connect_to_database()



def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
        
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")




#class
class User:
    def __init__(self, account_id , username, password  ):
        self.account_id=account_id
        self.username=username
        self.password=password


class Menu:
    def __init__(self, itemcode, name, description, pictures, ingredients, price):
        self.itemcode=itemcode
        self.name=name
        self.description=description
        self.pictures=pictures
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



def fetchmenu():
    query = "SELECT * FROM aesthetic_res.menu;"
    if db_connection and db_connection.is_connected():
         result=execute_query(db_connection, query)
    menulist=[]
    for i in result:
        pic=i[3].split(",")
        ing=i[4].split(",")
        menulist.append(Menu(i[0],i[1],i[2],pic, ing,i[5]))
    return menulist

def fetchmenu_byid(itemid):
    query = f"SELECT * FROM aesthetic_res.menu where itemid={itemid};"
    if db_connection and db_connection.is_connected():
         result=execute_query(db_connection, query)
    menulist=[]
    for i in result:
        pic=i[3].split(",")
        ing=i[4].split(",")
        menulist.append(Menu(i[0],i[1],i[2],pic, ing,i[5]))
    return menulist[0]



def fetchuser_byusername(username):
    query = f"SELECT * FROM aesthetic_res.user where username='{username}';"
    if db_connection and db_connection.is_connected():
         result=execute_query(db_connection, query)
    if len(result)<1:
        return None
    else:
        i=result[0]
        return User(i[0], i[2], i[1])



def fetchcustomer_by_customerid(customer_id):
    query = f"SELECT * FROM aesthetic_res.customer where Customer_ID='{customer_id}';"
    if db_connection and db_connection.is_connected():
         result=execute_query(db_connection, query)
    print(result)
    # def __init__(self, customer_id, name, birthdate, phone, email, allergens, height, weight, address, preferred_ingredients, level_of_masala)
    if len(result)<1:
        return None
    else:
        i=result[0]
        print(i)
        
        return Customer(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10])



def addmenu(item):
    # converting pictureslist to text
    s=""
    for i in item.pictures:
        s+=i + ","
    
    item.pictures=s[:-1]

    print(item.pictures)
    print(type(item.pictures))


    query = f"INSERT INTO `aesthetic_res`.`menu` (`ItemName`, `Description`, `Picture`, `Ingredients`, `Price`) VALUES ('{item.name}', '{item.description}', '{item.pictures}', '{item.ingredients}', '{item.price}');"
    if db_connection and db_connection.is_connected():
         execute_query(db_connection, query)
         db_connection.commit()
    print("rows added")


# x=Menu(0,"name", "desc", "pictre1,pic2", "ing", 45)
# addmenu(x)
# print(fetchmenu_byid(6).pictures)


# UPDATE `aesthetic_res`.`menu` SET `ItemName` = 'name', `Description` = 'desc', `Picture` = 'picture,pic3', `Ingredients` = 'ing1,ing2', `Price` = '24' WHERE (`ItemID` = '7');


def updatemenu(item):
    # converting pictureslist to text
    s=""
    for i in item.pictures:
        s+=i + ","
    
    item.pictures=s[:-1]

    print(item.pictures)
    print(type(item.pictures))

    print(item.itemcode)
    # query=f"UPDATE `aesthetic_res`.`menu` SET `ItemName` = '{item.name}', `Description` = '{item.description}', `Picture` = '{item.pictures}', `Ingredients` = '{item.ingredients}', `Price` = '{item.price}' WHERE (`ItemID` = '{item.itemcode}');"
    query=f"UPDATE `aesthetic_res`.`menu` SET `ItemName` = '{item.name}' WHERE (`ItemID` = '{item.itemcode}');"
    if db_connection and db_connection.is_connected():
         execute_query(db_connection, query)
         db_connection.commit()
    print("rows edited")



def deleteitem(itemcode):
    query=f"DELETE FROM `aesthetic_res`.`menu` WHERE (`ItemID` = '{itemcode}');"
    if db_connection and db_connection.is_connected():
         execute_query(db_connection, query)
         db_connection.commit()
    print("rows deleted")


def updateprofile(user):
    query=f"UPDATE `aesthetic_res`.`customer` SET `Name` = '{user.name}', `Birthdate` = '{user.birthdate}', `Phone` = '{user.phone}', `Email` = '{user.address}', `Allergens` = '{user.allergens}', `Height` = '{user.height}', `Weight` = '{user.weight}', `Address` = '{user.address}', `Preferred_Ingredients` = '{user.preferred_ingredients}', `Level_of_Masala` = '{user.level_of_masala}' WHERE (`Customer_ID` = '{user.customer_id}');"
    if db_connection and db_connection.is_connected():
         execute_query(db_connection, query)
         db_connection.commit()
    print("rows edited")









