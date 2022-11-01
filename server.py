"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session,redirect, jsonify, send_from_directory
from model import Locator, connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

GOOGLE_KEY=os.environ['GOOGLE_KEY']


@app.route('/')
def homepage():
    """"Return render template to homepage.html"""

    return render_template('homepage.html')

@app.route("/map/basic")
def view_basic_map():
    """Demo of basic map-related code."""

    return render_template("map-basic.html")

@app.route('/about')
def about():
    """View about page"""

    return render_template("about.html")


@app.route('/data_visualization')
def data_visualization():
    """View Data Visualization page"""
    
    return render_template("data_visualization.html")


@app.route('/prediction')
def  prediction():
    """View fireball prediction model page"""

    return render_template("prediction.html")


@app.route('/users', methods=['POST'])
def register_user():
    """Create new user account"""
    fname = request.form.get("fname")
    lname =  request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user:
        flash("An account with this email already exists.")
    else:
        user = crud.create_user(fname, lname, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please log in.")
    
    return redirect("/")


@app.route('/login', methods=['POST'])
def login_user():
    """Login to user account"""

    email = request.form.get("email")
    password = request.form.get("password")

    match = crud.check_email_and_pass(email, password)

    if not match:
        flash("This email is not correct. Try again.")
    else:
        session["user_email"]=match.email
        flash("Logged in!")
    
    return redirect("/")

@app.route('/users/<email>')
def show_user_details(email):

    user = crud.get_user_individual(email)
    saved = user.saved

    return render_template("user_details.html", user=user, saved=saved)

@app.route("/map/fireballs")
def view_fireball_map():
    """Show map off fireballs."""

    return render_template("map-fireballs.html", GOOGLE_KEY=GOOGLE_KEY)


@app.route("/api/fireballs")
def fireball_info():
    """JSON information about fireballs."""

    fireballs = [
        {
            "id": locator.locator_id,
            "date": locator.date,
            "latitude": locator.latitude,
            "longitude": locator.longitude,
            "ImpactEnergy": locator.energy
        }
        for locator in Locator.query.limit(50)
    ]
    print(fireballs)
    return jsonify(fireballs)

# def convert():
#     if 'N' or 'E' in locator.latitude:
#         .replace('N', ' ')
#     if 'E' in locator.latitude:
#          .replace('E, ' ')



# @app.route("/map/static/<path:resource>")
# def get_resource(resource):
#     return send_from_directory("static", resource)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
