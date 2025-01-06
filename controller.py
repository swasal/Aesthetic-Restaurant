"""This file contains all the functions that serve as controller"""

# imports
import model



#global
userlist=object() #list of all usrr objects fteched from model.py



# codes

def BMI(weight:int, height:int, ):
    """Make sure the weight is in Kilograms(KG) and
    height is in centimetres (cm)"""

    bmi=weight/height
    return


def authenticate_user(username, password):
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


def recommendations(customer):
    allergens=customer.allergens.split(",")
    
    menu=model.fetchmenu()

    recommendedlist=[]
    for item in menu:
        if item.ingredients not in allergens:
            recommendedlist.append(item)

    return recommendedlist
            
    
