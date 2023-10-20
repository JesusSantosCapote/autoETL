import faker
import sqlalchemy
from faker import Faker
from faker.providers import address
from config import SEED, CONNECTION_INFO
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from retailSalesDB import Province, Municipality
import random

fake = Faker()
fake.add_provider(address)
Faker.seed(SEED)

rand = random.Random()
rand.seed(SEED)

dialect = CONNECTION_INFO['dialect']
driver = CONNECTION_INFO['driver']
user = CONNECTION_INFO['username']
password = CONNECTION_INFO['password']
host = CONNECTION_INFO['host']
port = CONNECTION_INFO['port']
database = CONNECTION_INFO['database']

engine = create_engine(f'{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}', echo=True, future=True)
conn = engine.connect()
session = Session(engine)

def generate_locations():
    results = []
    for i in range(100):
        results.append(fake.unique.city())

    return results


def populate_locations_tables():
    locations = generate_locations()
    provinces = [Province(name=locations[i]) for i in range(5)]

    session.add_all(provinces)
    session.commit()

    prov_pk = select(Province.id_Prov)

    



populate_locations_tables()


