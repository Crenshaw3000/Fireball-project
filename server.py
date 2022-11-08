"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session,redirect, jsonify, send_from_directory
from model import Locator, User, Saved, connect_to_db, db
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

# @app.route('/user_details')
# def show_user_details():

#     email = request.form.get("email")
#     user = crud.get_user_by_email(email)
#     # saves = Saved.query.all()

#     if email not in session:
#         flash("You are not logged-in")
    
#     # user = User.query.get(session['user_email'])
#     # email=session.get("user_email")

#     # saved = user.saved
#     # if user==email:

#     return render_template("user_details.html", user=user)

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
        for locator in Locator.query.limit(150)
    ]
    print(fireballs)
    return jsonify(fireballs)

@app.route("/fireballs")
def all_fireballs():
    """View all fireballs."""

    fireballs = crud.get_fireballs()

    return render_template("all_fireballs.html", fireballs=fireballs)


@app.route('/fireballs/<locator_id>')
def show_fireball_details(locator_id):
    """Show fireball details"""

    fireball = crud.get_location_by_coordinates(locator_id)

    return render_template("fireball_details.html", fireball=fireball)


@app.route('/fireballs/<locator_id>/save', methods=["POST"])
def save_location(locator_id):
    """Show new save"""

    signed_in_email=session.get("user_email")

    if signed_in_email is None:
        flash(f"You must be signed in!")

    else: 
        user = crud.get_user_by_email(signed_in_email)
        locator = crud.get_location_by_coordinates(locator_id)

        save = crud.create_saved_location(user, locator)
        db.session.add(save)
        db.session.commit()
        flash(f"You saved the coordinates for the fireball with this date and time: {locator.date}")

    return redirect(f'/fireballs/{locator_id}')

@app.route("/my_saved_fireballs")
def my_fireball_saves():
    """Display fireball saved"""

    # user_id = session.get("user_id")
    # user_id = session["user_id"]
    # print(user_id)
    # my_saves=Saved.query.filter.all()
    user = User.query.filter(User.email==session["user_email"]).first()
    # print(user)
    # print("*******")
    # print(session['user_id'])
    my_saves=Saved.query.filter(Saved.user_id == user.user_id).all()
    # my_saves = crud.get_saves_by_user('user_id')
    print(my_saves)
    return render_template("my_saved_fireballs.html", my_saves=my_saves, user=user)

@app.route('/delete_saved_fireball', methods=["POST"])
def delete_fireball():
    """Delete a saved fireball"""

    signed_in_email=session.get("user_email")
    # user = crud.get_user_by_email(signed_in_email)
    print(signed_in_email)

    if signed_in_email is None:
        flash(f"You must be signed in!")

    else: 
        user= User.query.filter(User.email==session["user_email"]).first()
        locator_id = request.form.get('fireball_id')
        # print(user)
        # print(locator_id)
        remove = crud.remove_saved_location(user, locator_id)
        # print(remove)
        db.session.delete(remove)
        db.session.commit()
        flash(f"You deleted this fireball from your saves")


        return redirect("/my_saved_fireballs")

@app.route('/save_fireball', methods=["POST"])
def save_fireball_from_map():
    """Save fireball from map"""

    signed_in_email=session.get("user_email")
    print(signed_in_email)
    locator_id= request.form.get('fireballs_id')
    user = User.query.filter(User.email==session["user_email"]).first()
    list_of_saves=Saved.query.filter(Saved.user_id == user.user_id).all()


    if signed_in_email is None:
        flash(f"You must be signed in!")
    
    elif locator_id not in list_of_saves:    
    # locator_id= request.form.get('fireballs_id')
        print(user)
        print(locator_id)
    
        save_fire = crud.create_location_by_map(user, locator_id)
        print(save_fire)
        db.session.add(save_fire)
        db.session.commit()
        flash(f"You added this fireball to you saves")
        
  
    else:
        flash(f"You saved this fireball already.")

    return redirect("/my_saved_fireballs")


@app.route("/logout", methods=["GET"])
def logout():
    """ log out current user"""
    # print("this is the session before we do session pop")
    print(session)
    session.pop("user_email", None)
    # print("this is the session after we do session pop")
    print(session)

    flash("You are now logged out")

    return redirect("/")




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
