from ply import yacc
from dsl.ast_nodes import *
from dsl.lexer import tokens

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
        p[0] == Fact(p[2], p[4])


def p_List_Attr_Def(p):
    '''List_Attr_Def : List_Attr_Def Attr_Def'''
    p[0] = p[1]
    p[0].append(p[2])


def p_Attr_Def(p):
    '''Attr_Def : Simple_Attr
                | Compound_Attr'''
    p[0] = p[1]


def p_Simple_Attr(p):
    '''Simple_Attr : Attr Alias'''
    p[1].alias = p[2]
    p[0] = p[1]


def p_Compound_Attr(p):
    '''Compound_Attr : Arithmetic_Attr Alias'''
    p[1].alias = p[2]
    p[0] = p[1]


def p_Arithmetic_Attr(p):
    '''Arithmetic_Attr : T X'''
    p[0] = ArithmeticAttribute(p[1][0]+p[2][0], p[1][1] + p[2][1])
    p[1] + p[2]


def p_X(p):
    '''X : PLUS T X
         | MINUS T X
         | empty'''
    if p[1] == '+':
       p[0] = (p[2][0] + p[3][0], '+' + p[2][1] + p[3][1])

    if p[1] == '-':
       p[0] = (p[2][0] + p[3][0], '-' + p[2][1] + p[3][1])

   
def p_T(p):
    '''T : F Y'''
    p[0] = (p[1][0] + p[2][0], p[1][1] + p[2][1])   


def p_Y(p):
    '''Y : TIMES F Y
         | DIVIDE F Y
         | empty'''
    if p[1] == '*':
       p[0] = (p[2][0] + p[3][0], '*' + p[2][1] + p[3][1])   

    if p[1] == '/':
       p[0] = (p[2][0] + p[3][0], '/' + p[2][1] + p[3][1])       


def p_F(p):
    '''F : Simple_Attr
         | NUMBER
         | LPAREN Arithmetic_Attr RPAREN'''
    if len(p) == 2:
        if type(p[1].value) == int:
            p[0] = ([], str(p[1]))

        else:        
            p[0] = ([p[1]], f'{p[1].name}')

    if len(p) == 4:
        p[0] =  (p[2][0], '(' + p[2][1] + ')') 
    

# def p_F_Number(p):
#     '''F : NUMBER'''
#     p[0] = ([], str(p[1]))


def p_Attr(p):
    '''Attr : Table TWODOTS ID
            | Table TWODOTS Func LPAREN ID RPAREN
            | Table TWODOTS SUM LPAREN ID RPAREN GROUP Table TWODOTS ID
            | Table TWODOTS AVG LPAREN ID RPAREN GROUP Table TWODOTS ID
            | Table TWODOTS COUNT LPAREN ID RPAREN GROUP Table TWODOTS ID'''
            
    if len(p) == 4:
        p[0] = Attribute(p[1], p[3])

    if len(p) == 7:
        p[0] = AttributeFunction(p[1], p[5], p[3])

    if len(p) == 9:
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


def p_empty(p):
    'empty : '
    pass

parser = yacc.yacc(debug=True)