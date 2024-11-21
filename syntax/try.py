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

# update: test cases 4, 5, 6 error TODO fix smoosh+assign error and implement boolean operations and other keywords/statement types and refactor and variable type simplify

def yarn_parse():               # yarn literal parse
    yarn_list = []
    classification, lexeme = tokens.pop()
    yarn_list.append(lexeme)
    classification, lexeme = tokens.pop()
    yarn_list.append(lexeme)
    classification, lexeme = tokens.pop()
    yarn_list.append(lexeme)
    return yarn_list

def expr_parse():
    expr_list = []

    classification, lexeme = tokens.pop()
    expr_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR" or classification == "TROOF":
        expr_list.append(lexeme)
    elif classification == "STRING_DELIMITER":
        tokens.append((classification, lexeme))
        expr_list.append(yarn_parse())
    elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLER OF":
        tokens.append((classification, lexeme))
        expr_list.append(expr_parse())
    else:
        print("syntax error in expression")
        raise("LOLCode error")
    
    classification, lexeme = tokens.pop()
    if classification == "KEYWORD" and lexeme == "AN":
        expr_list.append(lexeme)
    else:
        print("syntax error in expression")
        raise("LOLCode error")
    
    classification, lexeme = tokens.pop()
    if classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR" or classification == "TROOF":
        expr_list.append(lexeme)
    elif classification == "STRING_DELIMITER":
        tokens.append((classification, lexeme))
        expr_list.append(yarn_parse())
    elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLR OF":
        tokens.append((classification, lexeme))
        expr_list.append(expr_parse())
    else:
        # print(classification, lexeme)
        print("syntax error in expression")
        raise("LOLCode error")
    
    return expr_list

def typecast_parse():
    typecast_list = []

    classification, lexeme = tokens.pop()
    typecast_list.append(lexeme)

    classification, lexeme = tokens.pop()
    if classification == "VARIABLE":
        typecast_list.append(lexeme)
    else:
        print("syntax error in typecast")
        raise("LOLCode error")

    classification, lexeme = tokens.pop()
    if lexeme == "A":
        typecast_list.append(lexeme)
    else:
        tokens.append((classification, lexeme))
        
    classification, lexeme = tokens.pop()
    if classification == "TYPE":
        typecast_list.append(lexeme)
    else:
        print("syntax error in typecast")
        raise("LOLCode error")
    
    return typecast_list

def assign_parse():             # TODO: SMOOSH + ASSIGN ERROR FIX
    assign_list = []
    
    classification, lexeme = tokens.pop()
    assign_list.append(lexeme)

    classification, lexeme = tokens.pop()
    if classification == "KEYWORD":
        if lexeme == "R":
            assign_list.append(lexeme)
            classification, lexeme = tokens.pop()
            if lexeme == "MAEK":
                tokens.append((classification, lexeme))
                assign_list.append(typecast_parse())
                return assign_list
            elif classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR"or classification == "TROOF":             # if next lexeme is variable or literal (that isn't a YARN) just append it and return the list
                assign_list.append(lexeme)
                return assign_list
            elif classification == "STRING_DELIMITER":              # if string delimiter is found, we hit yarn, parse yarn then return list
                tokens.append((classification, lexeme))
                assign_list.append(yarn_parse())
                return assign_list
            elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLR OF":
                tokens.append((classification, lexeme))
                assign_list.append(expr_parse())
                return assign_list
            else:                               # otherwise, syntax error
                # print(classification, lexeme)
                print("syntax error in assignment statement!")
                raise("LOLCode error")

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
        elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLR OF":
            tokens.append((classification, lexeme))
            var_dec_list.append(expr_parse())
            return var_dec_list
        else:                   # else, bad syntax
            print("syntax error in ITZ part of variable declaration!")
            raise("LOLCode error")
        
    return var_dec_list

