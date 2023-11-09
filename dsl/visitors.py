import abc
from logger import logger


class Visitable(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def accept(self, visitor):
        pass


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

    def visit_dimensional_model(self, dimensional_model):
        for table in dimensional_model.dimensional_table_list:
            self.symbol_table[table.name] = []

        for table in dimensional_model.dimensional_table_list:
            table.accept(self)

    def visit_dimensional_table(self, dimensional_table):
        for attr_def, index in zip(dimensional_table.list_attr, range(len(dimensional_table.list_attr))):
            if attr_def.alias:
                self.symbol_table[dimensional_table.name].append(attr_def.alias)
            else:
                if len(attr_def.elements) == 1:
                    try: #attr_def.elements[0] may be a number and dont have name. SemanticCheck is responsable for notify this 
                        self.symbol_table[dimensional_table.name].append(attr_def.elements[0].name)
                    except:
                        self.symbol_table[dimensional_table.name].append('error')
                else:
                    logger.error(f'Attribute number {index} in dimensional table {dimensional_table.name} is compound and dont have an alias.')
                    self.symbol_table[dimensional_table.name].append(None)

    def visit_agg_attr(self, agg_attr):
        return super().visit_agg_attr(agg_attr)
    
    def visit_attr_expression(self, attr_expression):
        return super().visit_attr_expression(attr_expression)
    
    def visit_attr_function(self, attr_func):
        return super().visit_attr_function(attr_func)
    
    def visit_attribute(self, attribute):
        return super().visit_attribute(attribute)


class VisitorSemanticCheck(Visitor):
    def __init__(self) -> None:
        self.good_semantic = True

    def visit_dimensional_model(self, dimensional_model):
        
        for table in dimensional_model.dimensional_table_list:
            table.accept(self)

    def visit_dimensional_table(self, dimensional_table):
        if dimensional_table.list_attr:
            pass
        

    