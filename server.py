"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session,redirect, jsonify, send_from_directory, url_for
import cloudinary.uploader
from model import Locator, User, Saved, connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
import re



app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



GOOGLE_KEY=os.environ['GOOGLE_KEY']
CLOUDINARY_KEY=os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET=os.environ['CLOUDINARY_SECRET']
CLOUD_NAME="dtxtrrnee"



@app.route('/forgot_password',  methods=["GET"])
def get_reset_password_form():
    """ Shows form to get email to reset password"""

    return render_template("forgot_password.html")


@app.route('/forgot_password',  methods=["POST"])
def reset_password():
    """Takes user to security questions when user email is entered."""
    email= request.form.get("user_email")

    user = crud.get_user_by_email(email)
    
    if user is None:
        flash("Incorrect email! Try entering the email again.")
    
    if user:
        session["user_email"]=user.email
        flash("Follow the instructions below.")
   
    return redirect("/security_to_reset_pw")

@app.route('/security_to_reset_pw',  methods=["GET"])
def get_security_for_reset_form():
    """ Shows form to answer security questions when forgotten"""

    return render_template("security_to_reset_pw.html")

@app.route('/security_to_reset_pw',  methods=["POST"])
def ask_for_security_questions():
    """ When security questions are all correct takes user to profile """

    user = User.query.filter(User.email==session["user_email"]).first()

    security1_reset =request.form.get("security1_reset")
    security2_reset =request.form.get("security2_reset")
    security3_reset =request.form.get("security3_reset")

    if user.security1 == security1_reset and user.security2 == security2_reset and user.security3 == security3_reset:
        return redirect("/change_password")

    else:
        flash("At least one of the answers are not correct. Please try again.")


@app.route('/upload_profile_pic')
def upload_form():
    """ Shows form to upload a picture"""
	
    return render_template('profile.html')

@app.route('/upload_profile_pic', methods=['POST'])
def upload_image():
    """Upload photo and saves to database"""

    user = User.query.filter(User.email==session["user_email"]).first()
    my_file = request.files['my-file']

    try:
        result = cloudinary.uploader.upload(my_file,
        api_key=CLOUDINARY_KEY,
        api_secret=CLOUDINARY_SECRET,
        cloud_name=CLOUD_NAME)

        img_url = result['secure_url']    
        if img_url:
            user.profile_url = img_url
            db.session.commit()
            flash("Profile picture uploaded.")

    # if img_url is None:
    except:
        flash("Could not upload profile picture please try again.")

    return redirect("/profile")

@app.route('/delete_profile_pic', methods=['POST'])
def delete_profile_image():
    """Deletes photo from profile"""
    
    signed_in_email=session.get("user_email")
    
    if signed_in_email is None:
        flash("You must be signed in!")
        return redirect("/")
    
    else:

        user = User.query.filter(User.email==session["user_email"]).first()
        print(user)

        user.profile_url = "/static/images/profile.png"
        db.session.commit()
        flash("Profile picture deleted.")

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

@app.route('/register',  methods=["GET"])
def get_register_form():
    """ Shows register form """

    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register_user():
    """Create new user account"""
    fname = request.form.get("fname")
    lname =  request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    fave_anime = request.form.get("fave_anime")
    profile_url = "/static/images/profile.png"
    security1=request.form.get("security1")
    security2=request.form.get("security2")
    security3=request.form.get("security3")

    #Must have at least one upper case letter, one lower case letter, one number,
    #  one special symbol (@$!%*#?&) and 13 to 20 characters long
    mat_pass = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!*&]{13,20}$")

    mat_email = re.compile(r"[a-zA-Z0-9._]+\@(\w+)(\.)[a-z]{2,3}")


    if re.match(mat_email, email) and re.match(mat_pass, password):
        flash("Email is vaild")
            
        if security1 or security2 or security3 is True:
            flash("Security questions saved")

            user = crud.get_user_by_email(email)
            if user:
                flash("An account with this email already exists.")

            else:
                user = crud.create_user(fname, lname, email, password, fave_anime, profile_url, security1, security2, security3)
                db.session.add(user)
                db.session.commit()
                flash("Account created successfully. Please log in.")


        else:
            flash("One or more fields are invalid! Please try again.")
    
    else:
        flash("One or more fields are invalid! Please try again.")

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
        session["user_id"]=match.user_id
        session.modified = True
        flash("Logged in!")
    
    return redirect("/")

