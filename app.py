
#import
from flask import Flask, render_template, request, redirect, url_for




#global

users = [] # In-memory storage for user data
userlogin=True #track if user is logged in
meaw="cat"




#code


# initiating app.py
app = Flask(__name__)






#setting up 


#routing traffic

@app.route("/")
def home():
    return render_template("index.html", title="Home")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # Fetch form data
        username = request.form.get('username')
        password = request.form.get('password')


        # Save user data (in-memory storage for demonstration)
        new_user = {
            'username': username,
            'password': password,
        }
        users.append(new_user)
        # print(new_user)

        # Redirect to login page after successful profile creation
        return redirect(url_for('login'))

    # Render the login form
    return render_template('login.html', title="Login")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # Fetch form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        height = request.form.get('height')
        weight = request.form.get('weight')

        # Basic password validation
        if password != confirm_password:
            return "Passwords do not match", 400

        # Save user data (in-memory storage for demonstration)
        new_user = {
            'username': username,
            'email': email,
            'phone': phone,
            'dob': dob,
            'height': height,
            'weight': weight,
        }
        users.append(new_user)
        # print(new_user)

        # Redirect to login page after successful profile creation
        return redirect(url_for('login'))

    # Render the register form
    return render_template('register.html', title="Register")  # Display the sign-in form



@app.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")



@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Us")



@app.route('/ordersummary')
def ordersummary():
    # Sample order data
    ordersummary = [
        ['order date','order id', ['Cake', 'A vanilla cake']],
        ['order date','order id', ['Cake', 'A vanilla cake']],
    ]
    return render_template('order_summary.html', title="Order Summary", ordersummary=ordersummary)



@app.route("/reservation")
def reservation():
    return render_template("reservation.html", title="Reservation")


@app.route('/menu', defaults={'item_id': None})
@app.route('/menu/<item_id>')
def menu(item_id):
    global userlogin

    if item_id==None: #render menu page

        # Sample menu data
        menu = [
            ['item_id_1', 'Cake', 'A vanilla cake', "A description of the item"],
            ['item_id_2', 'Cake', 'A vanilla cake', "A description of the item"],
            ['item_id_3', 'Cake', 'A vanilla cake', "A description of the item"],
        ]

        return render_template('menu.html', title="Menu", menu=menu, userlogin=userlogin)
    

    else: #render item description page

        
        class dish:
            # Constructor to initialize the object with name and age
            def __init__(self, name, item_id, description, picture, ingriedients, price):
                self.name = name
                self.id = item_id
                self.description=description
                self.picture=picture
                self.ingriedients=ingriedients
                self.price=price

        item=dish("meaw", 1234, "Descrition of athe item from the db", "A list of the pictures", ["spices", "mayo"], 12.50)

        return render_template('menu-description.html', title=f"{item_id}", item=item)



#executing file
if __name__ == "__main__":
    app.run(debug=True)