
#import
from flask import Flask, render_template, request, redirect, url_for




#global

users = [] # In-memory storage for user data



#code


# initiating app.py
app = Flask(__name__)







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
    return render_template('login.html')

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
    return render_template('register.html')  # Display the sign-in form



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

@app.route('/menu')
def menu():
    # Sample menu data
    menu = [
        ['item_id', 'Cake', 'A vanilla cake', "A description of the item"],
        ['item_id', 'Cake', 'A vanilla cake', "A description of the item"],
        ['item_id', 'Cake', 'A vanilla cake', "A description of the item"],
    ]
    return render_template('menu.html', title="Menu", menu=menu)
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    global menu
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            # Add a new menu item
            item_id = str(len(menu) + 1)
            name = request.form.get('name')
            description = request.form.get('description')
            details = request.form.get('details')
            if name and description and details:
                menu.append([item_id, name, description, details])
        elif action == 'delete':
            # Delete an item
            item_id = request.form.get('id')
            menu = [item for item in menu if item[0] != item_id]

    return render_template('admin_dashboard.html', title="Admin Dashboard", menu=menu)

if __name__ == "__main__":
    app.run(debug=True)