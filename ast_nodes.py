class DimensionalModel():
    def __init__(self, dimensional_table_list) -> None:
        self.dimensional_table_list = dimensional_table_list


class Attribute():
    def __init__(self, table_name, attr, alias=None) -> None:
        self.table_name = table_name
        self.attr = attr
        self.alias = alias


class AggAttribute(Attribute):
    def __init__(self, table_name, attr, agg_func, grouping_attr, alias) -> None:
        super().__init__(table_name, attr, alias)
        self.agg_function = agg_func
        self.grouping_attr = grouping_attr


class ArithmeticAttribute():
    def __init__(self, list_attr, arith_expr_string, alias) -> None:
        self.list_attr = list_attr
        self.arith_expr_string = arith_expr_string
        self.alias = alias


class DimensionalTable():
    def __init__(self, name, list_attr) -> None:
        self.name = name
        self.list_attr = list_attr


class Dimension(DimensionalTable):
    def __init__(self, name, list_attr) -> None:
        super().__init__(name, list_attr)


class Fact(DimensionalTable):
    def __init__(self, name, list_attr) -> None:
        super().__init__(name, list_attr)
