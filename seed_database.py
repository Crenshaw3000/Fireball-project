"""Script to seed database."""

import os
import json
from random import choice
from datetime import datetime

import crud
import model
import server

os.system("dropdb saved")
os.system("createdb saved")

model.connect_to_db(server.app)
model.db.create_all() 



with open('data/fireball4.json') as f:
    locator_data = json.loads(f.read())
    print(locator_data)



# Create locations, store them in list so we can use them
# to save locations later
locations_in_db = []
for loc in locator_data:
    print(loc)
    # print(type(loc))
    latitude, longitude, energy = (
        loc['latitude'],
        loc['longitude'],
        loc['energy']

    )

    date = datetime.strptime(loc['date'], "%Y-%m-%d %H: %M: %S")

    db_location = crud.create_location(date, latitude, longitude, energy)
    locations_in_db.append(db_location)

model.db.session.add_all(locations_in_db)
model.db.session.commit()

for n in range(10):
    fname =  'fname_test'
    lname = 'lname_test'
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'
    fave_anime = 'test anime'
    profile_url = 'test profile_url'

    user = crud.create_user(fname, fname, email, password, fave_anime, profile_url)
    model.db.session.add(user)

    for _ in range(10):
        random_save = choice(locations_in_db)

        save = crud.create_saved_location(user, random_save)
        model.db.session.add(random_save)
        
model.db.session.commit()


# tests for model.py
# create a user:
# test_user = User(fname='Jane', lname='Doe', email='test@test.test', password='test')
# db.session.add(test_user)
# db.session.commit()

# to see if user was crated with email:
# user = User.query.first()
# user

# create a new fireball location
# from datetime import datetime
# loc = Locator(date=datetime.now(), latitude= 26.3, longitude=165.8, energy=-2.2)
# db.session.add(loc)
# db.session.commit()

# return all locations just created
# location = Locator.query.all()
# location

# Create a Saved (location) by test_user for the first locator in location (the list above)
# Sav = Saved(user=test_user, locator=location[0])
# db.session.add(Sav)
# db.session.commit()

# Test by printing all saves, print users that have saves and locator latitude saved by users
# saves = Saved.query.all()
# print(saves[0].user.email)
# print(saves[0].locator.latitude)

# Extra tests
# Create a user and add it to the database:
# new_user = User(email='admin@website.com', password='admin')
# db.session.add(new_user)
# db.session.commit()

# Create a new locator (fireball location) and add it to the database:
# from datetime import datetime
# new_locator =  Locator(latitude= 33, longitude=98, date=datetime(2022, 3, 15, 20, 55, 7))
# db.session.add(new_locator)
# db.session.commit()

# Create a new Saved (saved location) by user and add to database:
# new_saves=Saved(user=new_user, locator =new_locator)
# db.session.add(new_saves)
# db.session.commit()

# Seed_database tests (run model interactively)
# get first saved location from data base 
# saves = Saved.query.first()

# Access Saved user and locator attributes 
# saves.user 
# saves.locator

# Print all the saves that saved.user has made
# for user_save in saves.user.saved:
#     print(user_save.locator)