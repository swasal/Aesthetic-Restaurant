#import
from flask import Flask, render_template




#global



#code


# initiating app.py
app = Flask(__name__)



#routing traffic

@app.route("/")
def home():
    return render_template("index.html", title="Home")



@app.route("/login")
def login():
    return render_template("login.html", title="Login")



@app.route("/profile")
def profile():
    return render_template("profile.html", title="Profile")



@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact Us")



@app.route("/order_summary")
def order_summary():
    return render_template("order_summary.html", title="Order Summary")



@app.route("/reservation")
def reservation():
    return render_template("reservation.html", title="Reservation")



@app.route('/menu')
def menu():
    # Get champion data based on champion_id
    menu = [
        ['item_id', 'Cake', 'A vanilla cake', "A description of the item"],
        ['item_id', 'Cake', 'A vanilla cake', "A description of the item"],
        ['item_id', 'Cake', 'A vanilla cake', "A description of the item"],
    ]
    
    return render_template('menu.html', title="Menu", menu=menu)










if __name__ == "__main__":
    app.run(debug=True)
