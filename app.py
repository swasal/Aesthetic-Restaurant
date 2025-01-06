
#import
import controller
import model
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime, timedelta  # Import timedelta along with datetime







# Initiating Flask app
app = Flask(__name__)

# Routing traffic





#global

user = None #storing user object when logged in
admin = True #checks if account is admin




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
    global user
    return render_template("index.html", title="Home", user=user)


@app.route("/logout")
def logout():
    global user
    user=None
    admin=False
    return redirect(url_for('login'))



@app.route("/login", methods=["GET", "POST"])
def login():
    global user

    if request.method == 'POST':
        # Fetch form data
        username = request.form.get('username')
        password = request.form.get('password')


        # Save user data (in-memory storage for demonstration)
        user=controller.authenticate_user(username, password)

        if user:
            # Redirect to login page after successful profile creation
            return redirect(url_for('profile'))
        else:
            errortext="Incorrect username or password"
            return render_template('login.html', title="Login", errortext=errortext, user=user)

    # Render the login form
    return render_template('login.html', title="Login", user=user)

    



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



@app.route("/profile", methods=['GET', 'POST'])
def profile():
    global user

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
            return render_template("profile.html", title="Profile", user=user)




    else:
        error="Login error"
        error_text="Please login first then access the profile page."
        return render_template("error.html", title="Error", error=error, error_text=error_text)



@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Us", user=user)



@app.route('/ordersummary')
def ordersummary():
    global user

    # Sample order data
    ordersummary = [
        ['order date','order id', ['Cake', 'A vanilla cake']],
        ['order date','order id', ['Cake', 'A vanilla cake']],
    ]
    return render_template('order_summary.html', title="Order Summary", ordersummary=ordersummary, user=user)



@app.route("/reservation")
def reservation():
    global user

    return render_template("reservation.html", title="Reservation", user=user)



def menupicture(filename):
    return send_from_directory('menupicture', filename)



@app.route('/menu', defaults={'item_id': None})
@app.route('/menu/<item_id>', methods=['GET', 'POST'])
def menu(item_id):
    global user

    if item_id==None: 
        menu=model.fetchmenu()
        if user:
            print(user)
            recommended=controller.recommendations(user)
            return render_template('menu.html', title="Menu", menu=menu, recommended=recommended, user=user)
        else:
            print("no user")
            return render_template('menu.html', title="Menu", menu=menu, user=None)
    else:
        item=model.fetchmenu_byid(item_id)
        if admin:
            if request.method == 'POST':
                name = request.form.get('inputName')
                description = request.form.get('description')
                ingredients = request.form.get('ingredients')
                price = request.form.get('price')

                print()
                new_item=model.Menu(item_id, name, description, item.pictures, ingredients, price, )
                model.updatemenu(new_item)
                return redirect(url_for('menu'))

        return render_template('menu-description.html', title=f"{item.name}", item=item, user=user)
    


# @app.route('/menu', defaults={'item_id': None})
@app.route('/addmenu' , methods=['GET', 'POST'])
def addmenu():
    global user, admin

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
    global user

    if admin:
        model.deleteitem(item_id)
        return redirect(url_for('menu'))



    
    




@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    global user
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

    return render_template('admin_dashboard.html', menu=menu, user=user)



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
    global user
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
    
    return render_template('reviews.html', title='Reviews', reviews=paginated_reviews, has_more=has_more, page=page, user=user)





#executing file
if __name__ == "__main__":
    app.run(debug=True)