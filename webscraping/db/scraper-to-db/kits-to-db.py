import json
from dotenv import load_dotenv
from webscraping.db.models.builder import Kits
from webscraping.db.database import SessionLocal
from sqlalchemy.exc import IntegrityError

load_dotenv()

session = SessionLocal()

with open('webscraping/data/kits.json', 'r') as file:
    kits_data = json.load(file)

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

session.commit()
session.close()