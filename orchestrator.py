from query_generator.dsl.parser_rules import parser
import os
from query_generator.join_computation import compute_joins
from query_generator.maximal_join_trees import maximal_join_trees_generator
from query_generator.dsl.visitors import VisitorSymbolTable, VisitorSemanticCheck, VisitorGetSelects, VisitorPostgreSQL, VisitorGetTypes
from data_catalog.handler import DataCatalogHandler
from crawler.postgresSql_crawler import PostgreSqlCrawler
import psycopg2
from utils.load_graphs import load_graph, load_graph_list

class Orchestrator():
    def __init__(self, dbname) -> None:
        self.attr_to_select_for_dim = []
        self.dbname = dbname
        self.join_graph = load_graph(dbname)
        self.code_is_good = True
        self.all_joins = []
        self.dimensional_model = None
        self.attr_types = []

    def parse_code(self, code):
        ast = parser.parse(code)
        self.dimensional_model = ast
        symbol_table = VisitorSymbolTable()
        symbol_table.visit_dimensional_model(ast)
        semantic = VisitorSemanticCheck(symbol_table.symbol_table)
        semantic.visit_dimensional_model(ast)
        selects = VisitorGetSelects()
        selects.visit_dimensional_model(ast)
        self.attr_to_select_for_dim = selects.selects_for_dimensions

        type_check = VisitorGetTypes(self.join_graph)
        type_check.visit_dimensional_model(ast)
        self.attr_types = type_check.dimensions_attrs

        self.code_is_good = symbol_table.good_naming and semantic.good_semantic and type_check.good_type

    def compute_joins(self):
        join_trees = load_graph_list(self.dbname)

        for attrs in self.attr_to_select_for_dim:
            joins = compute_joins(join_trees, attrs)
            self.all_joins.append(joins)

        dimensions_names = []
        for table in self.dimensional_model.dimensional_table_list:
            dimensions_names.append(table)

        return list(zip(dimensions_names, self.all_joins))
    

    def generate_querys(self, selected_joins, dwname, script_name):
        code_gen = VisitorPostgreSQL(selected_joins, self.join_graph, self.attr_types, f"{self.dbname}-{dwname}-{script_name}-querys")
        code_gen.visit_dimensional_model(self.dimensional_model)
        code_gen.export_querys()

        