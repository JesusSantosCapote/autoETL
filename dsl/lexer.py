from ply.lex import lex
from global_config import LOG_FILE_PATH
from logger import logger

reserved = {
    'dimension' : 'DIM',
    'fact' : 'FACT',
    'sum' : 'SUM',
    'avg' : 'AVG',
    'count': 'COUNT',
    'max': 'MAX',
    'min': 'MIN',
    'groupby' : 'GROUP',
    'self' : 'SELF',
    'as' : 'AS',
    'week_day' : 'WEEKDAY',
    'month_str': 'MONTHSTR',
    'PK'       : 'PK',
    'FK' : 'FK',
    'int' : 'INT',
    'str': 'STR',
    'date': 'DATE',
    'datetime': 'DATETIME',
    'serial': 'SERIAL',
    'to': 'TO'
}

tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'LBRACE',
   'RBRACE',
   'TWODOTS',
   'DOT',
   'ID'
] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'{'
t_RBRACE  = r'}'
t_TWODOTS = r':'
t_DOT = r'.'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9ÁÉÍÓÚáéíóú]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    logger.error("Illegal character '%s' at line" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex(debug=True)