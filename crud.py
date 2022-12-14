"""CRUD operations."""

from model import db, User, Locator, Saved, connect_to_db


def create_user(fname, lname, email, password, fave_anime, profile_url, security1, security2, security3):
    """Create & return a new user."""
    user = User(fname=fname, lname=lname, email=email, password=password, fave_anime=fave_anime, profile_url=profile_url, security1=security1, security2=security2, security3=security3)

    return user

def create_location(date, latitude, longitude, energy):
    """Create and return new  locator"""
    locator = Locator(date=date, latitude=latitude, longitude=longitude, energy=energy)

    return locator

def get_fireballs():
    """Return all fireballs"""
    return Locator.query.all()

def get_location_by_coordinates(locator_id):
    """Get location by locator_id"""
    return Locator.query.get(locator_id)

def create_saved_location(user, locator):
    """Create and return new saved location for user"""
    save = Saved(user=user, locator=locator)

    return save

def get_saves_by_user(user_id):
    """Returns all saves by user user_id"""
    return Saved.query.filter(Saved.user_id == user_id).all()

def remove_saved_location(user, locator_id):
    """" Removed saved fireball"""
    return Saved.query.filter_by(user=user, locator_id=locator_id).first()

def create_location_by_map(user, locator_id):
    """Creates location by user for maps"""
    get_location= Saved(user=user, locator_id=locator_id)

    return get_location

def get_profile(user):
    "gets user info"
    return User.query.filter_by(user=user).first()

def remove_profile_photo(user_id, profile_url):
    return User.query.filter_by(user_id=user_id, profile_url=profile_url).first()


def get_user_individual(email):
    """Get user by email"""
    return User.query.get(email)

def get_user_by_email(email):
    """ Get user information by email"""
    return User.query.filter(User.email == email).first()


def check_email_and_pass(email, password):
    """ Get email and password by user if email and password match from form"""
    return User.query.filter(User.password == password, User.email == email).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)