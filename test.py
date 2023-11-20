from crawler.postgresSql_crawler import PostgreSqlCrawler
from Retail_Sales.config import CONNECTION_INFO
from data_catalog.handler import DataCatalogHandler

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

dc = DataCatalogHandler(c.get_db_dict(), 'neo4j', 'datacatalog', 'bolt://172.20.0.4:7687')

dc.create_data_catalog()

dc.get_join_graph()