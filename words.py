from tokentable import Token, report_error

KEYWORDS = {
    "class": "CLASS",
    "public": "PUBLIC",
    "static": "STATIC",
    "void": "VOID",
    "main": "MAIN",
    "int": "INT",
    "float": "FLOAT",
    "boolean": "BOOLEAN_TYPE",
    "char": "CHAR",
    "String": "STRING_TYPE",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "return": "RETURN",
    "true": "BOOLEAN",
    "false": "BOOLEAN",
}

symbol_table = []

def scan_word(source_code, i, line, column):
    start_i = i
    start_col = column

    while i < len(source_code) and (source_code[i].isalnum() or source_code[i] == "_"):
        i += 1
        column += 1

    lexeme = source_code[start_i:i]

    if lexeme in KEYWORDS:
        token_type = KEYWORDS[lexeme]
    else:
        token_type = "IDENTIFIER"
        if lexeme not in symbol_table:
            symbol_table.append(lexeme)

    return Token(lexeme, token_type, line, start_col), i, line, column

def scan_number(source_code, i, line, column):
    start_i = i
    start_col = column

    while i < len(source_code) and source_code[i].isdigit():
        i += 1
        column += 1

    if (
        i < len(source_code)
        and source_code[i] == "."
        and i + 1 < len(source_code)
        and source_code[i + 1].isdigit()
    ):
        i += 1
        column += 1
        while i < len(source_code) and source_code[i].isdigit():
            i += 1
            column += 1

    if i < len(source_code) and (source_code[i].isalpha() or source_code[i] == "_"):
        while i < len(source_code) and (source_code[i].isalnum() or source_code[i] == "_"):
            i += 1
            column += 1
        lexeme = source_code[start_i:i]
        report_error(line, start_col, f"invalid identifier '{lexeme}'")
        return None, i, line, column

    lexeme = source_code[start_i:i]
    return Token(lexeme, "NUMBER", line, start_col), i, line, column
