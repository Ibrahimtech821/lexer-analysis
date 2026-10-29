import sys
from scanner import scan
from tokentable import errors


def get_type(t):
    return getattr(t, "type", getattr(t, "token", ""))


def get_col(t):
    return getattr(t, "col", getattr(t, "column", ""))


def print_results(tokens):
    for t in tokens:
        print(f"Lexeme: {t.lexeme}, Token: {get_type(t)}")

    print("\nSymbol Table")
    seen = set()
    for t in tokens:
        if get_type(t) == "IDENTIFIER" and t.lexeme not in seen:
            seen.add(t.lexeme)
            print(f"{t.lexeme} | IDENTIFIER | line {t.line}, col {get_col(t)}")

    print("\nErrors")
    for e in errors:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py tests/t1_valid.txt")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        src = f.read()
    print_results(scan(src))