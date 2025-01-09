

#import
import controller
import model
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime, timedelta  # Import timedelta along with datetime
import os
from werkzeug.utils import secure_filename

#global

user = None #storing user object when logged in
admin = False #checks if account is admin
staff=False #checks for staff account



# initiating app.py
app = Flask(__name__)


#initializing

# Define the upload folder (make sure this folder exists)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#routing traffic


@app.route("/")
def home():
    global user, admin, staff, staff
    return render_template("index.html", title="Home", user=user, admin=admin, staff=staff)


@app.route("/logout")
def logout():
    global user, admin, staff
    user=None
    admin=False
    return redirect(url_for('login'))



@app.route("/login", methods=["GET", "POST"])
def login():
    global user, admin, staff

    if request.method == 'POST':
        # Fetch form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Save user data (in-memory storage for demonstration)

        user=controller.authenticate_user(username, password)
        

        if user:
            if user=="admin":
                admin=True
                user=None
                return redirect(url_for('home'))
            # elif user=="staff":
            #     staff=True
            #     return redirect(url_for('profile'))
            
            else:
            # Redirect to login page after successful profile creation
                return redirect(url_for('profile'))
        else:
            errortext="Incorrect username or password"
            return render_template('login.html', title="Login", errortext=errortext, user=user, admin=admin, staff=staff)

    # Render the login form
    return render_template('login.html', title="Login", user=user, admin=admin, staff=staff)

    



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

        # Redirect to login page after successful profile creation
        return redirect(url_for('login'))

    # Render the register form

    return render_template('register.html', title="Register")  # Display the sign-in form



@app.route("/profile", methods=['GET', 'POST'])
def profile():
    global user, admin, staff

    if user:
        
        if request.method == 'POST':
        
            name = request.form.get('inputName')
            email = request.form.get('inputEmail')
            phone = request.form.get('inputPhoneNo')
            address = request.form.get('inputAddress')
            dob = request.form.get('inputDateofBirth')
            allergens = request.form.get('inputAllergens')
            height = request.form.get('inputHeight')
            weight = request.form.get('inputWeight')
            ing = request.form.get('inputPreferredIngredients')
            masala = request.form.get('inputMasalaLevel')

            user=model.Customer(user.customer_id, name, dob, phone, email, allergens, height, weight, address, ing, masala)
            model.updateprofile(user)

            model.updateprofile(user)
            return redirect(url_for('logout'))
            

        else:
            return render_template("profile.html", title="Profile", user=user, admin=admin, staff=staff)




    else:
        error="Login error"
        error_text="Please login first then access the profile page."
        return render_template("error.html", title="Error", error=error, error_text=error_text)



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

    return render_template('staff_dashboard.html', staff_members=filtered_staff_members, current_month=datetime.now().month, current_year=datetime.now().year, user=user, admin=admin, staff=staff)

@app.route("/staff_profile/<int:staff_id>")
def staff_profile(staff_id):
    # Get the staff member by ID
    # staff = next((staff for staff in controller.staff_members if staff['id'] == staff_id), None)

    # If the staff member doesn't exist, redirect to the staff dashboard
    if staff is None:
        return redirect(url_for('staff_dashboard'))

    # Calculate total working hours for the week
    total_weekly_hours = sum([controller.calculate_hours(staff['hours'][day]['start'], staff['hours'][day]['end']) for day in range(7)
                              if staff['hours'][day]['start'] and staff['hours'][day]['end']])

    return render_template("staff_profile.html", staff=staff, total_weekly_hours=total_weekly_hours, user=user, admin=admin)



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
    global user, admin, staff
    return render_template('view_schedule.html', staff_members=controller.staff_members, user=user, admin=admin, staff=staff)


@app.route("/contact")
def contact():
    global user, admin, staff
    return render_template("contact.html", title="Contact Us", user=user, admin=admin, staff=staff)

@app.route("/reservation")
def reservation():
    global user, admin, staff

    return render_template("reservation.html", title="Reservation", user=user, admin=admin, staff=staff)


@app.route('/ordersummary')
def ordersummary():
    global user, admin, staff

    # Sample order data
    ordersummary = [
        ['order date','order id', ['Cake', 'A vanilla cake']],
        ['order date','order id', ['Cake', 'A vanilla cake']],
    ]
    return render_template('order_summary.html', title="Order Summary", ordersummary=ordersummary, user=user, admin=admin, staff=staff)



@app.route("/aboutus")
def aboutus():
    global user, admin, staff
    return render_template("aboutus.html", title="Ahout Us", user=user, admin=admin, staff=staff)



