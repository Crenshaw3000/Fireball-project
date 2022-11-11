"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session,redirect, jsonify, send_from_directory, url_for
import cloudinary.uploader
from model import Locator, User, Saved, connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
# import requests
# from werkzeug.utils import secure_filename
# import bcrypt


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# UPLOAD_FOLDER = 'static/uploads'
# # ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

GOOGLE_KEY=os.environ['GOOGLE_KEY']
CLOUDINARY_KEY=os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET=os.environ['CLOUDINARY_SECRET']
CLOUD_NAME="dtxtrrnee"

# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_profile_pic')
def upload_form():
	return render_template('profile.html')

@app.route('/upload_profile_pic', methods=['POST'])
def upload_image():
    user = User.query.filter(User.email==session["user_email"]).first()
    my_file = request.files['my-file']

    result = cloudinary.uploader.upload(my_file,
    api_key=CLOUDINARY_KEY,
    api_secret=CLOUDINARY_SECRET,
    cloud_name=CLOUD_NAME)

    img_url = result['secure_url']

    
    if img_url:
        user.profile_url = img_url
        db.session.commit()
        flash(f"Profile picture uploaded.")

    return redirect("/profile")


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
    fave_anime = request.form.get("fave_anime")
    profile_url = request.form.get("profile_url")

    user = crud.get_user_by_email(email)

    if user:
        flash("An account with this email already exists.")
    else:
        user = crud.create_user(fname, lname, email, password, fave_anime, profile_url)
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
        flash("This email or password is not correct. Try again.")
    else:
        session["user_email"]=match.email
        flash("Logged in!")
    
    return redirect("/")

@app.route('/profile')
def show_user_details():
    """Shows users profile if logged-in"""
    signed_in_email=session.get("user_email")

    if signed_in_email is None:
        flash(f"You must be signed in!")
        return redirect("/")

    else:  
        user = User.query.filter(User.email==session["user_email"]).first()

    return render_template("profile.html", user=user)

@app.route('/update_profile', methods=["GET"])
def get_update_profile_form():
    """ Shows profile form"""
    return render_template("update_profile.html")

@app.route('/update_profile', methods=["POST"])
def update_profile():
    """Update details in profile page"""
    signed_in_email=session.get("user_email")
    user = User.query.filter(User.email==session["user_email"]).first()

    if signed_in_email is None:
        flash(f"You must be signed in!")
        return redirect("/")

    
    new_fname = request.form.get('fname')
    new_lname = request.form.get('lname')
    new_fave_anime = request.form.get('fave_anime')

    # new_email = request.form.get('email')

    if new_fname:
        user.fname = new_fname
        db.session.commit()
        flash(f"First name was updated.")


    if new_lname:
        user.lname = new_lname
        db.session.commit()
        flash(f"Last name was updated.")


    # if new_profile_pic:
    #     user.new_profile_pic: = new_profile_pic
    #     db.session.commit()
    #     flash(f"Profile photo was updated")


    if new_fave_anime:
        user.fave_anime = new_fave_anime
        db.session.commit()
        flash(f"Favorite anime was updated.")
    return redirect("/profile")

@app.route('/change_password', methods=["GET"])
def change_password_form():
    """ Shows change password form"""
    return render_template("change_password.html")


@app.route('/change_password', methods=["POST"])
def change_password():
    """Updates password form update profile page"""
    signed_in_email=session.get("user_email")
    user = User.query.filter(User.email==session["user_email"]).first()

    updated_new_password = request.form.get('new_password')
    updated_confirm_password = request.form.get('confirm_password')

    if signed_in_email is None:
        flash(f"You must be signed in!")
        return redirect("/")

    if updated_new_password != updated_confirm_password:
        flash(f"The passwords do not match. Please try again.")

    if updated_new_password == updated_confirm_password:
        user.password = updated_new_password
        db.session.commit()
        flash(f"The password was updated.")

    return redirect("/profile")



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
    """Save a fireball"""

    signed_in_email=session.get("user_email")

    if signed_in_email is None:
        flash(f"You must be signed in!")
        return redirect("/")

    # locator_id= request.form.get('fireballs_id')
    user = User.query.filter(User.email==session["user_email"]).first()
    map_save=Saved.query.filter(Saved.user_id == user.user_id, Saved.locator_id== locator_id).first()
    list_of_saves = Saved.query.filter(Saved.user_id == user.user_id).all()
    
    if map_save in list_of_saves:
        flash(f"You saved this fireball already.")

    elif map_save in list_of_saves:
        # user = crud.get_user_by_email(signed_in_email)
        locator = crud.get_location_by_coordinates(locator_id)

        save = crud.create_saved_location(user, locator)
        db.session.add(save)
        db.session.commit()
        flash(f"You saved the coordinates for the fireball with this date and time: {locator.date}")

    return redirect(f'/fireballs/{locator_id}')

@app.route("/my_saved_fireballs")
def my_fireball_saves():
    """Display fireball saved"""
    
    signed_in_email=session.get("user_email")

    if signed_in_email is None:
        flash(f"You must be signed in!")
        return redirect("/")
    # user_id = session.get("user_id")
    # user_id = session["user_id"]
    # print(user_id)
    # my_saves=Saved.query.filter.all()
    else:
        user = User.query.filter(User.email==session["user_email"]).first()
    # print(user)
    # print("*******")
    # print(session['user_id'])
        my_saves=Saved.query.filter(Saved.user_id == user.user_id).all()
    # my_saves = crud.get_saves_by_user('user_id')
    # print(my_saves)
    return render_template("my_saved_fireballs.html", my_saves=my_saves, user=user)

@app.route('/delete_saved_fireball', methods=["POST"])
def delete_fireball():
    """Delete a saved fireball"""

    signed_in_email=session.get("user_email")
    # user = crud.get_user_by_email(signed_in_email)
    # print(signed_in_email)

    if signed_in_email is None:
        flash(f"You must be signed in!")
        return redirect("/")

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
    # # print(signed_in_email)
 
    if signed_in_email is None:
        flash(f"You must be signed in!")
        return redirect("/")

    locator_id= request.form.get('fireballs_id')
    user = User.query.filter(User.email==session["user_email"]).first()
    map_save=Saved.query.filter(Saved.user_id == user.user_id, Saved.locator_id== locator_id).first()
    list_of_saves = Saved.query.filter(Saved.user_id == user.user_id).all()

    # print(locator_id)
    # print(list_of_saves)
    # print("***")
    # print(map_save)
    # print("***&&****")
    # print(list_of_saves)
    # print("**((*****((((")

    # for save in list_of_saves:
    if map_save in list_of_saves:
        flash(f"You saved this fireball already.")
        # print("you *** already **")

    elif map_save in list_of_saves:

        # user = User.query.filter(User.email==session["user_email"]).first()
        # locator_id = Saved.query.filter(Saved.user_id == user.user_id).all()
        save_fire = crud.create_location_by_map(user, locator_id)
        print(save_fire)
        db.session.add(save_fire)
        db.session.commit()
        flash(f"You added this fireball to you saves")


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
