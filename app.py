from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html", title="Home")



@app.route("/contact")
def home():
    return render_template("contact.html", title="Contact Us")



@app.route("/order_summary")
def home():
    return render_template("contact.html", title="Order Summary")



@app.route("/reservation")
def home():
    return render_template("contact.html", title="Reservation")



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
