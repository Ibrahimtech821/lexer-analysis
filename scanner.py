from tokentable import Token, report_error, advance_pos,errors
from words import scan_word, scan_number, symbol_table, update_symbol_table
from symbols import scan_symbol


def scan(source_code):
    tokens = []
    i,line,column = 0,1,1
    while i < len(source_code):
        c=source_code[i]
        if c in " \n\t\r":
            line,column=advance_pos(line,column,c)
            i+=1
        elif c.isalpha() or c == '_':
            token, i, line, column = scan_word(source_code, i, line, column)
            tokens.append(token)
        elif c.isdigit():
            token, i, line, column = scan_number(source_code, i, line, column)
            if token is not None:
                tokens.append(token)
        else:
            result = scan_symbol(source_code, i, line, column)
            if result is None:
                report_error(line, column, f"invalid character '{c}'")
                line,column=advance_pos(line,column,c)
                i+=1
            else:
                token, i, line, column = result
                if token is not None:
                    tokens.append(token)
    update_symbol_table(tokens)
    return tokens
def print_results_table(tokens, errors):
    print("=" * 65)
    print(f"{'LEXICAL ANALYSIS RESULTS':^65}")
    print("=" * 65)
    print(f"{'Lexeme':<25} | {'Token ':<20} | {'Line, Col':<12}")
    print("-" * 65)
    
    for t in tokens:
        lexeme = getattr(t, 'lexeme', str(t))
        token_type = getattr(t, 'type', getattr(t, 'token', ''))
        line = getattr(t, 'line', '')
        col = getattr(t, 'col', getattr(t, 'column', ''))
        pos = f"{line}, {col}" if line else ""
        
        print(f"{lexeme:<25} | {token_type:<20} | {pos:<12}")
    
    print("=" * 65)
    if errors:
        print("\nERRORS FOUND:")
        for err in errors:
            print(f"• {err}")
        print("=" * 65)

if __name__=="__main__":
    sample = "class Student int age 20 float grade 85.5 boolean flag true 1name"
    result = scan(sample)
    print_results_table(result, errors)
    
