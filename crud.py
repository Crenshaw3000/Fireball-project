"""CRUD operations."""

from model import db, User, Locator, Saved, connect_to_db


def create_user(fname, lname, email, password):
    """Create & return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

    return user

def create_location(date, latitude, longitude):
    """Create and return new locator"""
    locator = Locator(date=date, latitude=latitude, longitude=longitude)

    return locator

# def get_location_by_coordinates(locator_id):
    # return Locator.query.get(locator_id)

def get_saved_location(user, locator):
    """Create and return new saved location for user"""
    save = Saved(user=user, locator=locator)

    return save

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def check_email_and_pass(email, password):
    return User.query.filter(User.password == password).first() and User.query.filter(User.email == email).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)