from dsl.visitable import Visitable

class DimensionalModel(Visitable):
    def __init__(self, dimensional_table_list) -> None:
        self.dimensional_table_list = dimensional_table_list

    def accept(self, visitor):
        visitor.visit_dimensional_model(self)


class Attribute(Visitable):
    def __init__(self, table_name, attr, primary_key=None, foreign_key=None) -> None:
        self.table_name = table_name
        self.name = attr
        self.primary_key = primary_key
        self.foreign_key = foreign_key
    
    def accept(self, visitor):
        visitor.visit_attribute(self)


class AttributeFunction(Visitable):
    def __init__(self, table_name, attr, func) -> None:
        self.table_name = table_name
        self.name = attr
        self.func = func

    def accept(self, visitor):
        visitor.visit_attr_function(self)


class AggAttribute(Visitable):
    def __init__(self, table_name, attr, agg_func) -> None:
        self.table_name = table_name
        self.name = attr
        self.agg_function = agg_func

    def accept(self, visitor):
        visitor.visit_agg_attr(self)


class AttributeExpression(Visitable):
    def __init__(self, elements, exp_type=None, alias=None) -> None:
        self.elements = elements
        self.alias = alias
        self.exp_type = exp_type
    
    def accept(self, visitor):
        visitor.visit_attr_expression(self)


class DimensionalTable(Visitable):
    def __init__(self, name, list_attr) -> None:
        self.name = name
        self.list_attr = list_attr

    def accept(self, visitor):
        visitor.visit_dimensional_table(self)


class Dimension(DimensionalTable):
    def __init__(self, name, list_attr) -> None:
        super().__init__(name, list_attr)
    
    def accept(self, visitor):
        super().accept(visitor)


class Fact(DimensionalTable):
    def __init__(self, name, list_attr) -> None:
        super().__init__(name, list_attr)

    def accept(self, visitor):
        super().accept(visitor)