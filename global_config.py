import os 

LOG_FILE_PATH = os.path.join(os.getcwd(), 'logs.log')

CONNECTION_INFO_SOURCE = {
    'dialect' : 'postgresql',
    'driver' :  'psycopg2',
    'user': 'postgres',
    'password': 'postgres',
    'host': '172.20.0.2',
    'port': '5432',
    'dbname': 'retailsales',
}

