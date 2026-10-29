from tokentable import Token, report_error, advance_pos
OPERATORS = {
    "==": "LOGOP",
    "!=": "LOGOP",
    "<=": "LOGOP",
    ">=": "LOGOP",
    "&&": "LOGOP",
    "||": "LOGOP",
    "<": "LOGOP",
    ">": "LOGOP",
    "!": "LOGOP",
    "=": "ASSIGN",
    "+": "MATHOP",
    "-": "MATHOP",
    "*": "MATHOP",
    "/": "MATHOP",
    "%": "MATHOP",
    "+=": "ADDASSIGN",
    "-=": "SUBASSIGN",
    "*=": "MULASSIGN",
    "/=": "DIVASSIGN",
    "%=": "MODASSIGN",
    "++": "INC",
    "--": "DEC",
}
DELIMITERS = {
    "(": "LPAR",
    ")": "RPAR",
    "{": "LCUR",
    "}": "RCUR",
    "[": "LSQU",
    "]": "RSQU",
    ";": "SEMICOLON",
    ",": "COMMA",
    ".": "DOT",
}

def _scan_string(source_code, i, line, column):
    start_i = i
    start_line, start_column = line, column
    quote = source_code[i]  
    i += 1

    while i < len(source_code):
        char = source_code[i]
        if char == quote:
            i += 1
            lexeme = source_code[start_i:i]
            line, column = advance_pos(line, column, lexeme)
            return Token(lexeme, "STRING", start_line, start_column), i, line, column
        if char in "\r\n":
            report_error(start_line, start_column, "unclosed string literal starting")
            lexeme = source_code[start_i:i]
            line, column = advance_pos(line, column, lexeme)
            return None, i, line, column
        if (
            char == "\\"
            and i + 1 < len(source_code)
            and source_code[i + 1] not in "\r\n"
        ):
            i += 2
        else:
            i += 1

    report_error(start_line, start_column, "unclosed string literal starting")
    lexeme = source_code[start_i:i]
    line, column = advance_pos(line, column, lexeme)
    return None, i, line, column

def _scan_comment(source_code, i, line, column):
    start_i = i
    start_line, start_column = line, column

    if source_code.startswith("//", i):
        newline = source_code.find("\n", i + 2)
        i = len(source_code) if newline == -1 else newline
    else:
        end = source_code.find("*/", i + 2)
        if end == -1:
            report_error(start_line, start_column, "unclosed comment starting")
            i = len(source_code)
        else:
            i = end + 2

    line, column = advance_pos(line, column, source_code[start_i:i])
    return None, i, line, column

def scan_symbol(source_code, i, line, column):
    start_line, start_column = line, column

    if source_code[i] in ('"', "'"):
        return _scan_string(source_code, i, line, column)

    if source_code.startswith("//", i) or source_code.startswith("/*", i):
        return _scan_comment(source_code, i, line, column)

    for lexeme in sorted(OPERATORS, key=len, reverse=True):
        if source_code.startswith(lexeme, i):
            end = i + len(lexeme)
            line, column = advance_pos(line, column, lexeme)
            return Token(lexeme, OPERATORS[lexeme], start_line, start_column), end, line, column

    lexeme = source_code[i]
    if lexeme in DELIMITERS:
        line, column = advance_pos(line, column, lexeme)
        return Token(lexeme, DELIMITERS[lexeme], start_line, start_column), i + 1, line, column
    return None