from dsl.parser_rules import parser
import os
from query_generator.join_computation import compute_joins
from query_generator.maximal_join_trees import maximal_join_trees_generator
from dsl.visitors import VisitorSymbolTable, VisitorSemanticCheck, VisitorGetSelects, VisitorPostgreSQL, VisitorTypeCheck
from data_catalog.handler import DataCatalogHandler
from crawler.postgresSql_crawler import PostgreSqlCrawler
from Retail_Sales.config import CONNECTION_INFO

path = os.path.join(os.getcwd(), 'input.txt')

code =''

with open(path) as file:
    code = file.read()

a = parser.parse(code)
st = VisitorSymbolTable()
st.visit_dimensional_model(a)
semantic = VisitorSemanticCheck(st.symbol_table)
semantic.visit_dimensional_model(a)
type_check = VisitorTypeCheck()
type_check.visit_dimensional_model(a)
selects = VisitorGetSelects()
selects.visit_dimensional_model(a)
attr_to_select_for_dim = selects.selects_for_dimensions

db_params = {'dbname': CONNECTION_INFO['dbname'], 'user': CONNECTION_INFO['user'], 'password': CONNECTION_INFO['password'], 'host':CONNECTION_INFO['host'] , 'port': CONNECTION_INFO['port']}
crawler = PostgreSqlCrawler(db_params)
crawler.explore_db()

datacatalog = DataCatalogHandler(crawler.get_db_dict(), 'neo4j', 'datacatalog', 'bolt://172.20.0.4:7687')
datacatalog.create_data_catalog()
join_graph = datacatalog.get_join_graph()

join_trees = maximal_join_trees_generator(join_graph)

all_joins = []
for attrs in attr_to_select_for_dim:
    joins = compute_joins(join_trees, attrs)
    all_joins.append(joins[0]) #TODO here the user must select the join not select the 0 for defect

code_gen = VisitorPostgreSQL(all_joins, join_graph)
code_gen.visit_dimensional_model(a)

print(code_gen.query_list)
