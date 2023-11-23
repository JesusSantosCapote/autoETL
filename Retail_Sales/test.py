import sqlalchemy
from sqlalchemy import create_engine, Table, text, ForeignKeyConstraint
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

class Region(Base):
    __tablename__ = 'region'

    region_key = Column(Integer, primary_key=True, name='regionkey')


class Nation(Base):
    __tablename__ = 'nation'

    nation_key = Column(Integer, primary_key=True, name='nationkey')
    region_key = Column(Integer, ForeignKey('region.regionkey'), name='regionkey')


class Customer(Base):
    __tablename__ = 'customer'

    cust_key = Column(Integer, primary_key=True, name='custkey')
    nation_key = Column(Integer, ForeignKey('nation.nationkey'), name='nationkey')


class Order(Base):
    __tablename__ = 'buy_order'

    order_key = Column(Integer, primary_key=True, name='orderkey')
    cust_key = Column(Integer, ForeignKey('customer.custkey'), name='custkey')

class Part(Base):
    __tablename__ = 'part'

    part_key = Column(Integer, primary_key=True, name='partkey')


class Supplier(Base):
    __tablename__ = 'supplier'

    sup_key = Column(Integer, primary_key=True, name='supkey')
    nation_key = Column(Integer, ForeignKey('nation.nationkey'), name='nationkey')


class PartSup(Base):
    __tablename__ = 'partsup'

    part_key = Column(Integer, ForeignKey('part.partkey'), primary_key=True, name='partkey')
    sup_key = Column(Integer, ForeignKey('supplier.supkey'), primary_key=True, name='supkey')


class Line(Base):
    __tablename__ = 'line'

    line_num = Column(Integer, primary_key=True, name='linenumber')
    part_key = Column(Integer, ForeignKey('part.partkey'), name='partkey')
    sup_key = Column(Integer, ForeignKey('supplier.supkey'), name='supkey')
    order_key = Column(Integer, ForeignKey('buy_order.orderkey'), name='orderkey')


if __name__ == "__main__":
    Base.metadata.create_all(engine)
