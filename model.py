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


class Staff:
    def __init__(self, staff_id, name, role, phone, email, address, salary, schedule):
        self.staff_id = staff_id
        self.name = name
        self.role = role
        self.phone = phone
        self.email = email
        self.address = address
        self.salary = salary
        self.schedule = schedule  



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



class OrderSummary:
    def __init__(self, order_id, customer_id, items, total_amount, order_date, payment_status):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items  
        self.total_amount = total_amount
        self.order_date = order_date
        self.payment_status = payment_status  



class Reservation:
    def __init__(self, reservation_id, customer_id, date, time, number_of_people, special_request):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.date = date
        self.time = time
        self.number_of_people = number_of_people
        self.special_request = special_request




class Registeruser:
    def __init__(self, email, phone, dob, height, weight, account_id , username, password):
        self.email=email
        self.phone=phone
        self.dob=dob
        self.height=height
        self.weight=weight
        self.account_id=account_id
        self.username=username
        self.password=password

            # 'email': email,
            # 'phone': phone,
            # 'dob': dob,
            # 'height': height,
            # 'weight': weight,
            # to the database





def fetchmenu():
    query = "SELECT * FROM aesthetic_res.menu;"
    if db_connection and db_connection.is_connected():
         result=execute_query(db_connection, query)
    menulist=[]
    for i in result:
        pic=i[3].split(",")
        ing=i[4].split(", ")
        menulist.append(Menu(i[0],i[1],i[2],pic, ing,i[5]))
    return menulist


def fetchmenu_byid(itemid):
    query = f"SELECT * FROM aesthetic_res.menu where itemid={itemid};"
    if db_connection and db_connection.is_connected():
         result=execute_query(db_connection, query)
    menulist=[]
    for i in result:
        pic=i[3].split(",")
        ing=i[4].split(", ")
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
        
    # return Customer(i[0], i[1], i[2].date(), i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10])




def fetch_reviews():
    """
    Fetch all reviews from the database, including customer details.
    """
    query = """
        SELECT r.Review_ID, r.Content, r.Date, c.Name AS Customer_Name 
        FROM aesthetic_res.review r 
        JOIN aesthetic_res.customer c ON r.Customer_ID = c.Customer_ID 
        ORDER BY r.Date DESC;
    """
    if db_connection and db_connection.is_connected():
        result = execute_query(db_connection, query)
    reviews = []
    for i in result:
        reviews.append({
            "review_id": i[0],
            "content": i[1],
            "date": i[2],
            "customer_name": i[3]
        })
    return reviews


def add_review(customer_id, content):
    """
    Add a new review to the database.
    """
    query = f"""
        INSERT INTO `aesthetic_res`.`review` (`Customer_ID`, `Date`, `Content`) 
        VALUES ('{customer_id}', CURDATE(), '{content}');
    """
    if db_connection and db_connection.is_connected():
        execute_query(db_connection, query)
        db_connection.commit()
    print("Review added successfully")

