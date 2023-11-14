import abc
from logger import logger
from dsl.ast_nodes import Dimension, Fact, DimensionalModel, DimensionalTable, AttributeFunction, AggAttribute, Attribute, AttributeExpression

class Visitor(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def visit_dimensional_model(self, dimensional_model): pass 

    @abc.abstractmethod
    def visit_attribute(self, attribute): pass

    @abc.abstractmethod
    def visit_attr_function(self, attr_func): pass

    @abc.abstractmethod
    def visit_agg_attr(self, agg_attr): pass

    @abc.abstractmethod
    def visit_attr_expression(self, attr_expression): pass

    @abc.abstractmethod
    def visit_dimensional_table(self, dimensional_table): pass


class VisitorSymbolTable(Visitor):
    def __init__(self) -> None:
        self.symbol_table = {}
        self.good_naming = True

    def visit_dimensional_model(self, dimensional_model: DimensionalModel):
        for table in dimensional_model.dimensional_table_list:
            self.symbol_table[table.name] = []

        for table in dimensional_model.dimensional_table_list:
            table.accept(self)

    def visit_dimensional_table(self, dimensional_table: DimensionalTable):
        for attr_def, index in zip(dimensional_table.list_attr, range(1, len(dimensional_table.list_attr) + 1)):
            if attr_def.alias:
                if attr_def.alias in self.symbol_table[dimensional_table.name]:
                    logger.error(f'The alias {attr_def.alias} is used twice in table {dimensional_table.name}')
                    self.good_naming = False
                else:
                    self.symbol_table[dimensional_table.name].append(attr_def.alias)
            else:
                if len(attr_def.elements) == 1:
                    try: #attr_def.elements[0] may be a number and dont have name. SemanticCheck is responsable for notify this 
                        if attr_def.elements[0].name in self.symbol_table[dimensional_table.name]:
                            logger.error(f'The name {attr_def.elements[0].name} is used twice in table {dimensional_table.name}. Use an alias for fix this error.')
                            self.good_naming = False
                        else:
                            self.symbol_table[dimensional_table.name].append(attr_def.elements[0].name)
                    except:
                        self.symbol_table[dimensional_table.name].append('error')
                        self.good_naming = False
                else:
                    logger.error(f'Attribute number {index} in dimensional table {dimensional_table.name} is compound and dont have an alias.')
                    self.symbol_table[dimensional_table.name].append(None)
                    self.good_naming = False

    def visit_agg_attr(self, agg_attr):
        return super().visit_agg_attr(agg_attr)
    
    def visit_attr_expression(self, attr_expression):
        return super().visit_attr_expression(attr_expression)
    
    def visit_attr_function(self, attr_func):
        return super().visit_attr_function(attr_func)
    
    def visit_attribute(self, attribute):
        return super().visit_attribute(attribute)


class VisitorSemanticCheck(Visitor):
    def __init__(self, symbol_table) -> None:
        self.good_semantic = True
        self.symbol_table = symbol_table

    def visit_dimensional_model(self, dimensional_model: DimensionalModel):
        fact = False
        dimension = False

        for table in dimensional_model.dimensional_table_list:
            if isinstance(table, Fact):
                fact = True
            if isinstance(table, Dimension):
                dimension = True
        
        if not dimension and fact:
            logger.error("A Dimensional Model must have at least one Dimension and one Fact table")
            self.good_semantic = False

        for table in dimensional_model.dimensional_table_list:
            table.accept(self)


    def visit_dimensional_table(self, dimensional_table: DimensionalTable):
        PK_count = 0
        agg_attr_count = 0
        number_of_attr = 0
        for attr_expr, index in zip(dimensional_table.list_attr, range(1, len(dimensional_table.list_attr) + 1)):
            for attr in attr_expr.elements:
                if isinstance(attr, Attribute):
                    if attr.primary_key:
                        PK_count += 1
                
                if isinstance(attr, AggAttribute):
                    agg_attr_count += 1
                
                if isinstance(attr, (AggAttribute, Attribute, AttributeFunction)):
                    number_of_attr += 1
                    # if attr.table_name.startswith('Dim.'):
                    #     table = attr.table_name.split('.')[1]
                    #     if not table in self.symbol_table.keys():
                    #         logger.error(f"Dimensional Table {table} used but not defined")
                    #         self.good_semantic = False
                    #     else:
                    #         if not attr.name in self.symbol_table[table]:
                    #             logger.error(f"Attribute with {attr.name} as name or alias, refered in table {dimensional_table.name} is not defined in Dimensional Table {table}")
                    #             self.good_semantic = False

            if agg_attr_count > 1:
                if attr_expr.alias:
                    logger.error(f"Attribute {attr_expr.alias} in table {dimensional_table.name} have more than one aggregated attribute")
                else:
                    logger.error(f"Attribute number {index} in in table {dimensional_table.name} have more than one aggregated attribute")
                self.good_semantic = False

            agg_attr_count = 0

            if number_of_attr == 0:
                logger.error(f"Attribute definition number {index} in table {dimensional_table.name} must have at least one valid attribute")
                self.good_semantic = False
            
            number_of_attr = 0

        if PK_count > 1:
            logger.error(f"Dimensional Table: {dimensional_table.name} must have only one primary key")
            self.good_semantic = False

        if PK_count == 0:
            logger.error(f"Dimensional Table: {dimensional_table.name} must have a primary key")
            self.good_semantic = False

    def visit_agg_attr(self, agg_attr):
        return super().visit_agg_attr(agg_attr)
    
    def visit_attr_expression(self, attr_expression):
        return super().visit_attr_expression(attr_expression)
    
    def visit_attr_function(self, attr_func):
        return super().visit_attr_function(attr_func)
    
    def visit_attribute(self, attribute):
        return super().visit_attribute(attribute)
        

class VisitorPostgreSQL(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self.query_list = []

    def visit_dimensional_model(self, dimensional_model:DimensionalModel):
        for table in dimensional_model.dimensional_table_list:
            table.accept(self)

    def visit_dimensional_table(self, dimensional_table:DimensionalTable):
        query = ''
        attr_to_select = []
        for attr_expr in dimensional_table.list_attr:
            for elem in attr_expr.elements:
                if isinstance(elem, (Attribute, AttributeFunction, AggAttribute)):
                    if elem.table_name != 'self':
                            attr_to_select.append(elem)

                #join = compute_join(attr_to_select)
                        
            