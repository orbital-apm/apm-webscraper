import json
from dotenv import load_dotenv
from webscraping.db.models.builder import Switch, Keycap, Kits, Lubricant
from webscraping.db.database import SessionLocal
from sqlalchemy.exc import IntegrityError

load_dotenv()

session = SessionLocal()

# Read JSON file
with open('webscraping/data/kits.json', 'r') as file:
    kits_data = json.load(file)

with open('webscraping/data/keycaps.json', 'r') as file:
    keycaps_data = json.load(file)

with open('webscraping/data/switches.json', 'r') as file:
    switches_data = json.load(file)

with open('webscraping/data/lubricants.json', 'r') as file:
    lubricants_data = json.load(file)

# Iterate through JSON data and create Kits objects
for kit in kits_data:
    KIT = Kits(
        name=kit.get('name'),
        price=kit.get('price'),
        manufacturer=kit.get('manufacturer'),
        vendor=kit.get('vendor'),
        layout_size=kit.get('layout_size'),
        layout_standard=kit.get('layout_standard'),
        layout_ergonomic=kit.get('layout_ergonomic'),
        hotswappable=kit.get('hotswappable'),
        knob_support=kit.get('knob_support'),
        rgb_support=kit.get('rgb_support'),
        display_support=kit.get('display_support'),
        connection=kit.get('connection'),
        mount_style=kit.get('mount_style'),
        material=kit.get('material'),
        img_url=kit.get('img_url'),
        availability=kit.get('availability')
    )

    existing_kit = session.query(Kits).filter_by(name=KIT.name).first()

    if existing_kit is None:
        try:
            session.add(KIT)
            session.commit()

        except IntegrityError:
            session.rollback()

for switch in switches_data:
    SWITCH = Switch(
        name=switch.get('name'),
        price=switch.get('price'),
        manufacturer=switch.get('manufacturer'),
        vendor=switch.get('vendor'),
        switch_type=switch.get('switch_type'),
        actuation_force=switch.get('actuation_force'),
        travel_distance=switch.get('travel_distance'),
        img_url=switch.get('img_url'),
        availability=switch.get('availability')
    )

    existing_switch = session.query(Switch).filter_by(name=SWITCH.name).first()

    if existing_switch is None:
        try:
            session.add(SWITCH)
            session.commit()

        except IntegrityError:
            session.rollback()

for keycap in keycaps_data:
    KEYCAP = Keycap(
        name=keycap.get('name'),
        price=keycap.get('price'),
        manufacturer=keycap.get('manufacturer'),
        vendor=keycap.get('vendor'),
        colors=keycap.get('colors'),
        layout=keycap.get('layout'),
        material=keycap.get('material'),
        profile=keycap.get('profile'),
        img_url=switch.get('img_url'),
        availability=switch.get('availability')
    )

    existing_keycap = session.query(Keycap).filter_by(name=KEYCAP.name).first()

    if existing_keycap is None:
        try:
            session.add(KEYCAP)
            session.commit()

        except IntegrityError:
            session.rollback()

for lubricant in lubricants_data:
    LUBRICANT = Lubricant(
        name=lubricant.get('name'),
        price=lubricant.get('price'),
        img_url=lubricant.get('img_url'),
        availability=lubricant.get('availability')
    )

    existing_lubricant = session.query(Lubricant).filter_by(name=LUBRICANT.name).first()

    if existing_lubricant is None:
        try:
            session.add(LUBRICANT)
            session.commit()

        except IntegrityError:
            session.rollback()

session.commit()
session.close()
