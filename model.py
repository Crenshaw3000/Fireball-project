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
    password = db.Column(db.String, nullable=False)
    fave_anime=db.Column(db.String, nullable=True)
    profile_url = db.Column(db.String, nullable=True)
    security1 = db.Column(db.String, nullable= False)
    security2 = db.Column(db.String, nullable=False)
    security3 =db.Column(db.String, nullable=False)


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
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    energy = db.Column(db.Float)

    saved = db.relationship("Saved", back_populates="locator")

    # def __init__(self,
    #                 locator_id,
    #                 date,
    #                 latitude,
    #                 longitude,
    #                 energy):

    #         """Create a fireball."""

    #         self.locator_id = locator_id
    #         self.date = date
    #         self.latitude = latitude
    #         self.longitude = longitude
    #         self.energy = energy


    def __repr__(self):
        # repr_str = "<Locator locator_id={locator_id}>"

        return f'</Locator locator_id={self.locator_id} latitude={self.latitude}> longitude={self.longitude}>'

class Saved(db.Model):
    """Saved location."""

    __tablename__ = "saved"

    saved_location = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    locator_id = db.Column(db.Integer, db.ForeignKey("locators.locator_id"), nullable=False)               

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
