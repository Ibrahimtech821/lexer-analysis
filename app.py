import os
import gradio as gr
from scanner import scan
from tokentable import errors
from words import symbol_table


TEST_FILES = [
    ("t1_valid.txt", "tests/t1_valid.txt"),
    ("t2_char.txt", "tests/t2_char.txt"),
    ("t3_ident.txt", "tests/t3_ident.txt"),
    ("t4_string.txt", "tests/t4_string.txt"),
    ("t5_comment.txt", "tests/t5_comment.txt"),
    ("t6_valid.txt", "tests/t6_valid.txt"),
    ("t6_multiline.txt", "tests/t6_multiline.txt"),
    ("t7_dup.txt", "tests/t7_dup.txt")
]


def load_test_examples():
    """Loads the contents of test files in tests/ to display as clickable examples."""
    examples = []
    labels = []
    for label, path in TEST_FILES:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                examples.append([f.read().strip()])
                labels.append(label)
    return examples, labels


def load_file(file_obj):
    """Reads uploaded file content and puts it into the code editor."""
    if file_obj is None:
        return ""
    filepath = file_obj.name if hasattr(file_obj, "name") else str(file_obj)
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def analyze_code(code_text, uploaded_file=None):
    """Runs the lexical scanner on either the code editor text or uploaded file."""
    # If code_text is empty but a file is uploaded, read from the file
    if (not code_text or not code_text.strip()) and uploaded_file is not None:
        code_text = load_file(uploaded_file)

    if not code_text or not code_text.strip():
        return [], [], "Please enter some code or upload a file to analyze."

    # Clear previous run state
    errors.clear()
    symbol_table.clear()

    # Run scanner (also populates symbol_table)
    tokens = scan(code_text)

    # 1. Format Token Table rows: [Lexeme, Token, Line, Column]
    token_rows = [
        [t.lexeme, t.token, t.line, t.column]
        for t in tokens
    ]

    # 2. Format Symbol Table rows: [Lexeme, Type, Value, Line, Col]
    symbol_rows = [
        [s["lexeme"], s["type"], s["value"], s["pos"]]
        for s in symbol_table
    ]

    # 3. Format Errors text
    if errors:
        error_output = "\n".join(f"• {err}" for err in errors)
    else:
        error_output = "✅ No lexical errors found!"

    return token_rows, symbol_rows, error_output


example_data, example_labels = load_test_examples()

with gr.Blocks(title="Lexical Analyzer (Scanner)") as demo:
    gr.Markdown("# 🔍 Lexical Analyzer (Scanner)")
    gr.Markdown(
        "Write your code below, click one of the **Test File Examples**, or upload a `.txt` / code file to generate the **Token Table**, **Symbol Table**, and check for **Lexical Errors**."
    )

    with gr.Row():
        # Left Column: Inputs & Test Examples
        with gr.Column(scale=1):
            code_input = gr.Code(
                label="Write or Paste Code Here",
                language=None,
                lines=12,
            )

            if example_data:
                gr.Examples(
                    examples=example_data,
                    example_labels=example_labels,
                    inputs=[code_input],
                    outputs=[],
                    label="📂 Click a Test File from tests/ to Load & Analyze",
                )

            file_input = gr.File(
                label="Or Upload a Code / .txt File",
                file_types=[".txt", ".java", ".c", ".cpp", ".py"],
            )
            with gr.Row():
                analyze_btn = gr.Button("Analyze Code", variant="primary")
                clear_btn = gr.Button("Clear")

        # Right Column: Outputs (Token Table + Symbol Table + Errors in the same page)
        with gr.Column(scale=1):
            token_table_output = gr.Dataframe(
                headers=["Lexeme", "Token", "Line", "Column"],
                datatype=["str", "str", "number", "number"],
                label="Token Table",
                interactive=False,
            )
            symbol_table_output = gr.Dataframe(
                headers=["Lexeme", "Type", "Value", "Line, Col"],
                datatype=["str", "str", "str", "str"],
                label="Symbol Table",
                interactive=False,
            )
            errors_output = gr.Textbox(
                label="Lexical Errors",
                lines=5,
                interactive=False,
                placeholder="Errors will appear here...",
            )

    # Automatically run analysis whenever an example or file changes code_input
    code_input.change(
        fn=lambda code: analyze_code(code, None) if code and code.strip() else ([], [], ""),
        inputs=[code_input],
        outputs=[token_table_output, symbol_table_output, errors_output],
    )

    # Automatically populate the code box when a file is uploaded
    file_input.change(
        fn=load_file,
        inputs=file_input,
        outputs=code_input,
    )

    # Analyze button click
    analyze_btn.click(
        fn=analyze_code,
        inputs=[code_input, file_input],
        outputs=[token_table_output, symbol_table_output, errors_output],
    )

    # Clear button click
    clear_btn.click(
        fn=lambda: ("", None, [], [], ""),
        inputs=None,
        outputs=[code_input, file_input, token_table_output, symbol_table_output, errors_output],
    )


if __name__ == "__main__":
    demo.launch()
