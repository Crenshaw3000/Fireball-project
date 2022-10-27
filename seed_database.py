"""Script to seed database."""

import os
import json
from datetime import datetime

import crud
import model
import server

os.system("dropdb saved")
os.system("createdb saved")

model.connect_to_db(server.app)
model.db.create_all() 



with open('data/fireball2.json') as f:
    locator_data = json.dumps(f.read())
    print(locator_data)
    # result = [item.replace("'", '"') for item in locator_data]
    # print(result)
    result = json.loads(locator_data)
    print(result)
    print(type(result))
    # for i in result:
    #     if isinstance(i, dict):
    #         for key, value in i.items():
    #             print(key, value)
    #     else:
    #         print(i)


# Create locations, store them in list so we can use them
# to save locations later
# locations_in_db = []
# for loc in result:
#     print(loc)
#     # print(type(loc))
#     latitude, longitude, energy = (
#         loc['latitude'],
#         loc['longitude'],
#         loc['energy'],

#     )

#     date = datetime.strptime(loc['date'], "%Y-%m-%d %H:%M:%S")

#     db_location = crud.create_location(date, latitude, longitude, energy)
#     locations_in_db.append(db_location)

# model.db.session.add_all(locations_in_db)
# model.db.session.commit()
