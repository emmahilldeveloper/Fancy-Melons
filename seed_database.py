"""Sample data for Fancy Melons application."""

import os
import json
from datetime import datetime

import crud
import model
import server

os.system("dropdb fancy_melons")
os.system("createdb fancy_melons")
model.connect_to_db(server.app)
model.db.create_all()

####### Creating melons in database. #######
melons_in_db = []

with open('Data/melons.json') as f:
    melons_data = json.loads(f.read())

for melon in melons_data:
    melon_name = melon["melon_name"]
    melon_price = melon["melon_price"]
    melon_photo = melon["melon_photo"]

    db_melon = crud.create_melon(melon_name, melon_price, melon_photo)
    melons_in_db.append(db_melon)

model.db.session.add_all(melons_in_db)

####### Creating tastings in database. #######
tastings_in_db = []

with open('Data/tastings.json') as f:
    tastings_data = json.loads(f.read())

for tasting in tastings_data:
    tasting_name = tasting["tasting_name"]
    tasting_photo = tasting["tasting_photo"]

    db_tasting = crud.create_tasting(tasting_name, tasting_photo)
    tastings_in_db.append(db_tasting)

model.db.session.add_all(tastings_in_db)

####### Save everything. #######
model.db.session.commit()