def smoosh_parse():
    smoosh_list = []

    classification, lexeme = tokens.pop()
    smoosh_list.append(lexeme)

    classification, lexeme = tokens.pop()
    if classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR"or classification == "TROOF":
        smoosh_list.append(lexeme)
    elif classification == "STRING_DELIMITER":              # if string delimiter is found, we hit yarn, parse yarn then return list
        tokens.append((classification, lexeme))
        smoosh_list.append(yarn_parse())
    elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLR OF":
        tokens.append((classification, lexeme))
        smoosh_list.append(expr_parse())
    else:
        # print(classification, lexeme)
        print("syntax error in smoosh")
        raise("LOLCode error")
    
    while True:
        classification, lexeme = tokens.pop()
        if lexeme == "AN":
            smoosh_list.append(lexeme)
            classification, lexeme = tokens.pop()
            if classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR"or classification == "TROOF":
                smoosh_list.append(lexeme)
            elif classification == "STRING_DELIMITER":              # if string delimiter is found, we hit yarn, parse yarn then return list
                tokens.append((classification, lexeme))
                smoosh_list.append(yarn_parse())
            elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLR OF":
                tokens.append((classification, lexeme))
                smoosh_list.append(expr_parse())
            else:
                print("syntax error in smoosh")
                raise("LOLCode error")
        else:
            tokens.append((classification, lexeme))
            break
    
    return smoosh_list

def print_parse():              # print statement parse
    # print("parsing print")
    print_list = []                 # initialize list for print statement

    classification, lexeme = tokens.pop()           # add "VISIBLE" lexeme to list then pop next lexeme
    print_list.append(lexeme)
    classification, lexeme = tokens.pop()

    if classification == "VARIABLE" or classification == "NUMBR" or classification == "NUMBAR" or classification == "TROOF":             # if next lexeme is variable or literal (that isn't a YARN) just append it and return the list
        print_list.append(lexeme)
        return print_list
    elif classification == "STRING_DELIMITER":              # if string delimiter is found, we hit yarn, parse yarn then return list
        tokens.append((classification, lexeme))
        print_list.append(yarn_parse())
        return print_list
    elif lexeme == "SUM OF" or lexeme == "DIFF OF" or lexeme == "PRODUKT OF" or lexeme == "QUOSHUNT OF" or lexeme == "MOD OF" or lexeme == "BIGGR OF" or lexeme == "SMALLR OF":
        tokens.append((classification, lexeme))
        print_list.append(expr_parse())
        return print_list
    elif lexeme == "NUMBR" or lexeme == "NUMBAR" or lexeme == "YARN" or lexeme == "TROOF":              # if lexeme is of literal type TYPE, also append it to list and return list
        print_list.append(lexeme)
        return print_list
    elif lexeme == "SMOOSH":
        tokens.append((classification, lexeme))
        print_list.append(smoosh_parse())
        return print_list
    else:                               # otherwise, syntax error
        # print(classification, lexeme)
        print("syntax error in print statement!")
        raise("LOLCode error")

def statement_parse():                  # statement parse
    # print("parsing statement")
    classification, lexeme = tokens.pop()
    # print(classification, lexeme)

    if classification == "KEYWORD" or classification == "VARIABLE":         # if keyword or variable, correct syntax
        tokens.append((classification, lexeme))
        if lexeme == "VISIBLE":                     # if VISIBLE keyword found, go to print parse and return its output
            return print_parse()
        elif lexeme == "I HAS A":                   # if I HAS A keyword found, go to variable declaration parse and return its output
            return var_dec_parse()
        elif classification == "VARIABLE":
            return assign_parse()
        else:
            classification, lexeme = tokens.pop()
            return ["<other statement>"]

def program_parse():                # topmost level, checks hai and kthxbye
    # print("parsing program")
    classification, lexeme = tokens.pop()
    
    while classification == "COMMENT" or classification == "NEWLINE":              # ignore comments at start of program
        classification, lexeme = tokens.pop()
    
    # print(classification, lexeme)

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

# ======= SOME REFERENCES
# https://www.booleanworld.com/building-recursive-descent-parsers-definitive-guide/
# https://cratecode.com/info/python-recursive-descent-parser
# https://stackoverflow.com/questions/19749883/how-to-parse-parenthetical-trees-in-python