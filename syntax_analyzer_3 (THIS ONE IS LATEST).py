import re
import lexical_analyzer

# all of this is based on the grammar we submitted with a few modifications
# program parse -> statement parse
# statement parse -> print parse | variable declaration parse | etc other stuff
# print parse -> VISIBLE variable/literal/expression
# variable declaration parse -> I HAS A variable [ITZ variable/literal]

# uses tokens as stack to get the next lexeme
# uses a lot of loops and recursions
# outputs a nested list file we can later turn into a tree if needed

# ===== IMPORTANT: so far, all it can check syntactically is: program, statement (either print or variable declaration), and check specifically for YARNs

def yarn_parse():               # yarn literal parse
    yarn_list = []
    classification, lexeme = tokens.pop()
    yarn_list.append(lexeme)
    classification, lexeme = tokens.pop()
    yarn_list.append(lexeme)
    classification, lexeme = tokens.pop()
    yarn_list.append(lexeme)
    return yarn_list

def var_dec_parse():                # variable declaration statement parse
    # print("parsing variable declaration")

    var_dec_list = []                                   # initialize variable declaration statement list

    classification, lexeme = tokens.pop()                       # put "I HAS A" keyword in list then pop next lexeme
    var_dec_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if classification == "VARIABLE":                    # if next lexeme is a variable then append it, otherwise bad syntax
        var_dec_list.append(lexeme)
    else:
        print("syntax error in variable declaration!")
        raise("LOLCode error")

    classification, lexeme = tokens.pop()               # pop next lexeme again
    
    if lexeme != "ITZ":                             # if not ITZ keyword (for elaborate variable declaration, push that lexeme back in stack)
        tokens.append((classification, lexeme))
    else:                                              # if ITZ keyword, put "ITZ" keyword in list
        var_dec_list.append(lexeme)
        classification, lexeme = tokens.pop()           # pop next lexeme
        if classification == "NUMBR" or classification == "NUMBAR" or classification == "TROOF" or classification == "VARIABLE":            # if literal, append that lexeme to list then return
            var_dec_list.append(lexeme)
            return var_dec_list
        elif classification == "STRING_DELIMITER":
            tokens.append((classification, lexeme))
            var_dec_list.append(yarn_parse())
            return var_dec_list
        else:                   # else, bad syntax
            print("syntax error in ITZ part of variable declaration!")
            raise("LOLCode error")
        
    return var_dec_list

def print_parse():              # print statement parse
    # print("parsing print")
    print_list = []                 # initialize list for print statement

    classification, lexeme = tokens.pop()           # add "VISIBLE" lexeme to list then pop next lexeme
    print_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR"or classification == "TROOF":             # if next lexeme is variable or literal (that isn't a YARN) just append it and return the list
        print_list.append(lexeme)
        return print_list
    elif classification == "STRING_DELIMITER":              # if string delimiter is found, we hit yarn, parse yarn then return list
        tokens.append((classification, lexeme))
        print_list.append(yarn_parse())
        return print_list
    elif lexeme == "NUMBR" or lexeme == "NUMBAR" or lexeme == "YARN" or lexeme == "TROOF":              # if lexeme is of literal type TYPE, also append it to list and return list
        print_list.append(lexeme)
        return print_list
    else:                               # otherwise, syntax error
        print("syntax error in print statement!")
        raise("LOLCode error")

def statement_parse():                  # statement parse
    # print("parsing statement")
    classification, lexeme = tokens.pop()

    if classification == "KEYWORD" or classification == "VARIABLE":         # if keyword or variable, correct syntax
        tokens.append((classification, lexeme))
        if lexeme == "VISIBLE":                     # if VISIBLE keyword found, go to print parse and return its output
            return print_parse()
        elif lexeme == "I HAS A":                   # if I HAS A keyword found, go to variable declaration parse and return its output
            return var_dec_parse()

def program_parse():                # topmost level, checks hai and kthxbye
    # print("parsing program")
    classification, lexeme = tokens.pop()
    
    while classification == "COMMENT":              # ignore comments at start of program
        classification, lexeme = tokens.pop()

    if classification == "KEYWORD":
        if lexeme == "HAI":                 # hai found
            program_list = []                       # make list and append hai
            program_list.append(lexeme)
            while True:                                     # iterate infinitely through all lexemes
                classification, lexeme = tokens.pop()
                # print(classification, lexeme)
                if classification == "NEWLINE":                 # ignore newline and comments
                    continue
                elif classification == "COMMENT":
                    continue
                elif lexeme == "KTHXBYE":                   # if end of program found, exit and return program list 
                    program_list.append(lexeme)
                    return program_list
                else:
                    tokens.append((classification, lexeme))         # otherwise, found other keyword, statement starts, go to parse statement and append that statement to list
                    program_list.append(statement_parse())
        else:
            print("Parse error!")


# Run the lexer and open the file explorer for file selection
lexer = lexical_analyzer.LOLCodeLexer()
tokens = lexer.analyze_file()
tokens_initial = tokens.copy()          # to store original tokens
tokens.reverse()                        # turn tokens into a stack
parsed_output = program_parse()
print(parsed_output)