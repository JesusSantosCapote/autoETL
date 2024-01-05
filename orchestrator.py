import abc
from query_generator.dsl.parser_rules import parser
from query_generator.join_computation import compute_joins
from query_generator.maximal_join_trees import maximal_join_trees_generator
from query_generator.dsl.visitors import VisitorNamingCheck, VisitorSemanticCheck, VisitorGetSelects, VisitorPostgreSQL, VisitorGetTypes, VisitorGetLevel, VisitorPostgreSQLCreate, VisitorPostgreSQLSelect
from data_catalog.handler import DataCatalogHandler
from crawler.postgreSql_crawler import PostgreSqlCrawler
from utils.load_graphs import load_graph, load_graph_list


class Orchestrator:
    def __init__(self, dbname, dwname, source_sgbd, target_sgbd, script) -> None:
        self.attr_to_select_for_dim = []
        self.dbname = dbname
        self.dwname = dwname
        self.join_graph = load_graph(dbname)
        self.code_is_good = True
        self.all_joins = []
        self.dimensional_model = None
        self.attr_types = []
        self.level_dict = None
        self.source_sgbd = source_sgbd
        self.target_sgbd = target_sgbd
        self.script = script

    def parse_code(self, code):
        ast = parser.parse(code)
        self.dimensional_model = ast
        symbol_table = VisitorNamingCheck()
        symbol_table.visit_dimensional_model(ast)
        
        semantic = VisitorSemanticCheck(symbol_table.symbol_table, self.join_graph)
        if symbol_table.good_naming:
            semantic.visit_dimensional_model(ast)
        
        type_check = VisitorGetTypes(self.join_graph)
        if semantic.good_semantic:
            type_check.visit_dimensional_model(ast)
            self.attr_types = type_check.dimensions_attrs

        self.code_is_good = symbol_table.good_naming and semantic.good_semantic and type_check.good_type
        if self.code_is_good:
            selects = VisitorGetSelects()
            selects.visit_dimensional_model(ast)
            self.attr_to_select_for_dim = selects.selects_for_dimensions

        
    def compute_joins(self):
        join_trees = load_graph_list(self.dbname)

        for attrs in self.attr_to_select_for_dim:
            joins = compute_joins(join_trees, attrs)
            self.all_joins.append(joins)

        dimensions_names = []
        for table in self.dimensional_model.dimensional_table_list:
            dimensions_names.append(table)

        return list(zip(dimensions_names, self.all_joins))
    
    def generate_querys(self, selected_joins):
        level_visitor = VisitorGetLevel()
        level_visitor.visit_dimensional_model(self.dimensional_model)
        source_visitor = {
            'PostgreSQL': VisitorPostgreSQLSelect(selected_joins, f"{self.dbname}-{self.dwname}-{self.script}-querys", level_visitor.level_dict)
            }

        target_visitor = {
            'PostgreSQL': VisitorPostgreSQLCreate(self.join_graph, self.attr_types, f"{self.dbname}-{self.dwname}-{self.script}-querys", level_visitor.level_dict)
            }        

        source_code_gen = source_visitor[self.source_sgbd]
        target_code_gen = target_visitor[self.target_sgbd]

        source_code_gen.visit_dimensional_model(self.dimensional_model)
        source_code_gen.export_querys()

        target_code_gen.visit_dimensional_model(self.dimensional_model)
        target_code_gen.export_querys()
