import faker
from faker import Faker
from faker.providers import address
import random
import os
from datetime import date
import psycopg2

SEED = 4321

fake = Faker()
fake.add_provider(address)
Faker.seed(SEED)

rand = random.Random()
rand.seed(SEED)
db = {'dbname':'tpch', 'user': 'postgres', 'password': 'postgres', 'host':'db' , 'port':'5432'}
connection = psycopg2.connect(**db)
cursor = connection.cursor()
connection.autocommit = True

cursor.execute("""-- region
CREATE TABLE IF NOT EXISTS region (
  r_regionkey  INT,
  r_name       TEXT,
  PRIMARY KEY (r_regionkey));

-- nation
CREATE TABLE IF NOT EXISTS nation (
  n_nationkey  INT,
  n_name       TEXT,
  n_regionkey  INT,
  PRIMARY KEY (n_nationkey),
  FOREIGN KEY (n_regionkey) REFERENCES region (r_regionkey) ON DELETE CASCADE);

-- supplier
CREATE TABLE IF NOT EXISTS supplier (
  s_suppkey     INT,
  s_name        TEXT,
  s_address     TEXT,
  s_nationkey   INT,
  s_phone       TEXT,
  PRIMARY KEY (s_suppkey),
  FOREIGN KEY (s_nationkey) REFERENCES nation (n_nationkey) ON DELETE CASCADE);

-- customer
CREATE TABLE IF NOT EXISTS customer (
  c_custkey     INT,
  c_name        TEXT,
  c_address     TEXT,
  c_nationkey   INT,
  c_phone       TEXT,
  PRIMARY KEY (c_custkey), 
  FOREIGN KEY (c_nationkey) REFERENCES nation (n_nationkey) ON DELETE CASCADE);

-- part
CREATE TABLE IF NOT EXISTS part (
  p_partkey     INT,
  p_name        TEXT,
  p_brand       TEXT,
  p_size        INT,
  p_retailprice DECIMAL(15,2) ,
  PRIMARY KEY (p_partkey));

-- partsupp
CREATE TABLE IF NOT EXISTS partsupp (
  ps_partkey     INT,
  ps_suppkey     INT,
  ps_supplycost  DECIMAL(15,2),
  PRIMARY KEY (ps_partkey, ps_suppkey),
  FOREIGN KEY (ps_partkey) REFERENCES part (p_partkey) ON DELETE CASCADE,
  FOREIGN KEY (ps_suppkey) REFERENCES supplier (s_suppkey) ON DELETE CASCADE);

-- orders
CREATE TABLE IF NOT EXISTS orders (
  o_orderkey       INT,
  o_custkey        INT,
  o_orderstatus    CHAR(1),
  o_orderdate      DATE,
  PRIMARY KEY (o_orderkey),
  FOREIGN KEY (o_custkey) REFERENCES customer (c_custkey) ON DELETE CASCADE);

-- lineitem
CREATE TABLE IF NOT EXISTS lineitem (
  l_orderkey          INT,
  l_partkey           INT,
  l_suppkey           INT,
  l_linenumber        INT,
  l_quantity          INT,
  l_extendedprice     FLOAT,
  PRIMARY KEY (l_linenumber),
  FOREIGN KEY (l_orderkey) REFERENCES orders (o_orderkey) ON DELETE CASCADE,
  FOREIGN KEY (l_partkey) REFERENCES part (p_partkey) ON DELETE CASCADE,
  FOREIGN KEY (l_suppkey) REFERENCES supplier (s_suppkey) ON DELETE CASCADE);""")

region_pks = range(1, 5)
for r in region_pks:
    name = f'region{r}'

    cursor.execute(f"""INSERT INTO region VALUES ({r}, '{name}');""")


nation_pks = range(1, 15)
for n in nation_pks:
    name = f'nation{n}'
    region_key = rand.choice(region_pks)

    cursor.execute(f"""INSERT INTO nation VALUES ({n}, '{name}', {region_key});""")
    

supp_pks = range(1, 30)
for s in supp_pks:
    name = fake.unique.company()
    address = fake.unique.address()
    nation_key = rand.choice(nation_pks)
    phone = fake.unique.phone_number()

    cursor.execute(f"""INSERT INTO supplier VALUES ({s}, '{name}', '{address}', {nation_key}, '{phone}');""")
    

customer_pks = range(1, 35)
for c in customer_pks:
    name = fake.unique.name()
    address = fake.unique.address()
    nation_key = rand.choice(nation_pks)
    phone = fake.unique.phone_number()

    cursor.execute(f"""INSERT INTO customer VALUES ({c}, '{name}', '{address}', {nation_key}, '{phone}');""")
    

part_pks = range(1, 60)
for p in part_pks:
    name = f'part{p}'
    brand = fake.unique.company()
    size = rand.randint(1, 25)
    price = rand.randint(1, 40) + rand.random()

    cursor.execute(f"""INSERT INTO part VALUES ({p}, '{name}', '{brand}', {size}, {price});""")
    

ps_pks = []
for i in range(31):
    part = rand.choice(part_pks)
    supp = rand.choice(supp_pks)

    if (part, supp) not in ps_pks:
        ps_pks.append((part, supp))

for part, supp in ps_pks:
    cost = rand.randint(1, 40) + rand.random()

    cursor.execute(f"""INSERT INTO partsupp VALUES ({part}, {supp}, {cost});""")
    

orders_pks = range(1, 30)
for o in orders_pks:
    cust = rand.choice(customer_pks)
    status = rand.choice(['P', 'F'])
    order_date = fake.date_between(start_date='-1y')

    cursor.execute(f"""INSERT INTO orders VALUES ({o}, {cust}, '{status}', '{order_date}');""")
    

lineitem_pks = range(101)
orders_ps_list_dict = {order_id:[] for order_id in orders_pks}
for l in lineitem_pks:
    order_key = rand.choice(orders_pks)
    part_supp = rand.choice(ps_pks)

    if part_supp not in orders_ps_list_dict[order_key]:
        orders_ps_list_dict[order_key].append(part_supp)
        qty = rand.randint(1, 60)
        cursor.execute(f"""SELECT ps_supplycost, p_retailprice
                           FROM part JOIN partsupp ON part.p_partkey = partsupp.ps_partkey
                           WHERE partsupp.ps_partkey = {part_supp[0]} AND partsupp.ps_suppkey = {part_supp[1]};""")
        result = cursor.fetchall()
        price = round(rand.randint(1, 300) + rand.random() + float(result[0][0] * result[0][1] * qty), 4)

        cursor.execute(f"INSERT INTO lineitem VALUES ({order_key}, {part_supp[0]}, {part_supp[1]}, {l}, {qty}, {price});")

print("DATABASE POPULATED SUCCEFULLY")
connection.close()
cursor.close()