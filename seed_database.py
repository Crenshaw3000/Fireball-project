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



with open('data/fireball2.json') as f:
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
        loc['energy'],

    )

    date = datetime.strptime(loc['date'], "%Y-%m-%d %H:%M:%S")

    db_location = crud.create_location(date, latitude, longitude, energy)
    locations_in_db.append(db_location)

model.db.session.add_all(locations_in_db)
model.db.session.commit()

for n in range(10):
    fname =  'fname_test'
    lname = 'lname_test'
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(fname, fname, email, password)
    model.db.session.add(user)

    for _ in range(10):
        random_save = choice(locations_in_db)

        save = crud.get_saved_location(user, random_save)
        model.db.session.add(random_save)
        
model.db.session.commit()