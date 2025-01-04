"""This file contains all the functions that serve as controller"""

# imports



#global
userlist=object() #list of all usrr objects fteched from model.py



# codes

def BMI(weight:int, height:int, ):
    """Make sure the weight is in Kilograms(KG) and
    height is in centimetres (cm)"""

    bmi=weight/height
    return


def authenticate_user(username, password):
    for user in userlist: