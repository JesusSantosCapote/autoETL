from dsl.parser_rules import parser
import os
from dsl.visitors import VisitorSymbolTable, VisitorSemanticCheck

path = os.path.join(os.getcwd(), 'input.txt')

code =''

with open(path) as file:
    code = file.read()

a = parser.parse(code)

st = VisitorSymbolTable()

st.visit_dimensional_model(a)

semantic = VisitorSemanticCheck(st.symbol_table)

semantic.visit_dimensional_model(a)

print(st.symbol_table)
print(semantic.good_semantic)