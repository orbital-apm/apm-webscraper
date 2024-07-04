import json
from dotenv import load_dotenv
from webscraping.db.models.builder import Switch
from webscraping.db.database import SessionLocal
from sqlalchemy.exc import IntegrityError

load_dotenv()

session = SessionLocal()

with open('webscraping/data/switches.json', 'r') as file:
    switches_data = json.load(file)

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

session.commit()
session.close()