import faker
import sqlalchemy
from faker import Faker
from faker.providers import address
from config import SEED, CONNECTION_INFO
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, exists
from retailSalesDB import *
import random
import json
import os
from datetime import date

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
    for i in range(30):
        results.append(fake.unique.city())

    return results


def locations_tables_populate():
    locations = generate_locations()
    provinces = [Province(name=locations[i]) for i in range(5)]

    session.add_all(provinces)
    session.flush()

    #Returns a tuple in the form (pk,)
    prov_pk = session.execute(select(Province.id_Prov)).fetchall()

    municipalistys = []

    #Ensures that all the provinces have at least one municipality
    for i,j in zip(prov_pk, [locations[k] for k in range(5,10)]):
        municipalistys.append(Municipality(name=j, id_prov=i[0]))

    for i in range(10, 15):
        prov = rand.choice(prov_pk)[0]
        municipalistys.append(Municipality(name=locations[i], id_prov=prov))

    session.add_all(municipalistys)
    session.flush()

    mun_pk = session.execute(select(Municipality.id_Mun)).fetchall()

    neighborhoods = []

    #Ensures that all the municipalitys have at least one neighborhood
    for i,j in zip(mun_pk, [locations[k] for k in range(15, 25)]):
        neighborhoods.append(Neighborhood(name=j, id_mun=i[0]))

    for i in range(25, 30):
        mun = rand.choice(mun_pk)[0]
        neighborhoods.append(Neighborhood(name=locations[i], id_mun=mun))

    session.add_all(neighborhoods)
    session.flush()


def department_stores_populate():
    departments_names = ["Electrónica", "Ropa", "Calzado", 
                        "Hogar", "Belleza", "Juguetes", "Deportes", 
                        "Alimentos", "Muebles", "Libros"]
    
    departments_des = [
        "Productos electrónicos como teléfonos, computadoras y accesorios.",
        "Prendas de vestir para hombres, mujeres y niños de distintos estilos y tallas.",
        "Zapatos y zapatillas para todas las edades y ocasiones.",
        "Artículos para el hogar, decoración y muebles.",
        "Productos de cuidado personal, maquillaje y perfumería.",
        "Juguetes y juegos para niños de todas las edades.",
        "Equipos, ropa y accesorios para practicar deportes.",
        "Productos comestibles, desde alimentos frescos hasta enlatados.",
        "Muebles para todas las habitaciones del hogar, desde sala hasta cocina.",
        "Libros de diferentes géneros y temáticas para leer y disfrutar."]
    
    departments = []

    for dep, desc in zip(departments_names, departments_des):
        departments.append(Department(name=dep, description=desc))

    session.add_all(departments)
    session.flush()

    stores = []
    neighborhoods_pk = session.execute(select(Neighborhood.id_Neighb)).fetchall()

    for i in range(len(neighborhoods_pk)):
        stores.append(Store(name=f"Tienda{i+1}", id_neighb=neighborhoods_pk[i][0]))

    session.add_all(stores)
    session.flush()

    stores_pk = session.execute(select(Store.id_Store)).fetchall()
    department_pk = session.execute(select(Department.id_depart)).fetchall()

    stores_departments = []

    for i in stores_pk:
        depart_number = rand.randint(1, len(department_pk))
        rand.shuffle(department_pk)
        for j in range(depart_number):
            stores_departments.append(Store_Department(id_store=i[0], id_depart=department_pk[j][0]))

    session.add_all(stores_departments)
    session.flush()


def product_tables_populate():
    pwd = os.getcwd()
    data_path = os.path.join(pwd, 'products.json')

    with open(data_path) as file:
        data = json.load(file)

    for dep in data.keys():
        for prod in data[dep]:
            dep_pk = session.execute(select(Department.id_depart).where(Department.name == dep)).scalar()

            if not session.query(exists().where(Brand.name == prod['marca'])).scalar():
                session.add(Brand(name=prod['marca']))
                session.flush()

            brand_pk = session.execute(select(Brand.id_brand).where(Brand.name == prod['marca'])).scalar()

            if not session.query(exists().where(Category.name == prod['categoria'])).scalar():
                session.add(Category(name=prod['categoria']))
                session.flush()

            category_pk = session.execute(select(Category.id_cat).where(Category.name == prod['categoria'])).scalar()

            if not session.query(exists().where(Package.name == prod['empaquetado'])).scalar():
                session.add(Package(name=prod['empaquetado']))
                session.flush()

            package_pk = session.execute(select(Package.id_pack).where(Package.name == prod['empaquetado'])).scalar()

            price = rand.randint(20, 100)
            cost = price - rand.randint(5, price)
            session.add(Product(name=prod['producto'], price=price, 
                                cost=cost, id_brand=brand_pk, id_cat=category_pk, id_pack=package_pk, id_depart=dep_pk))
            session.flush()
                
    
def sale_table_populate():
    stores_pk = session.execute(select(Store.id_Store)).fetchall()
    products_pk = session.execute(select(Product.id_Prod, Product.price)).fetchall()

    for year in [2022, 2023]:
        for month in range(1, 13):
            month_sales = rand.randint(10, 20)
            for i in range(month_sales):
                day = rand.randint(1, 28)
                product, price = rand.choice(products_pk)
                store = rand.choice(stores_pk)[0]
                quantity_sold = rand.randint(1, 5)
                session.add(Sale(date=date(year,month,day), id_prod=product, id_store=store, 
                                 quantity_sold=quantity_sold, payment=price*quantity_sold))
                session.flush()


if __name__ == "__main__":
    locations_tables_populate()
    department_stores_populate()
    product_tables_populate()
    sale_table_populate()
    session.commit()
    session.close()