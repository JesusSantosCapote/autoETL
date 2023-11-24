from ply import yacc
from dsl.ast_nodes import *
from dsl.lexer import tokens
from logger import logger


def p_Dimensional_Model(p):
    '''Dimensional_Model : List_Dimensional_Tables'''
    p[0] = DimensionalModel(p[1])


def p_List_First(p):
    '''List_Dimensional_Tables : Dimensional_Table
       List_Attr_Def : Attr_Def'''
    p[0] = [p[1]]


def p_List_Dimensional_Tables(p):
    '''List_Dimensional_Tables : List_Dimensional_Tables Dimensional_Table'''
    p[0] = p[1]
    p[0].append(p[2])


def p_Dimensional_Table(p):
    '''Dimensional_Table : DIM ID LBRACE List_Attr_Def RBRACE
                         | FACT ID LBRACE List_Attr_Def RBRACE'''
    if p[1] == 'dimension':
        p[0] = Dimension(p[2], p[4])

    if p[1] == 'fact':
        p[0] = Fact(p[2], p[4])


def p_List_Attr_Def(p):
    '''List_Attr_Def : List_Attr_Def Attr_Def'''
    p[0] = p[1]
    p[0].append(p[2])


def p_Attr_Def(p):
    '''Attr_Def : Attr_Expression Type Alias'''
    p[0] = p[1]
    p[0].alias = p[3]
    p[0].exp_type = p[2]


def p_Attr_Expression(p):
    '''Attr_Expression : T X'''
    p[0] = AttributeExpression(p[1] + p[2])


def p_X(p):
    '''X : PLUS T X
         | MINUS T X
         | empty_list'''
    if p[1] == '+':
       p[0] = ['+'] + p[2] + p[3]

    elif p[1] == '-':
       p[0] = ['-'] + p[2] + p[3]

    else:
        p[0] = p[1]

   
def p_T(p):
    '''T : F Y'''
    p[0] = p[1] + p[2] 


def p_Y(p):
    '''Y : TIMES F Y
         | DIVIDE F Y
         | empty_list'''
    if p[1] == '*':
       p[0] = ['*'] + p[2] + p[3]  

    elif p[1] == '/':
       p[0] = ['/'] + p[2] + p[3]

    else:
        p[0] = p[1]       


def p_F(p):
    '''F : Attr
         | NUMBER
         | LPAREN Attr_Expression RPAREN'''
    if len(p) == 2:
        p[0] = [p[1]]

    if len(p) == 4:
        p[0] = ['('] + p[2].elements + [')'] 
    

def p_Attr(p):
    '''Attr : Table TWODOTS ID Modifier
            | Table TWODOTS Func LPAREN ID RPAREN
            | Table TWODOTS SUM LPAREN ID RPAREN GROUP Table TWODOTS ID
            | Table TWODOTS AVG LPAREN ID RPAREN GROUP Table TWODOTS ID
            | Table TWODOTS COUNT LPAREN ID RPAREN GROUP Table TWODOTS ID'''
            
    if len(p) == 5:
        if p[4] == 'PK':
            p[0] = Attribute(p[1], p[3], primary_key=p[4])
        if p[4] == 'FK':
            p[0] = Attribute(p[1], p[3], foreign_key=p[4])

    if len(p) == 7:
        p[0] = AttributeFunction(p[1], p[5], p[3])

    if len(p) == 11:
        p[0] = AggAttribute(p[1], p[5], p[3], p[10], p[8])


def p_Table(p):
    '''Table : ID
             | SELF'''
    p[0] = p[1]


def p_Func(p):
    '''Func : WEEKDAY
            | MONTHSTR'''
    p[0] = p[1]


def p_Alias(p):
    '''Alias : AS ID
             | empty'''
    if len(p) == 3:
        p[0] = p[2]


def p_Type(p):
    '''Type : INT
            | STR
            | DATE
            | DATETIME
            | empty'''
    p[0] = p[1]


def p_Modifier(p):
    '''Modifier : PK
                | FK
                | empty'''
    p[0] = p[1]


def p_empty(p):
    'empty : '
    pass


def p_empty_list(p):
    'empty_list : '
    p[0] = []


def p_error(p):
    logger.error(f'Syntax error {p.value} in input at line: {p.lineno}')


parser = yacc.yacc(debug=True)