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

TYPE_TOKENS = {"INT", "FLOAT", "BOOLEAN_TYPE", "CHAR", "STRING_TYPE", "CLASS", "VOID"}

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

    return Token(lexeme, token_type, line, start_col), i, line, column

def update_symbol_table(tokens):
    """Populates symbol_table with dicts: {lexeme, type, value, pos}."""
    symbol_table.clear()
    seen = {}

    for idx, t in enumerate(tokens):
        if t.token != "IDENTIFIER":
            continue

        # 1. In Java, the variable type comes from the type keyword before the identifier (e.g. int x = 20;)
        declared_type = None
        if idx > 0 and tokens[idx - 1].token in TYPE_TOKENS:
            declared_type = tokens[idx - 1].lexeme

        # 2. Check if a literal value is assigned via '=' (e.g. int x = 20;) or directly (e.g. int age 20)
        value = None
        if idx + 2 < len(tokens) and tokens[idx + 1].token == "ASSIGN":
            if tokens[idx + 2].token in ("NUMBER", "STRING", "BOOLEAN"):
                value = tokens[idx + 2].lexeme
        elif idx + 1 < len(tokens) and tokens[idx + 1].token in ("NUMBER", "STRING", "BOOLEAN"):
            value = tokens[idx + 1].lexeme

        if t.lexeme not in seen:
            entry = {
                "lexeme": t.lexeme,
                "type": declared_type if declared_type else "-",
                "value": value if value is not None else "-",
                "pos": f"{t.line}, {t.column}",
            }
            seen[t.lexeme] = entry
            symbol_table.append(entry)
        else:
            # If the variable was already declared earlier (e.g. int x; x = 20;), update its value
            entry = seen[t.lexeme]
            if entry["type"] == "-" and declared_type:
                entry["type"] = declared_type
            if value is not None:
                entry["value"] = value

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