@app.route('/menu', defaults={'item_id': None})
@app.route('/menu/<item_id>', methods=['GET', 'POST'])
def menu(item_id):
    global user, admin, staff

    if item_id==None: 
        menu=model.fetchmenu()
        if user:
            print(user)
            recommended=controller.recommendeditem(user)
            return render_template('menu.html', title="Menu", menu=menu, recommended=recommended, user=user, admin=admin, staff=staff)
        else:
            print("no user")
            return render_template('menu.html', title="Menu", menu=menu, user=None, admin=admin)
    else:
        item=model.fetchmenu_byid(item_id)
        print(item.ingredients)
        allergic=None
        if user:
            allergic=controller.allergic(user,item)
        if admin:
            if request.method == 'POST':
                name = request.form.get('inputName')
                description = request.form.get('description')
                ingredients = request.form.get('ingredients')
                price = request.form.get('price')
                new_item=model.Menu(item_id, name, description, item.pictures, ingredients, price, )
                model.updatemenu(new_item)
                return redirect(url_for('menu'))
        return render_template('menu-description.html', title=f"{item.name}", item=item, allergic=allergic, user=user, admin=admin, staff=staff)
    

# @app.route('/menu', defaults={'item_id': None})
@app.route('/addmenu' , methods=['GET', 'POST'])
def addmenu():
    global user, admin, staff

    if admin:
        if request.method == 'POST':
        
            name = request.form.get('inputName')
            description = request.form.get('description')
            ingredients = request.form.get('ingredients')
            price = request.form.get('price')
            pictures=[]


            
            files = request.files.getlist('menuimage')  # Get all files

            # Process each file
            for file in files:
                if file.filename == '':
                    return "No selected file", 400
                
                # Save the file (you can validate file type/size before saving)
                file.save(f"static/{file.filename}")
                pictures.append(file.filename)


            print(pictures)
            item=model.Menu(0, name, description, pictures, ingredients, price, )
            model.addmenu(item)
            return redirect(url_for('menu'))




@app.route('/deletemenu/<item_id>')
def deletemenu(item_id):
    global user, admin, staff

    if admin:
        model.deleteitem(item_id)
        return redirect(url_for('menu'))



    
    




@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    global user, admin, staff
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

    return render_template('admin_dashboard.html', menu=menu, user=user, admin=admin, staff=staff)



# Sample reviews data


# @app.route('/reviews', methods=['GET'])
# def reviews_page():
#     global user, admin, staff
#     REVIEWS_PER_PAGE= 12

#     # Get the current page number from the query parameters
#     page = int(request.args.get('page', 1))
    
#     # Calculate start and end indices for pagination
#     start = (page - 1) * REVIEWS_PER_PAGE
#     end = start + REVIEWS_PER_PAGE
    
#     # Paginated reviews
#     paginated_reviews = reviews[start:end]
    
#     # Determine if there are more reviews to load
#     has_more = end < len(reviews)
    
#     # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # For AJAX requests
#     #     return ({
#     #         'reviews': paginated_reviews,
#     #         'has_more': has_more
#     #     })
    
#     return render_template('reviews.html', title='Reviews', reviews=paginated_reviews, has_more=has_more, page=page, user=user, admin=admin, staff=staff)

    # Pass all reviews to the template
#  return render_template('reviews.html', title='Reviews', reviews=reviews, user=user, admin=admin, staff=staff)

# @app.route('/reviews', methods=['GET', 'POST'])
# def reviews_page():
#     if request.method == 'POST':
#         # Ensure user is logged in
#         if not user:
#             error = "Please log in to submit a review."
#             return render_template('error.html', title="Error", error=error)

#         # Get review content
#         content = request.form.get('review_content')
#         if not content:
#             error = "Review content cannot be empty."
#             return render_template('error.html', title="Error", error=error)

#         # Submit the review
#         add_review(user.customer_id, content)
#         return redirect(url_for('reviews_page'))

#     # Fetch and display reviews
#     all_reviews = fetch_reviews()
#     return render_template('reviews.html', title="Reviews", reviews=all_reviews, user=user)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews_page():
    reviews= controller.reviews
    if request.method == 'POST':
        # Extract data from the form
        review_content = request.form.get('review_content')
        name = "Anonymous User"  # Default name for simplicity
        image_url = "https://via.placeholder.com/50"  # Default profile image
        date = datetime.now().strftime("%B %d, %Y")

        # Append the new review to the list
        reviews.append([name, image_url, review_content, date])

        return redirect(url_for('reviews_page'))

    # Render reviews page
    return render_template('reviews.html', title="Customer Reviews", reviews=reviews)




#executing file
if __name__ == "__main__":
    app.run(debug=True)


