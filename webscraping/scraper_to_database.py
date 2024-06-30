import json
from dotenv import load_dotenv
from webscraping.db.builder import Switch, Keycap, Kits, Lubricant
from webscraping.db.database import SessionLocal

load_dotenv()

session = SessionLocal()

# Read JSON file
with open('kits.json', 'r') as file:
    data = json.load(file)

# Iterate through JSON data and create Kits objects
for item in data:
    kit = Kits(
        name=item.get('name'),
        price=item.get('price'),
        manufacturer=item.get('manufacturer'),
        layout_size=item.get('layout_size'),
        layout_standard=item.get('layout_standard'),
        layout_ergonomic=item.get('layout_ergonomic'),
        hotswappable=item.get('hotswappable'),
        knob_support=item.get('knob_support'),
        rgb_support=item.get('rgb_support'),
        display_support=item.get('display_support'),
        connection=item.get('connection'),
        mount_style=item.get('mount_style'),
        material=item.get('material')
    )
    session.add(kit)

# Commit the changes to the database
session.commit()

# Close the session
session.close()