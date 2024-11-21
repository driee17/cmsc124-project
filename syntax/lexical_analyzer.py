import re
import tkinter as tk
from tkinter import filedialog

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
    "MKAY": "Boolean Statement End"
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

class LOLCodeLexer:
    def __init__(self):
        self.file_path = self.open_file_dialog()

    def open_file_dialog(self):
        # Open file dialog to let the user select a LOLCODE file.
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(
            title="Select a LOLCODE file",
            filetypes=[("LOLCODE files", "*.lol"), ("All files", "*.*")]
        )
        return file_path

    def read_code(self):
        # Read code from the file.
        with open(self.file_path, 'r') as file:
            return file.read()

    def tokenize(self, code):
        # Tokenize the given code.
        tokens = []
        for match in re.finditer(TOKEN_REGEX, code, flags=0):
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

    def analyze_file(self):
        # Analyze the LOLCODE file.
        code = self.read_code()
        tokens = self.tokenize(code)
        return tokens


# # Run the lexer and open the file explorer for file selection
# lexer = LOLCodeLexer()
# tokens = lexer.analyze_file()

# # Print header for the table
# print(f"{'TYPE':<20} {'LEXEMES':<25} {'CLASSIFICATION':<30}")
# print("=" * 90)

# # Display tokens in three columns: TYPE, LEXEMES, CLASSIFICATION
# for token in tokens:
#     token_type = token[0]
#     lexeme = token[1]
    
#     if token_type == 'NEWLINE':
#         lexeme = '\\n'
#         classification = 'Newline\n'
#     else:
#         # Classification is either from KEYWORDS or based on the token type
#         if token_type == 'KEYWORD':
#             classification = KEYWORDS.get(lexeme, "Unknown")
#         else:
#             classification = {
#                 'COMMENT': 'Comment',
#                 'NUMBAR': 'Literal (Float)',
#                 'NUMBR': 'Literal (Integer)',
#                 'CONCATENATE': 'Concatenate Keyword',
#                 'TROOF': "Boolean Literal",
#                 'YARN': 'String',
#                 'STRING_DELIMITER': 'String Delimiter',
#                 'VARIABLE': 'Variable'
#             }.get(token_type, "Unknown")
    
#     # Print each token in a formatted table row

#     print(f"{token_type:<20} {lexeme:<25} {classification:<30}")