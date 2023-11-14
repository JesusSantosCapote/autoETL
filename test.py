from crawler.postgresSql_crawler import PostgreSqlCrawler
from Retail_Sales.config import CONNECTION_INFO

db_params = {
    'dbname': CONNECTION_INFO['dbname'],
    'user': CONNECTION_INFO['user'],
    'password': CONNECTION_INFO['password'],
    'host': CONNECTION_INFO['host'],
    'port': CONNECTION_INFO['port']
}

c = PostgreSqlCrawler(db_params)

c.explore_db()

c.export_metadata_to_file()