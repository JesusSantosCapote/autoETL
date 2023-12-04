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
db = {'dbname':'tpch', 'user': 'postgres', 'password': 'postgres', 'host':'some-postgres' , 'port':'5432'}
connection = psycopg2.connect(**db)
cursor = connection.cursor()
connection.autocommit = True

with open(os.path.join(os.getcwd(), 'tpch.sql'), 'r') as file:
    cursor.execute(file.read())

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