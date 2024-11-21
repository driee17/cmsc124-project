import re
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk

# LOLCODE keywords and patterns
KEYWORDS = {
    "HAI": "Code Delimiter",
    "KTHXBYE": "Code Delimiter",
    "WAZZUP": "Variable Declaration Clause Delimiter",
    "BUHBYE": "Variable Declaration Clause Delimiter",
    "BTW": "Comment",
    "OBTW": "Comment Delimiter",
    "TLDR": "Comment Delimiter",
    "I HAS A": "Variable Declaration",
    "ITZ": "Variable Initialization",
    "R": "Variable Assignment",
    "SUM OF": "Addition Operation",
    "DIFF OF": "Subtraction Operation",
    "PRODUKT OF": "Multiplication Operation",
    "QUOSHUNT OF": "Division Operation",
    "MOD OF": "Modulo Operation",
    "BIGGR OF": "Max Operation",
    "SMALLR OF": "Min Operation",
    "BOTH OF": "Boolean AND",
    "EITHER OF": "Boolean OR",
    "WON OF": "Boolean XOR",
    "NOT": "Boolean NOT",
    "ANY OF": "Boolean OR (Infinite Arity)",
    "ALL OF": "Boolean AND (Infinite Arity)",
    "BOTH SAEM": "Comparison Operation ==",
    "DIFFRINT": "Comparison Operation !=",
    "SMOOSH": "String Concatenation",
    "MAEK": "Explicit Typecast",
    "A": "Partial Keyword",
    "AN": "Partial Keyword",
    "IS NOW A": "Explicit Typecast",
    "VISIBLE": "Output Keyword", 
    "GIMMEH": "Input Keyword",
    "O RLY?": "If Block Start",
    "YA RLY": "Condition Met Code Block Delimiter",
    "^MEBBE": "Else If Code Block Delimiter", # not required to implement
    "NO WAI": "Condition Not Met Code Block Delimiter",
    "OIC": "If/Switch Block End",
    "WTF?": "Switch Block Start",
    "OMG": "Case Keyword",
    "OMGWTF": "Default Case Keyword",
    "IM IN YR": "Loop Delimiter",
    "UPPIN": "Increment Operation",
    "NERFIN": "Decrement Operation",
    "YR": "Partial Keyword",
    "TIL": "Repeat Loop Until Condition Met",
    "WILE": "Repeat Loop While Condition Met",
    "IM OUTTA YR": "Loop Delimiter",
    "HOW IZ I": "Function Delimiter",
    "IF U SAY SO": "Function Delimiter",
    "GTFO": "Break Keyword",
    "FOUND YR": "Return Keyword",
    "I IZ": "Function Call Keyword",
    "MKAY": "Boolean Statement End",
}

TOKEN_TYPES = {
    'COMMENT': r'BTW.*',
    'KEYWORD': r'\b(?:' + '|'.join(re.escape(keyword) for keyword in KEYWORDS) + r')\b',
    'NUMBAR':r'\b-?\d+\.\d+\b',
    'NUMBR': r'\b-?\d+\b',
    'CONCATENATE': r'\+', 
    'TROOF': r'WIN|FAIL',
    'YARN': r'"[^"]*"',
    'TYPE': r'(NUMBAR|NUMBR|TROOF|YARN|NOOB)',
    'VARIABLE': r'\b[A-Za-z_]\w*\b',
    'NEWLINE': r'\n+',
    'WHITESPACE': r'[ \t]+'
}

# Combine token types into a single regex pattern
TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())

