# Java Lexical Analyzer (Scanner)

A lexical analyzer (scanner) for a small subset of Java, written in Python.
It reads source code and produces:

- **Token Table**: every lexeme with its token type and position (line, column)
- **Symbol Table**: every identifier with its type, value and position
- **Lexical Errors**: invalid characters, invalid identifiers, unclosed strings/comments

It includes a command-line runner and a web UI built with Gradio.

## Project Structure

| File | Purpose |
| :--- | :--- |
| `tokentable.py` | `Token` definition, shared `errors` list, `report_error()` and `advance_pos()` |
| `words.py` | Keywords, identifiers, numbers and the symbol table |
| `symbols.py` | Operators, delimiters, strings and comments |
| `scanner.py` | Main `scan()` loop that combines everything |
| `main.py` | Command-line runner (prints results in the terminal) |
| `app.py` | Gradio web UI |
| `test_runner.py` | Simple runner used to compare output with `tests/expected_t1.txt` |
| `tests/` | Sample input files (`t1_valid.txt`, `t2_char.txt`, ...) |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Web UI (Gradio)

```bash
python app.py
```

Open the local link shown in the terminal (usually http://127.0.0.1:7860). You can:

- write or paste code in the editor,
- click one of the test file examples,
- or upload a `.txt` / code file.

The Token Table, Symbol Table and Lexical Errors appear on the same page.

### Command line

Run all test files:

```bash
python main.py
```

Run a specific file:

```bash
python main.py tests/t1_valid.txt
```

## Token Types

| Category | Tokens |
| :--- | :--- |
| Keywords | `CLASS`, `PUBLIC`, `PRIVATE`, `STATIC`, `VOID`, `MAIN`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BOOLEAN_TYPE`, `CHAR`, `STRING_TYPE`, `IF`, `ELSE`, `WHILE`, `FOR`, `BREAK`, `CONTINUE`, `RETURN`, `NEW`, `NULL` |
| Literals | `NUMBER`, `STRING`, `BOOLEAN` (`true` / `false`) |
| Identifier | `IDENTIFIER` |
| Logical operators | `LOGOP` (`== != <= >= && \|\| < > !`) |
| Math operators | `MATHOP` (`+ - * / %`) |
| Assignment | `ASSIGN` (`=`), `ADDASSIGN`, `SUBASSIGN`, `MULASSIGN`, `DIVASSIGN`, `MODASSIGN` |
| Increment / decrement | `INC` (`++`), `DEC` (`--`) |
| Delimiters | `LPAR`, `RPAR`, `LCUR`, `RCUR`, `LSQU`, `RSQU`, `SEMICOLON`, `COMMA`, `DOT` |

Comments (`//` and `/* ... */`) are skipped.

## Example

Input:

```java
int age = 20;
String s = "Hi"; // done
1x = 5 @ 2;
```

Token Table (first rows):

| Lexeme | Token | Line | Column |
| :--- | :--- | :--- | :--- |
| `int` | `INT` | 1 | 1 |
| `age` | `IDENTIFIER` | 1 | 5 |
| `=` | `ASSIGN` | 1 | 9 |
| `20` | `NUMBER` | 1 | 11 |
| `;` | `SEMICOLON` | 1 | 13 |

Symbol Table:

| Lexeme | Type | Value | Line, Col |
| :--- | :--- | :--- | :--- |
| `age` | `int` | `20` | 1, 5 |
| `s` | `String` | `"Hi"` | 2, 8 |

Errors:

```
Error at line 3, column 1: invalid identifier '1x'
Error at line 3, column 8: invalid character '@'
```

## Lexical Errors Detected

- Invalid character (for example `@`, `#`)
- Invalid identifier (for example `1name`)
- Unclosed string literal
- Unclosed comment

## Team

Built as a team project for a Compiler course.

