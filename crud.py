"""CRUD operations."""
from model import db, User, Locator, connect_to_db


def create_user(email, password):
    """Create & return a new user."""

    user = User(email=email, password=password)

    return user  

def get_location_by_coordinates(locator_id):
    """Get location by zipcode"""
    return Locator.query.get(locator_id)



def get_user_by_email(email):
    return User.query.filter(User.email == email).first()


def check_email_and_pass(email, password):
    return User.query.filter(User.password == password).first() and User.query.filter(User.email == email).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)