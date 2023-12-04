import sqlalchemy
from sqlalchemy import create_engine, Table, text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from config import CONNECTION_INFO
import psycopg2


dialect = CONNECTION_INFO['dialect']
driver = CONNECTION_INFO['driver']
user = CONNECTION_INFO['user']
password = CONNECTION_INFO['password']
host = CONNECTION_INFO['host']
port = CONNECTION_INFO['port']
database = CONNECTION_INFO['dbname']

connection = psycopg2.connect(user=user, password=password, host=host, port=port)
cursor = connection.cursor()
connection.autocommit = True

# Database table list
cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = '{}'".format(database))
existing_databases = cursor.fetchall()

# Check if the database exists
if existing_databases:
    print("Database '{}' already exists.".format(database))
else:
    # Create the database
    cursor.execute("CREATE DATABASE {}".format(database))
    print("Database '{}' created successfully.".format(database))


engine = create_engine(f'{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}', echo=True, future=True)
Base = declarative_base()

class Province(Base):
    __tablename__ = 'provincia'
    id_Prov = Column(Integer, primary_key=True, name='idprovincia')
    name = Column(String, name='nombre', unique=True)

    municipalitys = relationship('Municipality', back_populates='province')


class Municipality(Base):
    __tablename__ = 'municipio'
    id_Mun = Column(Integer, primary_key=True, name='idmunicipio')
    name = Column(String, name='nombre', unique=True)

    id_prov = Column(Integer, ForeignKey('provincia.idprovincia'), name='idprovincia')
    province = relationship('Province', back_populates='municipalitys')

    neighborhoods = relationship('Neighborhood', back_populates='municipality')


class Neighborhood(Base):
    __tablename__ = 'reparto'
    id_Neighb = Column(Integer, primary_key=True, name='idreparto')
    name = Column(String, name='nombre', unique=True)

    id_mun = Column(Integer, ForeignKey('municipio.idmunicipio'), name='idmunicipio')
    municipality = relationship('Municipality', back_populates='neighborhoods')

    stores = relationship('Store', back_populates='neighborhood')


class Store(Base):
    __tablename__ = 'tienda'
    id_Store = Column(Integer, primary_key=True, name='idtienda')
    name = Column(String, name='nombre', unique=True)

    id_neighb = Column(Integer, ForeignKey('reparto.idreparto'), name='idreparto')
    neighborhood = relationship('Neighborhood', back_populates='stores')

    sales = relationship('Sale')


class Department(Base):
    __tablename__ = 'departamento'
    id_depart = Column(Integer, primary_key=True, name='iddepartamento')
    name = Column(String, name='nombre', unique=True)
    description = Column(String, name='descripcion')

    products = relationship('Product', back_populates='department')

    
class Brand(Base):
    __tablename__ = 'marca'
    id_brand = Column(Integer, primary_key=True, name='idmarca')
    name = Column(String, name='nombre', unique=True)

    products = relationship('Product', back_populates='brand')


class Category(Base):
    __tablename__ = 'categoria'
    id_cat = Column(Integer, primary_key=True, name='idcategoria')
    name = Column(String, name='nombre', unique=True)

    products = relationship('Product', back_populates='category')


class Package(Base):
    __tablename__ = 'tipopaquete'
    id_pack = Column(Integer, primary_key=True, name='idtipopaquete')
    name = Column(String, name='nombre', unique=True)

    products = relationship('Product', back_populates='package')


class Product(Base):
    __tablename__ = 'producto'
    id_Prod = Column(Integer, primary_key=True, name='idproducto')
    name = Column(String, name='nombre', unique=True)
    price = Column(Integer, name='precio')
    cost = Column(Integer, name='costo')

    id_brand = Column(Integer, ForeignKey('marca.idmarca'), name='idmarca')
    brand = relationship('Brand', back_populates='products')

    id_cat = Column(Integer, ForeignKey('categoria.idcategoria'), name='idcategoria')
    category = relationship('Category', back_populates='products')

    id_pack = Column(Integer, ForeignKey('tipopaquete.idtipopaquete'), name='idtipopaquete')
    package = relationship('Package', back_populates='products')

    id_depart = Column(Integer, ForeignKey('departamento.iddepartamento'), name='iddepartamento')
    department = relationship('Department', back_populates='products')

    sales = relationship('Sale')


class Sale(Base):
    __tablename__ = 'venta'
    id_sale = Column(Integer, primary_key=True, name='idventa')
    date = Column(Date, name='fecha')

    id_prod = Column(Integer, ForeignKey('producto.idproducto'), name='idproducto')
    id_store = Column(Integer, ForeignKey('tienda.idtienda'), name='idtienda')

    quantity_sold = Column(Integer, name='cantidad_vendida')
    payment = Column(Integer, name='pago')


if __name__ == "__main__":
    Base.metadata.create_all(engine)