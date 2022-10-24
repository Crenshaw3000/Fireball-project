"""Models for fireball locator."""

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

    saves = db.relationship("Saved", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Locator(db.Model):
    """fireball coordinates"""

    __tablename__ = "fireball coordinates"

    locator_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    coordinates = db.Column(db.Integer)


    saves = db.relationship("Saved", back_populates="locator")

    def __repr__(self):
        return f'</Locator locator_id={self.locator_id} coordinates={self.coordinates}>'

class Saved(db.Model):
    """Saved location."""

    __tablename__ = "saved"

    saved_location = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key= True)
    user_id = db.Column(db.String, db.ForeignKey('Users.user_id')     
    locator_id = db.Column(db.String, db.ForeignKey('Locators.locator_id'))                    

    locator = db.relationship("Locator", back_populates="saved")
    user = db.relationship("User", back_populates="saved")
    
    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'



if __name__ == "__main__":
    from server import app


# Call connect_to_db(app, echo=False) if your program output gets
 # too annoying; this will tell SQLAlchemy not to print out every
 # query it executes.
    connect_to_db(app)
