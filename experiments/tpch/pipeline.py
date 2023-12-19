import psycopg2
import os

connection = psycopg2.connect(user='postgres', password='postgres', host='target', port='5432')
cursor = connection.cursor()
connection.autocommit = True

cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'tpch_dw';")
existing_databases = cursor.fetchall()

if existing_databases:
    print("Database tpch_dw already exists.")
else:
    # Create the database
    cursor.execute("CREATE DATABASE tpch_dw;")
    print("Database tpch_dw created successfully.")
    
connection.close()
cursor.close()

connection_source = psycopg2.connect(dbname='tpch', user='postgres', password='postgres', host='db', port='5432')
cursor_source = connection_source.cursor()
connection_source.autocommit = True

connection_target = psycopg2.connect(dbname='tpch_dw', user='postgres', password='postgres', host='target', port='5432')
cursor_target = connection_target.cursor()
connection_target.autocommit = True

query_path = os.path.join(os.getcwd(), 'experiments', 'tpch')

#CREATES
with open(os.path.join(query_path, 'supplier_create.sql')) as file:
    cursor_target.execute(file.read())

with open(os.path.join(query_path, 'part_create.sql')) as file:
    cursor_target.execute(file.read())

with open(os.path.join(query_path, 'order_date_create.sql')) as file:
    cursor_target.execute(file.read())

with open(os.path.join(query_path, 'lineitem_create.sql')) as file:
    cursor_target.execute(file.read())


#POPULATE DW
with open(os.path.join(query_path, 'supplier_select.sql')) as file:
    cursor_source.execute(file.read())
    rows = cursor_source.fetchall()
    for suppkey, name, phone, address, nation, region in rows:
        cursor_target.execute(f"""INSERT INTO supplier 
                              VALUES ({suppkey}, '{name}', '{phone}', '{address}', '{nation}', '{region}')
                              ON CONFLICT (suppkey) 
                              DO UPDATE SET name = EXCLUDED.name, phone = EXCLUDED.phone, 
                              address = EXCLUDED.address, nation = EXCLUDED.nation,
                              region = EXCLUDED.region;""")
        
with open(os.path.join(query_path, 'part_select.sql')) as file:
    cursor_source.execute(file.read())
    rows = cursor_source.fetchall()
    for p_partkey, name, brand, p_size in rows:
        cursor_target.execute(f"""INSERT INTO part 
                              VALUES ({p_partkey}, '{name}', '{brand}', {p_size})
                              ON CONFLICT (p_partkey) 
                              DO UPDATE SET name = EXCLUDED.name, brand = EXCLUDED.brand, 
                              p_size = EXCLUDED.p_size;""")
        
with open(os.path.join(query_path, 'order_date_select.sql')) as file:
    cursor_source.execute(file.read())
    rows = cursor_source.fetchall()
    for o_date, day, month in rows:
        cursor_target.execute(f"""INSERT INTO order_date 
                              VALUES ('{o_date}', '{day}', '{month}')
                              ON CONFLICT (o_date) 
                              DO UPDATE SET day = EXCLUDED.day, month = EXCLUDED.month;""")

with open(os.path.join(query_path, 'lineitem_select.sql')) as file:
    cursor_source.execute(file.read())
    rows = cursor_source.fetchall()
    for partkey, supplierkey, order_date, totalpayment, totalquantity, earnings in rows:
        cursor_target.execute(f"""INSERT INTO lineitem (partkey, supplierkey, order_date, totalpayment, 
                              totalquantity, earnings)
                              VALUES ({partkey}, '{supplierkey}', '{order_date}', '{totalpayment}', 
                              '{totalquantity}', '{earnings}')
                              ON CONFLICT (partkey, supplierkey, order_date) 
                              DO UPDATE SET totalpayment = EXCLUDED.totalpayment, totalquantity = EXCLUDED.totalquantity, 
                              earnings = EXCLUDED.earnings;""")
        
print('PIPELINE EXECUTED SUCCEFULLY')