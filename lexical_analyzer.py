import re

# LOLCODE keywords and patterns
KEYWORDS = {
    "HAI": "Start Variable",       # Start of program
    "KTHXBYE": "Keyword",   # End of program
    "WAZZUP": "Keyword",
    "BUHBYE": "Keyword",
    "I HAS A": "Keyword",   # Variable declaration
    "ITZ": "Keyword",       # Variable assignment
    "VISIBLE": "Keyword",   # Output command
    "GIMMEH": "Keyword",    # Input command
    "OBTW": "Keyword",
    "TLDR": "Keyword",
    "R": "Keyword",
    "SUM OF": "Keyword",
    "DIFF OF": "Keyword",
    "PRODUKT OF": "Keyword",
    "QUOSHUNT OF": "Keyword",
    "MOD OF": "Keyword",
    "BIGGR OF": "Keyword",
    "SMALLR OF": "Keyword",
    "BOTH OF": "Keyword",
    "EITHER OF": "Keyword",
    "WON OF": "Keyword",
    "NOT": "Keyword",
    "ANY OF": "Keyword",
    "ALL OF": "Keyword",
    "BOTH SAEM": "Keyword",
    "DIFFRINT": "Keyword",
    "SMOOSH": "Keyword",
    "MAEK": "Keyword",
    "A": "Keyword",
    "AN": "Keyword",
    "IS NOW A": "Keyword",
    "O RLY?": "Keyword",   # If statement
    "YA RLY": "Keyword",   # If true
    "MEBBE": "Keyword",
    "NO WAI": "Keyword",   # If false
    "OIC": "Keyword",      # End if
    "WTF?": "Keyword",
    "OMG": "Keyword",
    "OMGWTF": "Keyword",
    "IM IN YR": "Keyword",
    "UPPIN": "Keyword",
    "NERFIN": "Keyword",
    "YR": "Keyword",
    "TIL": "Keyword",
    "WILE": "Keyword",
    "IM OUTTA YR": "Keyword",
    "HOW IZ I": "Keyword",
    "IF U SAY SO": "Keyword",
    "GTFO": "Keyword",
    "FOUND YR": "Keyword",
    "I IZ": "Keyword",
    "MKAY": "Keyword"
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
print(TOKEN_REGEX)

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
            tokens.append((token_type, value))
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
        print(token, end='')
        print(" " + KEYWORDS[token[1]])
    elif token[0] == 'NEWLINE':
        print(token)
        print()
    else:
        print(token)
