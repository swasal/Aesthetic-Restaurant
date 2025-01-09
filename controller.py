"""This file contains all the functions that serve as controller"""

# imports
import model
import random



#global
userlist=object() #list of all usrr objects fteched from model.py

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


reviews = [
    ['Jean Tang', 'https://via.placeholder.com/50', '可以搭地鐵再轉搭免費公車上山，很方便。看夕陽，看洛杉磯夜景的好地方。', '2 days ago'],
    ['محمد جواد حبیبی', 'https://via.placeholder.com/50', 'من بیمه عمر خریدم و بعد از 1 سال واقعا احساس ثروتمندی میکنم', '2 days ago'],
    ['Daniel White', 'https://via.placeholder.com/50', 'Great views of the surrounding area and interesting exhibits. Highly recommend!', '4 days ago'],
    ['Breanne F', 'https://via.placeholder.com/50', 'Easy hike and not too busy on weekend evenings during early December!', '4 days ago'],
    ['Hamza Amin', 'https://via.placeholder.com/50', 'Excellent quality of product. Tried honey nuts and they are amazing. Highly recommend.', '5 days ago'],
    ['Ali Muhammad', 'https://via.placeholder.com/50', 'Great customer service and fantastic ambiance!', '6 days ago'],
    ['Carol Lloyd', 'https://via.placeholder.com/50', 'The dishes were delightful and the staff was very attentive.', '7 days ago']
]

# codes

def BMI(weight:int, height:int, ):
    """Make sure the weight is in Kilograms(KG) and
    height is in centimetres (cm)"""

    bmi=weight/height
    return



def authenticate_user(username, password):
    if username=="admin" and password=="admin":
        return 'admin'


    user=model.fetchuser_byusername(username)
    if user!=None:
        if user.password==password:
            return model.fetchcustomer_by_customerid(user.account_id)
    else:
        return None
    


def register(username:str, email:str, password, confirm_password, phone:int, dob, height, weight):
    pass



def find_matching_items(list1, list2):
    matching_items = [item for item in list1 if item in list2]
    return matching_items


def recommendeditem(customer):
    # allergens=customer.allergens.split(", ")
    menu=model.fetchmenu()
    recommendedlist=[]
    for item in menu:
        if allergic(customer, item) is False:
            recommendedlist.append(item)
            print(item.name)

    return random.choice(recommendedlist)
            

def allergic(customer, item):
    allergens=customer.allergens.split(", ")

    for i in item.ingredients:
        if i in allergens:
            return True

    return False

# Function to calculate hours worked
def calculate_salary(role, hours_worked):
    """Calculate the salary for a staff member based on their role and worked hours."""
    hourly_wages = {
        'Manager': 30,
        'Waiter': 15,
        'Head Chef': 25,
        'Assistant Chef': 20,
        'Cleaner Staff': 12
    }
    
    hourly_wage = hourly_wages.get(role, 0)  # Default to 0 if role is not found
    return hourly_wage * hours_worked

def calculate_total_salary(staff_member):
    """Calculate the total weekly and monthly salary based on staff schedule."""
    total_weekly_hours = 0
    total_weekly_salary = 0
    
    for day in range(7):  # 7 days of the week
        if not staff_member['leave'][day]:  # If not on leave, calculate hours
            start_time = staff_member['hours'][day]['start']
            end_time = staff_member['hours'][day]['end']
            
            if start_time and end_time:  # Ensure that the times are valid
                worked_hours = calculate_hours(start_time, end_time)
                total_weekly_hours += worked_hours
                total_weekly_salary += calculate_salary(staff_member['role'], worked_hours)

    # Monthly salary: Assume 4 weeks per month
    monthly_salary = total_weekly_salary * 4  # This calculation assumes 4 weeks in a month
    return total_weekly_hours, total_weekly_salary, monthly_salary

def calculate_hours(start_time, end_time):
    """Calculate hours worked between the start and end time."""
    from datetime import datetime, timedelta
    
    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')
    
    # Handle cases where the end time is before the start time (e.g., overnight shifts)
    if end < start:
        end += timedelta(days=1)
    
    duration = (end - start).seconds / 3600  # Convert seconds to hours
    return duration



# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

