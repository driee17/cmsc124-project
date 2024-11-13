import re

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
    "ITZ": "Variable Iniitalization",
    "R": "Variable Assignment",
    "SUM OF": "Addition Operation",
    "DIFF OF": "Subtraction Operation",
    "PRODUKT OF": "Multiplication Operation",
    "QUOSHUNT OF": "Divistion Operation",
    "MOD OF": "Modulo Operation",
    "BIGGR OF": "Max Operation",
    "SMALLR OF": "Min Operation",
    "BOTH OF": "Boolen AND",
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
    'STRING': r'"[^"]*"',
    'VARIABLE': r'\b[A-Za-z_]\w*\b',
    'NEWLINE': r'\n+',
    'WHITESPACE': r'[ \t]+'
}

# Combine token types into a single regex pattern
TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES.items())

class LOLCodeLexer:
    def __init__(self, file_path):
        self.file_path = file_path

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
            if token_type == "STRING":
                value = value[1:-1] # remove surrounding quotations
            tokens.append((token_type, value))  # appends the found value and token type in the tokens list
        return tokens

    def analyze_file(self):
        # Analyze the LOLCODE file.
        code = self.read_code()
        tokens = self.tokenize(code)
        return tokens

# Specify the path to the LOLCODE file
file_path = 'project-testcases/01_variables.lol'

# Run the lexer on the specified file
lexer = LOLCodeLexer(file_path)
tokens = lexer.analyze_file()

# Display tokens
for token in tokens:
    if token[0] == 'KEYWORD':
        print(token, KEYWORDS[token[1]])
    elif token[0] == 'NEWLINE':
        print(token, "\n")
    else:
        print(token)
