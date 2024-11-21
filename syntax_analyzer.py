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
def wazzup_syntax_check(i):
    matching_buhbye = False

    if "BUHBYE" in [x[1] for x in tokens]:
        matching_buhbye = True
    
    if matching_buhbye:
        return 1
def obtw_syntax_check(i):
    matching_tldr = False

    for j in range(i, len(tokens)):
        if re.match(r"TLDR", tokens[j][1]):
            matching_tldr = True
    
    if matching_tldr:
        return 1

def analyze_syntax(tokens):
    in_obtw = False
    for i in range(0, len(tokens)):
        # print(tokens[i])
        if(re.match(r"HAI", tokens[i][1])):
            if not hai_syntax_check(i):
                print("syntax error in line " + str(i + 1) + ": HAI")
        elif(re.match(r"WAZZUP", tokens[i][1])):
            if not wazzup_syntax_check(i):
                print("syntax error in line " + str(i + 1) + ": WAZZUP")
        elif(re.match(r"(\n)+", tokens[i][1])):
            # print("newline wtf")
            continue
        elif(re.match(r"BTW.*", tokens[i][1])):
            continue
        elif(re.match(r"OBTW.*", tokens[i][1])):
            if not in_obtw:
                in_obtw = True
                if not obtw_syntax_check(i):
                    print("syntax error in line " + str(i + 1) + ": OBTW")
        elif in_obtw:
            if(re.match(r"BTW"))
        else:
            continue
            # print("idk what this is")

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