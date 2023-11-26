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
                    logger.error(f'Attribute number {index} in dimensional table {dimensional_table.name} is composite and dont have an alias.')
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


class VisitorTypeCheck(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self.good_type = True

    def visit_dimensional_model(self, dimensional_model:DimensionalModel):
        for table in dimensional_model.dimensional_table_list:
            table.accept(self)

    def visit_dimensional_table(self, dimensional_table:DimensionalTable):
        for attr_expr in dimensional_table.list_attr:
            if len(attr_expr.elements) > 1:
                if not attr_expr.exp_type:
                    logger.error(f'Missing type declaration for composite attribute definition in table: {dimensional_table.name}')
                    self.good_type = False
    
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
        

class VisitorGetSelects(Visitor):
    def __init__(self) -> None:
        super().__init__()
        self.selects_for_dimensions = []

    def visit_dimensional_model(self, dimensional_model:DimensionalModel):
        for table in dimensional_model.dimensional_table_list:
            table.accept(self)

    def visit_dimensional_table(self, dimensional_table):
        attr_to_select = []
        for attr_expr in dimensional_table.list_attr:
            for elem in attr_expr.elements:
                if isinstance(elem, (Attribute, AttributeFunction, AggAttribute)):
                    if elem.table_name != 'self' and not elem.table_name.startswith('Dim.') :
                            attr_to_select.append((elem.table_name, elem.name))

        self.selects_for_dimensions.append(attr_to_select)

    def visit_attribute(self, attribute):
        return super().visit_attribute(attribute)
    def visit_attr_function(self, attr_func):
        return super().visit_attr_function(attr_func)
    def visit_agg_attr(self, agg_attr):
        return super().visit_agg_attr(agg_attr)
    def visit_attr_expression(self, attr_expression):
        return super().visit_attr_expression(attr_expression)


class VisitorGetTypes(Visitor):
    def __init__(self, join_graph) -> None:
        super().__init__()
        self.dimensions_attrs = {}
        self.good_type = True
        self.join_graph = join_graph

    def visit_dimensional_model(self, dimensional_model:DimensionalModel):
        for dimension_table in dimensional_model.dimensional_table_list:
            self.dimensions_attrs[dimension_table] = {}
            dimension_table.accept(self)

    def visit_dimensional_table(self, dimensional_table:DimensionalTable):
        for attr_expr, index in zip(dimensional_table.list_attr, range(len(dimensional_table.list_attr))):
            if len(attr_expr.elements) > 1:
                if not attr_expr.exp_type:
                    logger.error(f'Missing type declaration for composite attribute definition number {index} in table: {dimensional_table.name}')
                    self.good_type = False

                else:
                    self.dimensions_attrs[dimensional_table.name][attr_expr.alias] = attr_expr.exp_type

            else:
                if attr_expr.alias:
                    if attr_expr.exp_type:
                        self.dimensions_attrs[dimensional_table.name][attr_expr.alias] = attr_expr.exp_type
                    
                    else:
                        attr = attr_expr.elements[0]
                        if attr.table_name == 'self':
                            if isinstance(attr, AttributeFunction):
                                if attr.func in ['week_day', 'month_str']:
                                    self.dimensions_attrs[dimensional_table.name][attr_expr.alias] = 'str'
                            #This is because i dont allow declarations of new attr for the moment
                            else:
                                logger.error(f'Definitions of new attributes are not allowed: attribute number {index} in dimensional table {dimensional_table.name}')
                                self.good_type = False
                        
                        elif attr.table_name.startswith('Dim.'):
                            if isinstance(attr, Attribute):
                                if attr.foreign_key:
                                    dimension = attr.table_name.split('.')[1]
                                    try:
                                        attr_type = self.dimensions_attrs[dimension][attr.name]
                                        self.dimensions_attrs[dimensional_table.name][attr_expr.alias] = attr_type
                                    except KeyError:
                                        logger.error(f'Attribute {attr.name} not declared in dimensional table {dimension}')
                                        self.good_type = False
                                    
                                else:
                                    logger.error(f'For referencing another table the attribute must be a foreign key: attribute number {index} in dimensional table {dimensional_table.name}')
                                    self.good_type = False

                            else:
                                logger.error(f'Invalid combination of table and attribute: attribute number {index} in dimensional table {dimensional_table.name}')

                        else:
                            for attr_name, attr_type, _ in self.join_graph.nodes[attr.table_name]['attrs']:
                                if attr.name == attr_name:
                                    self.dimensions_attrs[dimensional_table.name][attr_expr.alias] = attr_type
                                    break
                    
                else: #TODO si no tiene alias hay que hacer lo mismo de arriba, modificar la estructura del if
                    attr = attr_expr.elements[0]
                    for attr_name, attr_type, _ in self.join_graph.nodes[attr.table_name]['attrs']:
                            if attr.name == attr_name:
                                self.dimensions_attrs[dimensional_table.name][attr.name] = attr_type
                                break


class VisitorPostgreSQL(Visitor):
    def __init__(self, join_list, join_tree) -> None:
        super().__init__()
        self.query_list = []
        self.join_tree = join_tree
        self.dsl_types_to_postgres = {'int': 'INT', 'str': 'TEXT', 'date': 'DATE', 'datetime': 'TIMESTAMP'}
        self.dsl_agg_to_postgres = {'sum': 'SUM', 'avg': 'AVG', 'count': 'COUNT'}
        self.join_list = join_list
        self.join_index = 0

    def visit_dimensional_model(self, dimensional_model:DimensionalModel):
        for table in dimensional_model.dimensional_table_list:
            table.accept(self)

    def visit_dimensional_table(self, dimensional_table:DimensionalTable):
        query_create = 'CREATE TABLE [IF NOT EXIST] %s ('
        select_part = 'SELECT '
        from_part = 'FROM '
        groupby_part = ''

        for attr_expr in dimensional_table.list_attr:
            #Name
            if attr_expr.alias:
                query_create = query_create + attr_expr.alias
            else:
                query_create = query_create + attr_expr.elements[0].name
            #Type
            if attr_expr.exp_type:
                query_create = query_create + self.dsl_types_to_postgres[attr_expr.exp_type]
            else:
                source_table = attr_expr.elements[0].table_name
                source_attr = attr_expr.elements[0].name
                for attr_name, attr_type, _ in self.join_tree.nodes[source_table]['attrs']:
                    if attr_name == source_attr:
                        query_create = query_create + attr_type
                        break
            #PK Constraint
            if len(attr_expr.elements) == 1:
                if isinstance(attr_expr.elements[0], Attribute):
                    if attr_expr.elements[0].primary_key:
                        query_create = query_create + 'PRIMARY KEY'

            query_create = query_create + ', \n'    

        #FK Constraints
        for attr_expr in dimensional_table.list_attr:
            if len(attr_expr.elements) == 1:
                if isinstance(attr_expr.elements[0], Attribute):
                    if attr_expr.elements[0].foreign_key:
                        references = attr_expr.elements[0].table_name.split('.')[1]
                        name = attr_expr.elements[0].name
                        if attr_expr.alias:
                            name = attr_expr.alias
                        query_create = query_create + f'FOREIGN KEY ({name})' + f'REFERENCES {references} ({attr_expr.elements[0].name}), \n'

        query_create = query_create[0:-2] #Deleting the last ,
        query_create = query_create + ');'

        #SELECT statement
        for attr_expr, index in zip(dimensional_table.list_attr, range(len(dimensional_table.list_attr))):
            for elem in attr_expr.elements:
                if isinstance(elem, Attribute):
                    select_part = select_part + f'{elem.table_name}.{elem.name}'
                elif isinstance(elem, AttributeFunction):
                    if elem.func == 'week_day':
                        if elem.table_name != 'self':
                            select_part = select_part + f"to_char({elem.table_name}.{elem.name}, 'Day')"
                        else:
                            select_part = select_part + f"to_char({elem.name}, 'Day')"

                    if elem.func == 'month_str':
                        if elem.table_name != 'self':
                            select_part = select_part + f"to_char({elem.table_name}.{elem.name}, 'Month')"
                        else:
                            select_part = select_part + f"to_char({elem.name}, 'Month')"
                
                elif isinstance(elem, AggAttribute): #TODO check if here i must to check if self is a valid table_name for this kind of attr
                    select_part = select_part + f'{self.dsl_agg_to_postgres[elem.agg_function]}({elem.table_name}.{elem.name})'
                    groupby_part = groupby_part + f'GROUP BY {elem.table_grouping_attr}.{elem.grouping_attr}'

                else:
                    select_part = select_part + elem
            
            if index < len(dimensional_table.list_attr) - 1:
                select_part = select_part + ','

        #FROM statement
        join = self.join_list[self.join_index]
        from_part = from_part
        for i in range(0, len(join), 2):
            if i == 0:
                select_part = select_part + join[i]
            else:
                conditions = ''
                for cond, index in zip(join[i-1], range(len(join[i-1]))):
                    conditions = conditions + f'{join[i-2]}.{cond[0]} = {join[i]}.{cond[1]}'
                    if index != len(join[i-1]) - 1:
                        conditions = conditions + 'AND'
                select_part = select_part + f'JOIN f{join[i]} ON' + conditions

        select_part = select_part + from_part + groupby_part + ';'
        self.query_list.append((query_create, select_part)) 

    def visit_attr_expression(self, attr_expression):
        return super().visit_attr_expression(attr_expression)
    def visit_agg_attr(self, agg_attr):
        return super().visit_agg_attr(agg_attr)
    def visit_attr_function(self, attr_func):
        return super().visit_attr_function(attr_func)
    def visit_attribute(self, attribute):
        return super().visit_attribute(attribute)
        
