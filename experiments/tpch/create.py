import psycopg2

connection = psycopg2.connect(user='postgres', password='postgres', host='db', port='5432')
cursor = connection.cursor()
connection.autocommit = True

# Database table list
try:
    cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = tpch;")
    existing_databases = cursor.fetchall()

except:
    # Create the database
    cursor.execute("CREATE DATABASE tpch;")
    print("DATABASE tpch CREATED")

connection.close()
cursor.close()