# ========== WRONG CODE, KEEPING FOR FUTURE REFERENCE


import re
import lexical_analyzer


def hai_syntax_check(i):
    preceded_by_comments = True
    matching_kthxbye = False

    if "KTHXBYE" in [x[1] for x in tokens]:
        matching_kthxbye = True

    if i == 0 and matching_kthxbye:
        print("HAI at start")
        return 1
    
    if 1 != 0:
        in_obtw = False
        for j in range(0, i):
            if(re.match(r"BTW.*", tokens[j][1])):
                continue
            elif(re.match(r"(\n)+", tokens[j][1])):
                continue
            elif(re.match(r"OBTW.*", tokens[j][1])):
                in_obtw = True
                continue
            elif in_obtw:
                if(re.match(r"TLDR", tokens[j][1])):
                    in_obtw = False
                    continue
                else:
                    continue
            else:
                print(tokens[j][1] + " fucked it over")
                preceded_by_comments = False
    
    if preceded_by_comments and matching_kthxbye:
        print("HAI preceded only by comments")
        return 1

def recursive_parser(tokens):
    classification, lexeme = next(tokens)
    if classification != "NEWLINE":
        print("parse error")
        return -1
        

def analyze_syntax(tokens):
    # parseTree = ["<program>"]
    # i, j = 0

    # # for i in range(0, len(tokens)):
    # while True:
    #     curr = parseTree[i]
    #     if "<program>" in curr:
    #         if tokens[j][1] == "HAI":
    #             if hai_syntax_check(j):
    #                 parseTree[i] = []
    #                 parseTree[i].append(tokens[j][0])
    #                 parseTree[i].append("<newline>")
    #                 parseTree[i].append("<statement>")
    #                 parseTree[i].append("<newline>")
    #                 parseTree[i].append("<KTHXBYE>")
    #                 # i += 1
    #                 j += 1
    #     if "<newline>" in curr:
    #         if tokens[j][0] == "NEWLINE":

    classification, lexeme = next(tokens)
    while classification == "COMMENT":
        classification, lexeme = next(tokens)
    if classification == "KEYWORD" and lexeme == "HAI":
        return recursive_parser(tokens)
        




# Run the lexer and open the file explorer for file selection
lexer = lexical_analyzer.LOLCodeLexer()
tokens = lexer.analyze_file()
# print(tokens)
analyze_syntax(tokens)


# ========================================================================================= FOR DISPLAYING LEXEMES
# Print header for the table
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
#             classification = lexical_analyzer.KEYWORDS.get(lexeme, "Unknown")
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
# ===========================================================================================