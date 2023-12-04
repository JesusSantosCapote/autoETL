from query_generator.dsl.parser_rules import parser
import os
from query_generator.join_computation import compute_joins
from query_generator.maximal_join_trees import maximal_join_trees_generator
from query_generator.dsl.visitors import VisitorSymbolTable, VisitorSemanticCheck, VisitorGetSelects, VisitorPostgreSQL, VisitorGetTypes
from data_catalog.handler import DataCatalogHandler
from crawler.postgresSql_crawler import PostgreSqlCrawler
from config import CONNECTION_INFO_SOURCE
import psycopg2
from utils.load_graphs import load_graph, load_graph_list

path = os.path.join(os.getcwd(), 'input.txt')

code =''

with open(path) as file:
    code = file.read()

a = parser.parse(code)
st = VisitorSymbolTable()
st.visit_dimensional_model(a)
semantic = VisitorSemanticCheck(st.symbol_table)
semantic.visit_dimensional_model(a)
selects = VisitorGetSelects()
selects.visit_dimensional_model(a)
attr_to_select_for_dim = selects.selects_for_dimensions

db_params = {'dbname': CONNECTION_INFO_SOURCE['dbname'], 'user': CONNECTION_INFO_SOURCE['user'], 'password': CONNECTION_INFO_SOURCE['password'], 'host':CONNECTION_INFO_SOURCE['host'] , 'port': CONNECTION_INFO_SOURCE['port']}
crawler = PostgreSqlCrawler(db_params)
crawler.explore_db()
crawler.export_metadata_to_file()

datacatalog = DataCatalogHandler(crawler.get_db_dict(), db_params['dbname'], 'neo4j', 'datacatalog', 'bolt://neo4j_data_catalog:7687')
datacatalog.create_data_catalog()
datacatalog.export_join_graph()

join_graph = load_graph(db_params['dbname'])

type_check = VisitorGetTypes(join_graph)
type_check.visit_dimensional_model(a)

maximal_join_trees_generator(join_graph)
join_trees = load_graph_list(db_params['dbname'])

all_joins = []
for attrs in attr_to_select_for_dim:
    joins = compute_joins(join_trees, attrs)
    all_joins.append(joins[0]) #TODO here the user must select the join not select the 0 for defect

code_gen = VisitorPostgreSQL(all_joins, join_graph, type_check.dimensions_attrs, f"{db_params['dbname']}_target_querys")
code_gen.visit_dimensional_model(a)
code_gen.export_querys()


target_params = {'dbname': 'target', 'user': 'postgres', 'password': 'postgres', 'host':'target' , 'port':'5432'}
connection = psycopg2.connect(**target_params)
cursor = connection.cursor()
for key in code_gen.query_dict.keys():
    cursor.execute(code_gen.query_dict[key][0])

connection.close()
cursor.close()

source_params = {'dbname': CONNECTION_INFO_SOURCE['dbname'], 'user': CONNECTION_INFO_SOURCE['user'], 'password': CONNECTION_INFO_SOURCE['password'], 'host':CONNECTION_INFO_SOURCE['host'] , 'port': CONNECTION_INFO_SOURCE['port']}
connection = psycopg2.connect(**source_params)
cursor = connection.cursor()
for key in code_gen.query_dict.keys():
    cursor.execute(code_gen.query_dict[key][1])
    a = cursor.fetchall()
    print(a)
    print('\n')
