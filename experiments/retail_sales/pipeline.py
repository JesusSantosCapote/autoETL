import psycopg2
import os

connection = psycopg2.connect(user='postgres', password='postgres', host='target', port='5432')
cursor = connection.cursor()
connection.autocommit = True

cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'retail_dw';")
existing_databases = cursor.fetchall()

if existing_databases:
    print("Database retail_dw already exists.")
else:
    # Create the database
    cursor.execute("CREATE DATABASE retail_dw;")
    print("Database retail_dw created successfully.")
    
connection.close()
cursor.close()

connection_source = psycopg2.connect(dbname='retailsales', user='postgres', password='postgres', host='db', port='5432')
cursor_source = connection_source.cursor()
connection_source.autocommit = True

connection_target = psycopg2.connect(dbname='retail_dw', user='postgres', password='postgres', host='target', port='5432')
cursor_target = connection_target.cursor()
connection_target.autocommit = True

query_path = os.path.join(os.getcwd(), 'experiments', 'retail_sales')

#CREATES
with open(os.path.join(query_path, 'fecha_create.sql')) as file:
    cursor_target.execute(file.read())

with open(os.path.join(query_path, 'producto_create.sql')) as file:
    cursor_target.execute(file.read())

with open(os.path.join(query_path, 'tienda_create.sql')) as file:
    cursor_target.execute(file.read())

with open(os.path.join(query_path, 'venta_create.sql')) as file:
    cursor_target.execute(file.read())


#POPULATE DW
with open(os.path.join(query_path, 'tienda_select.sql')) as file:
    cursor_source.execute(file.read())
    rows = cursor_source.fetchall()
    for idtienda, nombre, reparto, municipio, provincia in rows:
        cursor_target.execute(f"""INSERT INTO tienda 
                              VALUES ({idtienda}, '{nombre}', '{reparto}', '{municipio}', '{provincia}')
                              ON CONFLICT (idtienda) 
                              DO UPDATE SET nombre = EXCLUDED.nombre, reparto = EXCLUDED.reparto, 
                              municipio = EXCLUDED.municipio, provincia = EXCLUDED.provincia;""")
        
with open(os.path.join(query_path, 'producto_select.sql')) as file:
    cursor_source.execute(file.read())
    rows = cursor_source.fetchall()
    for idproducto, marca, categoria, paquete, departamento, descripcion, producto, precio, costo in rows:
        cursor_target.execute(f"""INSERT INTO producto 
                              VALUES ({idproducto}, '{marca}', '{categoria}', '{paquete}', '{departamento}', '{descripcion}', '{producto}', {precio}, {costo})
                              ON CONFLICT (idproducto) 
                              DO UPDATE SET marca = EXCLUDED.marca, categoria = EXCLUDED.categoria, paquete = EXCLUDED.paquete,
                              departamento =  EXCLUDED.departamento, descripcion = EXCLUDED.descripcion, producto = EXCLUDED.producto,
                              precio = EXCLUDED.precio, costo = EXCLUDED.costo;""")
        
with open(os.path.join(query_path, 'fecha_select.sql')) as file:
    cursor_source.execute(file.read())
    rows = cursor_source.fetchall()
    for fecha, day, month in rows:
        cursor_target.execute(f"""INSERT INTO fecha 
                              VALUES ('{fecha}', '{day}', '{month}')
                              ON CONFLICT (fecha) 
                              DO UPDATE SET Dia = EXCLUDED.Dia, Mes = EXCLUDED.Mes;""")

with open(os.path.join(query_path, 'venta_select.sql')) as file:
    cursor_source.execute(file.read())
    rows = cursor_source.fetchall()
    for idproducto, idtienda, fecha, cantidad_vendida_total, importe_total, coste_total, ganancia in rows:
        cursor_target.execute(f"""INSERT INTO venta (idproducto, idtienda, fecha, cantidad_vendida_total, 
                              importe_total, coste_total, ganancia)
                              VALUES ({idproducto}, '{idtienda}', '{fecha}', '{cantidad_vendida_total}', 
                              '{importe_total}', '{coste_total}', '{ganancia}')
                              ON CONFLICT (idproducto, idtienda, fecha) 
                              DO UPDATE SET cantidad_vendida_total = EXCLUDED.cantidad_vendida_total, importe_total = EXCLUDED.importe_total, 
                              coste_total = EXCLUDED.coste_total, ganancia = EXCLUDED.ganancia;""")
        
with open(os.path.join(query_path, 'level_metadata.sql')) as file:
    cursor_target.execute(file.read())
        
print('PIPELINE EXECUTED SUCCEFULLY')