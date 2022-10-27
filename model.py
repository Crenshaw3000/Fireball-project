"""Models for fireball locator."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique= True)
    password = db.Column(db.String)

    saved = db.relationship("Saved", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Locator(db.Model):
    """fireball coordinates"""

    __tablename__ = "locators"

    locator_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    
    date = db.Column(db.DateTime)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    energy = db.Column(db.Float)

    saved = db.relationship("Saved", back_populates="locator")

    def __repr__(self):
        return f'</Locator locator_id={self.locator_id} latitude={self.latitude}> longitude={self.longitude}>'

class Saved(db.Model):
    """Saved location."""

    __tablename__ = "saved"

    saved_location = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    locator_id = db.Column(db.Integer, db.ForeignKey("locators.locator_id"))               

    locator = db.relationship("Locator", back_populates="saved")
    user = db.relationship("User", back_populates="saved")
    
    def __repr__(self):
        return f'<Saved saved_location={self.saved_location}>'


def connect_to_db(flask_app, db_uri="postgresql:///saved", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app


# Call connect_to_db(app, echo=False) if your program output gets
 # too annoying; this will tell SQLAlchemy not to print out every
 # query it executes.
    connect_to_db(app)
