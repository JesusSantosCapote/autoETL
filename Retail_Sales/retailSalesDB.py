import sqlalchemy
from sqlalchemy import create_engine, Table, text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from config import CONNECTION_INFO
import psycopg2


dialect = CONNECTION_INFO['dialect']
driver = CONNECTION_INFO['driver']
user = CONNECTION_INFO['username']
password = CONNECTION_INFO['password']
host = CONNECTION_INFO['host']
port = CONNECTION_INFO['port']
database = CONNECTION_INFO['database']

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
    __tablename__ = 'Provincia'
    id_Prov = Column(Integer, primary_key=True, name='IdProvincia')
    name = Column(String, name='Nombre')

    municipalitys = relationship('Municipality', back_populates='province')


class Municipality(Base):
    __tablename__ = 'Municipio'
    id_Mun = Column(Integer, primary_key=True, name='IdMunicipio')
    name = Column(String, name='Nombre')

    id_prov = Column(Integer, ForeignKey('Provincia.IdProvincia'), name='IdProvincia')
    province = relationship('Province', back_populates='municipalitys')

    neighborhoods = relationship('Neighborhood', back_populates='municipality')


class Neighborhood(Base):
    __tablename__ = 'Reparto'
    id_Neighb = Column(Integer, primary_key=True, name='IdReparto')
    name = Column(String, name='Nombre')

    id_mun = Column(Integer, ForeignKey('Municipio.IdMunicipio'), name='IdMunicipio')
    municipality = relationship('Municipality', back_populates='neighborhoods')

    stores = relationship('Store', back_populates='neighborhood')


class Store_Department(Base):
    __tablename__ = 'Tienda_Departamento'
    id_store = Column(Integer, ForeignKey('Tienda.IdTienda'), primary_key=True, name='IdTienda')
    id_depart = Column(Integer, ForeignKey('Departamento.IdDepartamento'), primary_key=True, name='IdDepartamento')

    store = relationship('Store', back_populates='departments')
    department = relationship('Department', back_populates='stores')


class Store(Base):
    __tablename__ = 'Tienda'
    id_Store = Column(Integer, primary_key=True, name='IdTienda')
    name = Column(String, name='Nombre')

    id_neighb = Column(Integer, ForeignKey('Reparto.IdReparto'), name='IdReparto')
    neighborhood = relationship('Neighborhood', back_populates='stores')

    departments = relationship('Store_Department', back_populates='store')
    sales = relationship('Sale')


class Department(Base):
    __tablename__ = 'Departamento'
    id_depart = Column(Integer, primary_key=True, name='IdDepartamento')
    name = Column(String, name='Nombre')
    description = Column(String, name='Descripción')

    stores = relationship('Store_Department', back_populates='department')

    products = relationship('Product', back_populates='department')

    
class Brand(Base):
    __tablename__ = 'Marca'
    id_brand = Column(Integer, primary_key=True, name='IdMarca')
    name = Column(String, name='Nombre')

    products = relationship('Product', back_populates='brand')


class Category(Base):
    __tablename__ = 'Categoría'
    id_cat = Column(Integer, primary_key=True, name='IdCategoría')
    name = Column(String, name='Nombre')

    products = relationship('Product', back_populates='category')


class Package(Base):
    __tablename__ = 'TipoPaquete'
    id_pack = Column(Integer, primary_key=True, name='IdTipoPaquete')
    name = Column(String, name='Nombre')

    products = relationship('Product', back_populates='package')


class Product(Base):
    __tablename__ = 'Producto'
    id_Prod = Column(Integer, primary_key=True, name='IdProducto')
    name = Column(String, name='Nombre')
    price = Column(Integer, name='Precio')
    cost = Column(Integer, name='Costo')

    id_brand = Column(Integer, ForeignKey('Marca.IdMarca'), name='IdMarca')
    brand = relationship('Brand', back_populates='products')

    id_cat = Column(Integer, ForeignKey('Categoría.IdCategoría'), name='IdCategoría')
    category = relationship('Category', back_populates='products')

    id_pack = Column(Integer, ForeignKey('TipoPaquete.IdTipoPaquete'), name='IdTipoPaquete')
    package = relationship('Package', back_populates='products')

    id_depart = Column(Integer, ForeignKey('Departamento.IdDepartamento'), name='IdDepartamento')
    department = relationship('Department', back_populates='products')

    sales = relationship('Sale')


class Sale(Base):
    __tablename__ = 'Venta'
    id_sale = Column(Integer, primary_key=True, name='IdVenta')
    date = Column(Date, name='Fecha')

    id_prod = Column(Integer, ForeignKey('Producto.IdProducto'), name='IdProducto')
    id_store = Column(Integer, ForeignKey('Tienda.IdTienda'), name='IdTienda')

    quantity_sold = Column(Integer, name='Cantidad_Vendida')
    payment = Column(Integer, name='Pago')


if __name__ == "__main__":
    Base.metadata.create_all(engine)