@app.route('/profile')
def show_user_details():
    """Shows users profile if logged-in"""
    signed_in_email=session.get("user_email")

    if signed_in_email is None:
        flash("You must be signed in!")
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
        flash("You must be signed in!")
        return redirect("/")

    
    new_fname = request.form.get('fname')
    new_lname = request.form.get('lname')
    new_fave_anime = request.form.get('fave_anime')


    if new_fname:
        user.fname = new_fname
        db.session.commit()
        flash("First name was updated.")


    if new_lname:
        user.lname = new_lname
        db.session.commit()
        flash("Last name was updated.")


    if new_fave_anime:
        user.fave_anime = new_fave_anime
        db.session.commit()
        flash("Favorite anime was updated.")
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
        flash("You must be signed in!")
        return redirect("/")

    if updated_new_password != updated_confirm_password:
        flash("The passwords do not match. Please try again.")

    if updated_new_password == updated_confirm_password:
        user.password = updated_new_password
        db.session.commit()
        flash("The password was updated.")

    return redirect("/profile")



@app.route("/map/fireballs")
def view_fireball_map():
    """Show map of fireballs."""

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
        for locator in Locator.query.limit(1000)
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
        flash("You must be signed in!")
        return redirect("/")

    # locator_id= request.form.get('fireballs_id')
    # user = User.query.filter(User.email==session["user_email"]).first()
    user= User.query.get(session["user_id"])
 
    map_save=Saved.query.filter(Saved.user_id == user.user_id, Saved.locator_id == locator_id).first()
    # list_of_saves = Saved.query.filter(Saved.user_id == user.user_id).all()

    if map_save:
        flash("You saved this fireball already.")

    else:
        # user = crud.get_user_by_email(signed_in_email)
        locator = crud.get_location_by_coordinates(locator_id)

        save = crud.create_saved_location(user, locator)
        db.session.add(save)
        db.session.commit()
        flash("You saved the coordinates for this fireball.")

    return redirect(f'/fireballs/{locator_id}')

@app.route("/my_saved_fireballs")
def my_fireball_saves():
    """Display fireball saved"""
    
    signed_in_email=session.get("user_email")

    if signed_in_email is None:
        flash("You must be signed in!")
        return redirect("/")

    else:
        user = User.query.filter(User.email==session["user_email"]).first()

        my_saves=Saved.query.filter(Saved.user_id == user.user_id).all()

    return render_template("my_saved_fireballs.html", my_saves=my_saves, user=user)

@app.route('/delete_saved_fireball', methods=["POST"])
def delete_fireball():
    """Delete a saved fireball"""

    signed_in_email=session.get("user_email")

    if signed_in_email is None:
        flash("You must be signed in!")
        return redirect("/")

    else: 
        user= User.query.filter(User.email==session["user_email"]).first()
        locator_id = request.form.get('fireball_id')

        remove = crud.remove_saved_location(user, locator_id)
        db.session.delete(remove)
        db.session.commit()
        flash("You deleted this fireball from your saves.")


        return redirect("/my_saved_fireballs")

@app.route('/save_fireball', methods=["POST"])
def save_fireball_from_map():
    """Save fireball from map"""

    signed_in_email=session.get("user_email")
 
    if signed_in_email is None:
        flash("You must be signed in!")
        return redirect("/")

    locator_id= request.form.get('fireballs_id')
    # user = User.query.filter(User.email==session["user_email"]).first()
    user= User.query.get(session["user_id"])
    map_save=Saved.query.filter(Saved.user_id == user.user_id, Saved.locator_id== locator_id).first()
    # list_of_saves = Saved.query.filter(Saved.user_id == user.user_id).all()

    # for save in list_of_saves:
    if map_save:
        flash("You saved this fireball already.")

    else:

        # user = User.query.filter(User.email==session["user_email"]).first()
        # locator_id = Saved.query.filter(Saved.user_id == user.user_id).all()
        save_fire = crud.create_location_by_map(user, locator_id)
        print(save_fire)
        db.session.add(save_fire)
        db.session.commit()
        flash("You added this fireball to you saves")


    return redirect("/my_saved_fireballs")


@app.route("/logout", methods=["GET"])
def logout():
    """ log out current user"""
    # print("this is the session before we do session pop")
    # print(session)
    session.pop("user_email", None)
    # print("this is the session after we do session pop")
    # print(session)

    flash("You are now logged out")

    return redirect("/")




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
