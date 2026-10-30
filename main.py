import sys
import os
from scanner import scan, print_results_table
from tokentable import errors
from words import symbol_table

def run_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        source_code = f.read()

    # Clear previous state before scanning a new file
    errors.clear()
    symbol_table.clear()

    print(f"\n>>> Scanning file: {filepath}")
    print(f"Source code:\n{source_code.strip()}\n")

    tokens = scan(source_code)
    print_results_table(tokens, errors)

def main():
    # If file paths are passed via command line: python main.py tests/t1_valid.txt
    if len(sys.argv) > 1:
        for filepath in sys.argv[1:]:
            run_file(filepath)
    else:
        # Default: run all test files in the tests/ folder
        test_files = [
            "tests/t1_valid.txt",
            "tests/t2_char.txt",
            "tests/t3_ident.txt",
            "tests/t4_string.txt",
            "tests/t5_comment.txt",
            "tests/t6_valid.txt",
            "tests/t6_multiline.txt",
            "tests/t7_dup.txt"
        ]
        for filepath in test_files:
            run_file(filepath)

if __name__ == "__main__":
    main()
