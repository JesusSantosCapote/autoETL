from crawler.postgresSql_crawler import PostgreSqlCrawler
from Retail_Sales.config import CONNECTION_INFO
from data_catalog.handler import DataCatalogHandler
from networkx import DiGraph, path_graph
import pickle
import os

db_params = {
    'dbname': CONNECTION_INFO['dbname'],
    'user': CONNECTION_INFO['user'],
    'password': CONNECTION_INFO['password'],
    'host': CONNECTION_INFO['host'],
    'port': CONNECTION_INFO['port']
}


tpc_h = DiGraph()
tpc_h.add_node('part', attrs=[('partkey', 'integer', 'PRIMARY KEY'), 
                              ('name', 'character varying', 'Constraint_Not_Specified'), 
                              ('brand', 'character varying', 'Constraint_Not_Specified')], pks=['partkey'])

tpc_h.add_node('supplier', attrs=[('supkey', 'integer', 'PRIMARY KEY'), 
                                  ('name', 'character varying', 'Constraint_Not_Specified'), 
                                  ('nationkey', 'integer', 'FOREIGN KEY')], pks=['supkey'])

tpc_h.add_node('partsupp', attrs=[('partkey', 'integer', 'PK FK'), 
                                  ('supkey', 'integer', 'PK FK'), 
                                  ('qty', 'integer', 'Constraint_Not_Specified')], pks=['partkey', 'supkey'])

tpc_h.add_node('customer', attrs=[('custkey', 'integer', 'PRIMARY KEY'), 
                                  ('name', 'character varying', 'Constraint_Not_Specified'), 
                                  ('address', 'character varying', 'Constraint_Not_Specified'), 
                                  ('nationkey', 'integer', 'FOREIGN KEY')], pks=['custkey'])

tpc_h.add_node('orders', attrs=[('orderkey', 'integer', 'PRIMARY KEY'), 
                                ('custkey', 'integer', 'FOREIGN KEY'), 
                                ('status', 'character varying', 'Constraint_Not_Specified'), 
                                ('totalprice', 'integer', 'Constraint_Not_Specified')], pks=['orderkey'])

tpc_h.add_node('lineitem', attrs=[('orderkey', 'integer', 'FOREIGN KEY'), 
                                  ('partkey', 'integer', 'FOREIGN KEY'), 
                                  ('supkey', 'integer', 'FOREIGN KEY'), 
                                  ('linenumber', 'integer', 'PRIMARY KEY'), 
                                  ('status', 'character varying', 'Constraint_Not_Specified'), 
                                  ('qty', 'integer', 'Constraint_Not_Specified')], pks=['linenumber'])

tpc_h.add_node('nation', attrs=[('nationkey', 'integer', 'PRIMARY KEY'), 
                                ('name', 'character varying', 'Constraint_Not_Specified'), 
                                ('regionkey', 'integer', 'FOREIGN KEY'), 
                                ('comment', 'character varying', 'Constraint_Not_Specified')], pks=['nationkey'])

tpc_h.add_node('region', attrs=[('regionkey', 'integer', 'PRIMARY KEY'), 
                                ('name', 'character varying', 'Constraint_Not_Specified'), 
                                ('comment', 'character varying', 'Constraint_Not_Specified')], pks=['regionkey'])

edges = [
    ('lineitem', 'part', {'conditions': [('partkey', 'partkey')], 'weight':1}),
    ('lineitem', 'supplier', {'conditions': [('supkey', 'supkey')], 'weight':1}),
    ('lineitem', 'partsupp', {'conditions': [('partkey', 'partkey'), ('supkey', 'supkey')], 'weight':1}),
    ('lineitem', 'orders', {'conditions':[('orderkey', 'orderkey')], 'weight':1}),
    ('partsupp', 'part', {'conditions': [('partkey', 'partkey')], 'weight':1}),
    ('partsupp', 'supplier', {'conditions': [('supkey', 'supkey')], 'weight':1}),
    ('supplier', 'nation', {'conditions': [('nationkey', 'nationkey')], 'weight':1}),
    ('nation', 'region', {'conditions': [('regionkey', 'regionkey')], 'weight':1}),
    ('orders', 'customer', {'conditions': [('custkey', 'custkey')], 'weight':1}),
    ('customer', 'nation', {'conditions': [('nationkey', 'nationkey')], 'weight':1})
]

tpc_h.add_edges_from(edges)
graph1 = path_graph((1,2,3))
e = [tpc_h, graph1]

a = pickle.dumps(e)

b = pickle.loads(a)

print(type(b))