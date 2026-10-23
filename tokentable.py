from collections import namedtuple

Token=namedtuple("Token","lexeme token")

errors=[]

def report_error(line,column,message):
    errors.append(f"Error at line {line}, column {column}: {message}")