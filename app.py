import os
import controller
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta  # Import timedelta along with datetime

# Global variables for storing user data
users = []  # In-memory storage for user data

# Staff members data
# staff_members = [
#     {'id': 1, 'name': 'Tanvir', 'role': 'Manager', 'leave': [False] * 7, 'hours': [{'start': None, 'end': None}] * 7, 'total_hours': 0, 'monthly_salary': 0},
#     {'id': 2, 'name': 'Ahnaf', 'role': 'Waiter', 'leave': [False] * 7, 'hours': [{'start': None, 'end': None}] * 7, 'total_hours': 0, 'monthly_salary': 0},
# ]

# Staff hourly rates based on their role
# staff_roles = {
#     'Manager': 30,
#     'Waiter': 15,
#     'Head Chef': 25,
#     'Assistant Chef': 20,
#     'Cleaner Staff': 12,
# }


#global

users = [] # In-memory storage for user data
userlogin=True #track if user is logged in
meaw="cat"

# Define the upload folder (make sure this folder exists)
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


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

        # Handle file upload for profile picture
        if 'profile_picture' not in request.files:
            return "No file part", 400
        profile_picture = request.files['profile_picture']

        if profile_picture and controller.allowed_file(profile_picture.filename):
                    # Ensure the upload directory exists
                    if not os.path.exists(controller.UPLOAD_FOLDER):
                        os.makedirs(controller.UPLOAD_FOLDER)

                    # Secure the filename and save the file
                    filename = secure_filename(profile_picture.filename)
                    file_path = os.path.join(controller.UPLOAD_FOLDER, filename)
                    profile_picture.save(file_path)
        else:
            return "Invalid file format", 400

        # Save user data (including the file path for the profile picture)
        # new_user = {
        #     'username': username,
        #     'email': email,
        #     'phone': phone,
        #     'dob': dob,
        #     'height': height,
        #     'weight': weight,
        #     'profile_picture': file_path  # Store the file path of the profile picture
        # }
def __init__(self, username, email, phone, dob, height, weight, profile_picture):
        self.username = username
        self.email = email
        self.phone = phone
        self.dob = dob
        self.height = height
        self.weight = weight
        self.profile_picture = profile_picture
        # You can save this data in your database or any storage method you are using
        # users.append(new_user)

        # Redirect to login page after successful profile creation
        return redirect(url_for('login'))

    # Render the register form

    return render_template('register.html', title="Register")  # Display the sign-in form



@app.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")

@app.route("/staff_dashboard", methods=["GET", "POST"])
def staff_dashboard():
    # Get the search query from the GET request
    search_query = request.args.get('search', '').lower()  # Get the query from the URL
    
    # Filter staff based on the search query
    filtered_staff_members = [staff for staff in controller.staff_members if search_query in staff['name'].lower()] if search_query else controller.staff_members

    if request.method == 'POST':
        # Handle the staff schedule form submission here
        for staff in controller.staff_members:
            for day in range(7):
                start_time = request.form.get(f"start_{staff['id']}_{day}")
                end_time = request.form.get(f"end_{staff['id']}_{day}")
                is_on_leave = request.form.get(f"leave_{staff['id']}_{day}") == 'on'
                
                if is_on_leave:
                    staff['hours'][day] = {'start': None, 'end': None}
                else:
                    staff['hours'][day] = {'start': start_time, 'end': end_time}

                staff['leave'][day] = is_on_leave

        # Calculate weekly and monthly salaries for each staff member
        for staff in controller.staff_members:
            total_weekly_hours, total_weekly_salary, monthly_salary = controller.calculate_total_salary(staff)
            staff['total_hours'] = total_weekly_hours
            staff['weekly_salary'] = total_weekly_salary
            staff['monthly_salary'] = monthly_salary  # Monthly salary is calculated

        return redirect(url_for('staff_dashboard'))  # Redirect after saving

    return render_template('staff_dashboard.html', staff_members=filtered_staff_members, current_month=datetime.now().month, current_year=datetime.now().year)

@app.route("/staff_profile/<int:staff_id>")
def staff_profile(staff_id):
    # Get the staff member by ID
    staff = next((staff for staff in controller.staff_members if staff['id'] == staff_id), None)

    # If the staff member doesn't exist, redirect to the staff dashboard
    if staff is None:
        return redirect(url_for('staff_dashboard'))

    # Calculate total working hours for the week
    total_weekly_hours = sum([controller.calculate_hours(staff['hours'][day]['start'], staff['hours'][day]['end']) for day in range(7)
                              if staff['hours'][day]['start'] and staff['hours'][day]['end']])

    return render_template("staff_profile.html", staff=staff, total_weekly_hours=total_weekly_hours)

# Register a custom Jinja filter to calculate time difference in hours
@app.template_filter('time_diff')
def time_diff(end_time, start_time):
    # Convert string time to datetime objects
    start = datetime.strptime(start_time, '%H:%M')
    end = datetime.strptime(end_time, '%H:%M')
    
    # Handle cases where the end time is before the start time (e.g., overnight shifts)
    if end < start:
        end += timedelta(days=1)

    # Calculate the difference in hours
    duration = (end - start).seconds / 3600  # Convert seconds to hours
    return duration

@app.route('/view_schedule')
def view_schedule():
    return render_template('view_schedule.html', staff_members=controller.staff_members)


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
    
    # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # For AJAX requests
    #     return ({
    #         'reviews': paginated_reviews,
    #         'has_more': has_more
    #     })
    
    return render_template('reviews.html', title='Reviews', reviews=paginated_reviews, has_more=has_more, page=page)





#executing file
if __name__ == "__main__":
    app.run(debug=True)


