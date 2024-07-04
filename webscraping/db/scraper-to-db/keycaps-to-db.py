import json
from dotenv import load_dotenv
from webscraping.db.models.builder import Keycap
from webscraping.db.database import SessionLocal
from sqlalchemy.exc import IntegrityError

load_dotenv()

session = SessionLocal()

with open('webscraping/data/keycaps.json', 'r') as file:
    keycaps_data = json.load(file)

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
        img_url=keycap.get('img_url'),
        availability=keycap.get('availability')
    )

    existing_keycap = session.query(Keycap).filter_by(name=KEYCAP.name).first()

    if existing_keycap is None:
        try:
            session.add(KEYCAP)
            session.commit()

        except IntegrityError:
            session.rollback()

session.commit()
session.close()