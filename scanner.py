from tokentable import Token, report_error
from tokentable import errors
from words import scan_word, scan_number, symbol_table

def advance_pos(source_code,line, column):
    for c in source_code:
        if c == '\n':
            line += 1
            column = 1
        else:
            column += 1
    return line, column

def scan(source_code):
    tokens = []
    i,line,column = 0,1,1
    while i < len(source_code):
        c=source_code[i]
        if c in " \n\t\r":
            line,column=advance_pos(c,line,column)
            i+=1
        elif c.isalpha() or c == '_':
            token, i, line, column = scan_word(source_code, i, line, column)
            tokens.append(token)
        elif c.isdigit():
            token, i, line, column = scan_number(source_code, i, line, column)
            if token is not None:
                tokens.append(token)
        # Member 3 will add their elif branches HERE
        else:
            report_error(line,column,f"Unexpected character: {c}")
            line,column=advance_pos(c,line,column)
            i+=1
    return tokens
if __name__=="__main__":
    sample = "class Student int age 20 float grade 85.5 boolean flag true 1name"
    result = scan(sample)
    print("Tokens:", result)
    print("Symbol Table:", symbol_table)
    print("Errors:", errors)
    