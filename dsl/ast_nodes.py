from dsl.visitors import Visitable, Visitor

class DimensionalModel(Visitable):
    def __init__(self, dimensional_table_list) -> None:
        self.dimensional_table_list = dimensional_table_list

    def accept(self, visitor: Visitor):
        visitor.visit_dimensional_model(self)


class Attribute(Visitable):
    def __init__(self, table_name, attr, primary_key=None) -> None:
        self.table_name = table_name
        self.name = attr
        self.primary_key = primary_key
    
    def accept(self, visitor:Visitor):
        visitor.visit_attribute(self)


class AttributeFunction(Visitable):
    def __init__(self, table_name, attr, func) -> None:
        self.table_name = table_name
        self.name = attr
        self.func = func

    def accept(self, visitor: Visitor):
        visitor.visit_attr_function(self)


class AggAttribute(Visitable):
    def __init__(self, table_name, attr, agg_func, grouping_attr, table_grouping_attr) -> None:
        self.table_name = table_name
        self.name = attr
        self.agg_function = agg_func
        self.grouping_attr = grouping_attr
        self.table_grouping_attr = table_grouping_attr

    def accept(self, visitor: Visitor):
        visitor.visit_agg_attr(self)


class AttributeExpression(Visitable):
    def __init__(self, elements, alias=None) -> None:
        self.elements = elements
        self.alias = alias
    
    def accept(self, visitor: Visitor):
        visitor.visit_attr_expression(self)


class DimensionalTable(Visitable):
    def __init__(self, name, list_attr) -> None:
        self.name = name
        self.list_attr = list_attr

    def accept(self, visitor: Visitor):
        visitor.visit_dimensional_table(self)


class Dimension(DimensionalTable):
    def __init__(self, name, list_attr) -> None:
        super().__init__(name, list_attr)
    
    def accept(self, visitor: Visitor):
        super().accept(visitor)


class Fact(DimensionalTable):
    def __init__(self, name, list_attr) -> None:
        super().__init__(name, list_attr)

    def accept(self, visitor: Visitor):
        super().accept(visitor)