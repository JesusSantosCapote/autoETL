from query_generator.dsl.parser_rules import parser
import os
from query_generator.join_computation import compute_joins
from query_generator.maximal_join_trees import maximal_join_trees_generator
from query_generator.dsl.visitors import VisitorNamingCheck, VisitorSemanticCheck, VisitorGetSelects, VisitorPostgreSQL, VisitorGetTypes
from data_catalog.handler import DataCatalogHandler
from crawler.postgreSql_crawler import PostgreSqlCrawler
import psycopg2
from utils.load_graphs import load_graph, load_graph_list

path = os.path.join(os.getcwd(), 'tpch.txt')

code ="""dimension supplier { supplier: s_suppkey PK as suppkey supplier: s_name as name supplier: s_phone as phone supplier: s_address as address nation: n_name as nation region: r_name as region }

dimension part { part: p_partkey PK part: p_name as name part: p_brand as brand part: p_size }

dimension order_date { orders: o_orderdate PK as o_date orders
(o_orderdate) str as day orders
(o_orderdate) str as month }

fact lineitem { self: linenumber PK serial as lnumber lineitem: l_partkey FK to part.p_partkey as partkey lineitem: l_suppkey FK to supplier.suppkey as supplierkey orders: o_orderdate FK to order_date.o_date as order_date lineitem: sum(l_extendedprice) as totalpayment lineitem: sum(l_quantity) as totalquantity lineitem: sum(l_extendedprice) - (lineitem: sum(l_quantity) * partsupp
) - (lineitem: sum(l_quantity) * part
) numeric as earnings }"""

with open(path) as file:
    code = file.read()

a = parser.parse(code)
st = VisitorNamingCheck()
st.visit_dimensional_model(a)
semantic = VisitorSemanticCheck(st.symbol_table)
semantic.visit_dimensional_model(a)
selects = VisitorGetSelects()
selects.visit_dimensional_model(a)
attr_to_select_for_dim = selects.selects_for_dimensions

db_params = {'dbname': 'tpch', 'user': 'postgres', 'password': 'postgres', 'host':'some-postgres' , 'port':'5432'}
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

code_gen = VisitorPostgreSQL(all_joins, join_graph, type_check.dimensions_attrs, f"{db_params['dbname']}_tpch_dw_querys")
code_gen.visit_dimensional_model(a)
code_gen.export_querys()


# target_params = {'dbname': 'target', 'user': 'postgres', 'password': 'postgres', 'host':'target' , 'port':'5432'}
# connection = psycopg2.connect(**target_params)
# cursor = connection.cursor()
# for key in code_gen.query_dict.keys():
#     cursor.execute(code_gen.query_dict[key][0])

# connection.close()
# cursor.close()

# source_params = {'dbname': 'tpch', 'user': 'postgres', 'password': 'postgres', 'host':'some-postgres' , 'port':'5432'}
# connection = psycopg2.connect(**source_params)
# cursor = connection.cursor()
# for key in code_gen.query_dict.keys():
#     cursor.execute(code_gen.query_dict[key][1])
#     a = cursor.fetchall()
#     print(a)
#     print('\n')
