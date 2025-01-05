
#import
import controller
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta  # Import timedelta along with datetime

# Global variables for storing user data
users = []  # In-memory storage for user data

# Staff members data
staff_members = [
    {'id': 1, 'name': 'Tanvir', 'role': 'Manager', 'leave': [False] * 7, 'hours': [{'start': None, 'end': None}] * 7, 'total_hours': 0, 'monthly_salary': 0},
    {'id': 2, 'name': 'Ahnaf', 'role': 'Waiter', 'leave': [False] * 7, 'hours': [{'start': None, 'end': None}] * 7, 'total_hours': 0, 'monthly_salary': 0},
]

# Staff hourly rates based on their role
staff_roles = {
    'Manager': 30,
    'Waiter': 15,
    'Head Chef': 25,
    'Assistant Chef': 20,
    'Cleaner Staff': 12,
}

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

# Define the upload folder (make sure this folder exists)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initiating Flask app
app = Flask(__name__)

# Routing traffic





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

        controller.register(username, email, password, confirm_password, phone, dob, height, weight)
        # # Save user data (in-memory storage for demonstration)
        # new_user = {
        #     'username': username,
        #     'email': email,
        #     'phone': phone,
        #     'dob': dob,
        #     'height': height,
        #     'weight': weight,
        # }
        # users.append(new_user)
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

  
@app.route('/menu')
def menu():
    global userlogin
    # Sample menu data
    menu = [
        ['item_id', 'Cake', 'A vanilla cake', "A description of the item"],
        ['item_id', 'Cake', 'A vanilla cake', "A description of the item"],
        ['item_id', 'Cake', 'A vanilla cake', "A description of the item"],
    ]
    return render_template('menu.html', title="Menu", menu=menu, userlogin=userlogin)




@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    # Local menu list
    menu = [
        ['1', 'Cake', 'A vanilla cake', "A delicious vanilla-flavored cake with frosting"],
        ['2', 'Pie', 'An apple pie', "A freshly baked apple pie with a flaky crust"],
        ['3', 'Cookie', 'Chocolate chip cookies', "Crunchy chocolate chip cookies with a hint of vanilla"],
    ]
    
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

    return render_template('admin_dashboard.html', menu=menu)



# Sample reviews data
reviews = [
    ['Jean Tang', 'https://via.placeholder.com/50', '可以搭地鐵再轉搭免費公車上山，很方便。看夕陽，看洛杉磯夜景的好地方。', '2 days ago'],
    ['محمد جواد حبیبی', 'https://via.placeholder.com/50', 'من بیمه عمر خریدم و بعد از 1 سال واقعا احساس ثروتمندی میکنم', '2 days ago'],
    ['Daniel White', 'https://via.placeholder.com/50', 'Great views of the surrounding area and interesting exhibits. Highly recommend!', '4 days ago'],
    ['Breanne F', 'https://via.placeholder.com/50', 'Easy hike and not too busy on weekend evenings during early December!', '4 days ago'],
    ['Hamza Amin', 'https://via.placeholder.com/50', 'Excellent quality of product. Tried honey nuts and they are amazing. Highly recommend.', '5 days ago'],
    ['Ali Muhammad', 'https://via.placeholder.com/50', 'Great customer service and fantastic ambiance!', '6 days ago'],
    ['Carol Lloyd', 'https://via.placeholder.com/50', 'The dishes were delightful and the staff was very attentive.', '7 days ago']
]

# Reviews per page
REVIEWS_PER_PAGE = 6

@app.route('/reviews', methods=['GET'])
def reviews_page():
    # Get the current page number from the query parameters
    page = int(request.args.get('page', 1))
    
    # Calculate start and end indices for pagination
    start = (page - 1) * REVIEWS_PER_PAGE
    end = start + REVIEWS_PER_PAGE
    
    # Paginated reviews
    paginated_reviews = reviews[start:end]
    
    # Determine if there are more reviews to load
    has_more = end < len(reviews)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # For AJAX requests
        return jsonify({
            'reviews': paginated_reviews,
            'has_more': has_more
        })
    
    return render_template('reviews.html', title='Reviews', reviews=paginated_reviews, has_more=has_more, page=page)





#executing file
if __name__ == "__main__":
    app.run(debug=True)