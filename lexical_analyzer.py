import re

# LOLCODE keywords and patterns
KEYWORDS = {
    "HAI",       # Start of program
    "KTHXBYE",   # End of program
    "WAZZUP",
    "BUHBYE",
    "I HAS A",   # Variable declaration
    "ITZ",       # Variable assignment
    "VISIBLE",   # Output command
    "GIMMEH",    # Input command
    "OBTW",
    "TLDR",
    "R",
    "SUM OF",
    "DIFF OF",
    "PRODUKT OF",
    "QUOSHUNT OF",
    "MOD OF",
    "BIGGR OF",
    "SMALLR OF",
    "BOTH OF",
    "EITHER OF",
    "WON OF",
    "NOT",
    "ANY OF",
    "ALL OF",
    "BOTH SAEM",
    "DIFFRINT",
    "SMOOSH",
    "MAEK",
    "A",
    "AN",
    "IS NOW A",
    "O RLY?",   # If statement
    "YA RLY",   # If true
    "MEBBE",
    "NO WAI",   # If false
    "OIC",      # End if
    "WTF?",
    "OMG",
    "OMGWTF",
    "IM IN YR",
    "UPPIN",
    "NERFIN",
    "YR",
    "TIL",
    "WILE",
    "IM OUTTA YR",
    "HOW IZ I",
    "IF U SAY SO",
    "GTFO",
    "FOUND YR",
    "I IZ",
    "MKAY"
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
        for match in re.finditer(TOKEN_REGEX, code, re.IGNORECASE):
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
    print(token)
    if token[0] == 'NEWLINE':
        print()
