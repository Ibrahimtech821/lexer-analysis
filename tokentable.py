from collections import namedtuple

Token=namedtuple("Token","lexeme token line column")

errors=[]

def report_error(line,column,message):
    errors.append(f"Error at line {line}, column {column}: {message}")

def advance_pos(line, column, source_code):
    for c in source_code:
        if c == "\n":
            line += 1
            column = 1
        else:
            column += 1
    return line, column
