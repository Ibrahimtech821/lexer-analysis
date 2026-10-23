from tokentable import Token, report_error
from tokentable import errors
def advance_pos(line, column, char):
    if char == '\n':
        return line + 1, 1
    else:
        return line, column + 1

def scan(source_code):
    tokens = []
    i,line,column = 0,1,1
    while i < len(source_code):
        c=source_code[i]
        if c in " \n\t\r":
            line,column=advance_pos(line,column,c)
            i+=1
        # Member 2 will add their elif branches HERE
        # Member 3 will add their elif branches HERE
        else:
            report_error(line,column,f"Unexpected character: {c}")
            line,column=advance_pos(line,column,c)
            i+=1
    return tokens
if __name__=="__main__":
    scan("\n abc")
    print("Errors:", errors)
