import sqlalchemy
from sqlalchemy import create_engine, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from config import connection_info

dialect = connection_info['dialect']
driver = connection_info['driver']
user = connection_info['username']
password = connection_info['password']
host = connection_info['host']
port = connection_info['port']
database = connection_info['database']

engine = create_engine(f'{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}', echo=True, future=True)
Base = declarative_base()


# Check if the database exists
database_name = 'retailSales'
existing_databases = engine.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = '{}'".format(database_name)).fetchall()

if existing_databases:
    print("Database '{}' already exists.".format(database_name))
else:
    # Create the database
    engine.execute("CREATE DATABASE {}".format(database_name))
    print("Database '{}' created successfully.".format(database_name))



class Province(Base):
    __tablename__ = 'Provincia'
    id_Prov = Column(Integer, primary_key=True, name='IdProvincia')
    name = Column(String, name='Nombre')

    municipalitys = relationship('Municipality', back_populates='province')


class Municipality(Base):
    __tablename__ = 'Municipio'
    id_Mun = Column(Integer, primary_key=True, name='IdMunicipio')
    name = Column(String, name='Nombre')

    id_prov = Column(Integer, ForeignKey('Provincia.id_Prov'), name='IdProvincia')
    province = relationship('Province', back_populates='municipalitys')

    neighborhoods = relationship('Neighborhood', back_populates='municipality')


class Neighborhood(Base):
    __tablename__ = 'Reparto'
    id_Neighb = Column(Integer, primary_key=True, name='IdReparto')
    name = Column(String, name='Nombre')

    id_mun = Column(Integer, ForeignKey('Municipality.id_Mun'), name='IdMunicipio')
    municipality = relationship('Municipality', back_populates='neighborhoods')

    stores = relationship('Store', back_populates='neighborhood')


store_depart_association_table = Table(
    'Tienda Departamento',
    Base.metadata,
    Column(Integer, ForeignKey('Store.id_Store'), primary_key=True, name='IdTienda'),
    Column(Integer, ForeignKey('Department.id_depart'), primary_key=True, name='IdDepartamento'), 
)


class Store(Base):
    __tablename__ = 'Tienda'
    id_Store = Column(Integer, primary_key=True, name='IdTienda')
    name = Column(String, name='Nombre')

    id_neighb = Column(Integer, ForeignKey('Neighborhood.id_Neighb'), name='IdReparto')
    neighborhood = relationship('Neighborhood', back_populates='stores')

    departments = relationship('Department', secondary=store_depart_association_table, back_populates='stores')
    sales = relationship('Sale')


class Department(Base):
    __tablename__ = 'Departamento'
    id_depart = Column(Integer, primary_key=True, name='IdDepartamento')
    name = Column(String, name='Nombre')
    description = Column(String, name='Descripción')

    stores = relationship('Store', secondary=store_depart_association_table, back_populates='departments')

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

    id_brand = Column(Integer, ForeignKey('Brand.id_brand'), name='IdMarca')
    brand = relationship('Brand', back_populates='products')

    id_cat = Column(Integer, ForeignKey('Category.id_cat'), name='IdCategoría')
    category = relationship('Category', back_populates='products')

    id_pack = Column(Integer, ForeignKey('Package.id_pack'), name='IdTipoPaquete')
    package = relationship('Package', back_populates='products')

    id_depart = Column(Integer, ForeignKey('Department.id_depart'), name='IdDepartamento')
    department = relationship('Department', back_populates='products')

    sales = relationship('Sale')


class Sale(Base):
    __tablename__ = 'Venta'
    id_sale = Column(Integer, primary_key=True, name='IdVenta')
    date = Column(Date, name='Fecha')

    id_prod = Column(Integer, ForeignKey('Product.id_Prod'), name='IdProducto')
    id_store = Column(Integer, ForeignKey('Store.id_Store'), name='IdTienda')

    quantity_sold = Column(Integer, name='Cantidad Vendida')
    payment = Column(Integer, name='Pago')


Base.metadata.create_all(engine)