class LOLCodeGUI:
    # color guides:
    # https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html 
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCODE Interpreter")

        # Set the root background color
        self.root.configure(bg="ivory2")

        # Create a 3-column grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        # HEADER
        header = tk.Label(root, text="LOLCODE INTERPRETER", bg="steel blue", fg="ivory2", font=("Helvetica", 14, "bold"))
        header.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # COLUMN 1: File Explorer and Text Editor
        self.file_explorer_frame = tk.Frame(root, bd=1, relief="solid", bg="ivory2")
        self.file_explorer_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.file_label = tk.Label(self.file_explorer_frame, text="Select a file", bg="ivory2", anchor="w", font=("Helvetica", 10, "bold"))
        self.file_label.pack(fill="x", padx=5, pady=5)

        self.browse_button = tk.Button(self.file_explorer_frame, text="📂", bg="steel blue", fg="ivory2", font=("Helvetica", 12, "bold"), command=self.open_file)
        self.browse_button.pack(fill="x", padx=5, pady=5)

        self.text_editor = scrolledtext.ScrolledText(self.file_explorer_frame, wrap="word", bg="ivory2", height=25, width=80)
        self.text_editor.pack(fill="both", expand=True, padx=5, pady=5)

        # COLUMN 2: List of Tokens
        self.tokens_frame = tk.Frame(root, bd=1, bg="ivory2", relief="solid")
        self.tokens_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.lexemes_header = tk.Label(self.tokens_frame, text="LEXEMES", bg="steel blue", fg="ivory2", font=("Helvetica", 12, "bold"))
        self.lexemes_header.pack(fill="x", padx=5, pady=5)

        # Create a frame to contain both the Treeview and scrollbar
        tokens_tree_container = tk.Frame(self.tokens_frame, bg="ivory2")
        tokens_tree_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview for the lexemes section
        self.tokens_tree = ttk.Treeview(tokens_tree_container, columns=("Type", "Lexeme", "Classification"), show="headings", height=20)
        self.tokens_tree.heading("Type", text="TYPE")
        self.tokens_tree.heading("Lexeme", text="LEXEMES")
        self.tokens_tree.heading("Classification", text="CLASSIFICATION")

        self.tokens_tree.column("Type", width=150, anchor="w")
        self.tokens_tree.column("Lexeme", width=250, anchor="w")
        self.tokens_tree.column("Classification", width=250, anchor="w")

        self.tokens_tree.pack(side="left", fill="both", expand=True)

        # Add vertical scrollbar to the Treeview
        tokens_scrollbar = ttk.Scrollbar(tokens_tree_container, orient="vertical", command=self.tokens_tree.yview)
        tokens_scrollbar.pack(side="right", fill="y")

        # Configure Treeview to use the scrollbar
        self.tokens_tree.configure(yscrollcommand=tokens_scrollbar.set)

        # COLUMN 3: Symbol Table
        self.symbol_table_frame = tk.Frame(root, bd=1, bg="ivory2", relief="solid")
        self.symbol_table_frame.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        self.symbol_table_header = tk.Label(self.symbol_table_frame, text="SYMBOL TABLE", bg="steel blue", fg="ivory2", font=("Helvetica", 12, "bold"))
        self.symbol_table_header.pack(fill="x", padx=5, pady=5)

        # Create a frame to contain both the Treeview and scrollbar
        symbol_table_container = tk.Frame(self.symbol_table_frame, bg="ivory2")
        symbol_table_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview for the symbol table
        self.symbol_table = ttk.Treeview(symbol_table_container, columns=("Identifier", "Value"), show="headings")
        self.symbol_table.heading("Identifier", text="IDENTIFIER")
        self.symbol_table.heading("Value", text="VALUE")

        self.symbol_table.column("Identifier", width=200, anchor="w")
        self.symbol_table.column("Value", width=200, anchor="w")

        self.symbol_table.pack(side="left", fill="both", expand=True)

        # Add vertical scrollbar to the symbol table
        symbol_table_scrollbar = ttk.Scrollbar(symbol_table_container, orient="vertical", command=self.symbol_table.yview)
        symbol_table_scrollbar.pack(side="right", fill="y")

        # Configure Treeview to use the scrollbar
        self.symbol_table.configure(yscrollcommand=symbol_table_scrollbar.set)

        # EXECUTE Button
        self.execute_button = tk.Button(root, text="EXECUTE", command=self.execute_code, font=("Helvetica", 12, "bold"), bg="steel blue", fg="ivory2")
        self.execute_button.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # CONSOLE
        self.console = tk.Label(root, bg="ivory2", anchor="nw", relief="solid", height=15)
        self.console.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

    def open_file(self):
        # Open file dialog to let the user select a LOLCODE file.  
        file_path = filedialog.askopenfilename(
            title="Select a LOLCODE file",
            filetypes=[("LOLCODE files", "*.lol"), ("All files", "*.*")]
        )
        if file_path:
            self.file_label.config(text=file_path)
            with open(file_path, 'r') as file:
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, file.read())

    def tokenize(self, code):
        # Tokenize the given code.
        tokens = []
        lines = code.splitlines()
        is_multiline_comment = False
        multiline_comment_content = []

        for line in lines:
            line = line.strip()
            if is_multiline_comment:
                if line.startswith("TLDR"):
                    # End of multi-line comment
                    # Join the comment lines with a \n and add "OBTW" at the start and "TLDR" at the end
                    full_comment = "OBTW \\n " + " \\n ".join(multiline_comment_content) + " \\n TLDR"
                    tokens.append(("MULTI-LINE_COMMENT", full_comment))
                    is_multiline_comment = False
                    multiline_comment_content = []
                else:
                    # Append the content of the line to the multi-line comment (without leading whitespace)
                    multiline_comment_content.append(line)
                continue

            if line.startswith("OBTW"):
                # Start of multi-line comment
                is_multiline_comment = True
                continue

            # Tokenize normally for non-comment lines
            for match in re.finditer(TOKEN_REGEX, line, flags=0):
                token_type = match.lastgroup
                value = match.group(token_type)
                if token_type == "WHITESPACE":
                    continue
                if token_type == "YARN":
                    tokens.append(("STRING_DELIMITER", '"'))
                    value = value[1:-1]
                    tokens.append((token_type, value))
                    tokens.append(("STRING_DELIMITER", '"'))
                    continue
                tokens.append((token_type, value))  # Appends the found value and token type in the tokens list

        return tokens

    def execute_code(self):
        # Retrieve LOLCODE from the text editor
        code = self.text_editor.get(1.0, tk.END).strip()

        # Clear previous data
        self.tokens_tree.delete(*self.tokens_tree.get_children())  # Clear tokens treeview
        for row in self.symbol_table.get_children():
            self.symbol_table.delete(row)

        # Tokenize the code
        tokens = self.tokenize(code)
        # symbol_table = {}

        for token in tokens:
            token_type = token[0]
            lexeme = token[1]

            # Classification logic
            if token_type == 'NEWLINE':
                lexeme = '\\n'
                classification = 'Newline\n'
            else:
                # Classification is either from KEYWORDS or based on the token type
                if token_type == 'KEYWORD':
                    classification = KEYWORDS.get(lexeme, "Unknown")
                else:
                    classification = {
                        'COMMENT': 'Comment',
                        'MULTI-LINE_COMMENT': 'Multi-line Comment',
                        'NUMBAR': 'Literal (Float)',
                        'NUMBR': 'Literal (Integer)',
                        'CONCATENATE': 'Concatenate Keyword',
                        'TROOF': "Boolean Literal",
                        'YARN': 'String',
                        'STRING_DELIMITER': 'String Delimiter',
                        'VARIABLE': 'Variable',
                        'TYPE': 'Variable Type'
                    }.get(token_type, "Unknown")

            # Display token in the Treeview
            self.tokens_tree.insert("", "end", values=(token_type, lexeme, classification))

            '''
            # Add variables to the symbol table
            if token_type == "VARIABLE":
                if lexeme not in symbol_table:
                    symbol_table[lexeme] = " "

        # Update the symbol table in the UI
        for identifier, value in symbol_table.items():
            self.symbol_table.insert("", "end", values=(identifier, value))
        '''

# Create the main application window
root = tk.Tk()
app = LOLCodeGUI(root)
root.mainloop()