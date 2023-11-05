from dsl.lexer import lexer
import os

path = os.path.join(os.getcwd(), 'input.txt')
with open(path) as file:
    data = file.read()

lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)