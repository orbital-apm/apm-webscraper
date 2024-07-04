import json
from dotenv import load_dotenv
from webscraping.db.models.builder import Lubricant
from webscraping.db.database import SessionLocal
from sqlalchemy.exc import IntegrityError

load_dotenv()

session = SessionLocal()

with open('webscraping/data/lubricants.json', 'r') as file:
    lubricants_data = json.load(file)

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
