import re

identifier_regex = "\\b[a-zA-Z][a-zA-Z0-9_]*\\b"
literal_regex = {"\\b-?[0-9]+\\b": "Integer Literal",
                 "\\b-?[0-9]+\.[0-9]+\\b": "Float Literal",
                 "\".*?\"": "String Literal",
                 "\\b(WIN|FAIL)\\b": "Boolean Literal",
                 "\\b(NOOB|NUMBR|NUMBAR|YARN|TROOF)\\b": "Type Literal"}
keyword_regex = {"\\bHAI\\b": "Code Delimiter",
                 "\\bKTHXBYE\\b": "Code Delimiter",
                 "\\bWAZZUP\\b": "Variable Declaration Clause Delimiter",
                 "\\bBUHBYE\\b": "Variable Declaration Clause Delimiter",
                 "\\bBTW\\b": "Comment",
                 "\\bOBTW\\b": "Comment Delimiter",
                 "\\bTLDR\\b": "Comment Delimiter",
                 "I HAS A": "Variable Declaration",
                 "\\bITZ\\b": "Variable Iniitalization",
                 "\\bR\\b": "Variable Assignment",
                 "\\bSUM OF\\b": "Addition Operation",
                 "\\bDIFF OF\\b": "Subtraction Operation",
                 "\\bPRODUKT OF\\b": "Multiplication Operation",
                 "\\bQUOSHUNT OF\\b": "Divistion Operation",
                 "\\bMOD OF\\b": "Modulo Operation",
                 "\\bBIGGR OF\\b": "Max Operation",
                 "\\bSMALLR OF\\b": "Min Operation",
                 "\\bBOTH OF\\b": "Boolen AND",
                 "\\bEITHER OF\\b": "Boolean OR",
                 "\\bWON OF\\b": "Boolean XOR",
                 "\\bNOT\\b": "Boolean NOT",
                 "\\bANY OF\\b": "Boolean OR (Infinite Arity)",
                 "\\bALL OF\\b": "Boolean AND (Infinite Arity)",
                 "\\bBOTH SAEM\\b": "Comparison Operation ==",
                 "\\bDIFFRINT\\b": "Comparison Operation !=",
                 "\\bSMOOSH\\b": "String Concatenation",
                 "\\bMAEK\\b": "Explicit Typecast",
                 "\\bA\\b": "Partial Keyword",
                 "\\bIS NOW A\\b": "Explicit Typecast",
                 "\\bVISIBLE\\b": "Output Keyword",
                 "\\bGIMMEH\\b": "Input Keyword",
                 "\\bO RLY\?\\b": "If Block Start",
                 "\\bYA RLY\\b": "Condition Met Code Block Delimiter",
                #  "^MEBBE\\b": "Else If Code Block Delimiter",                 # not required to implement
                 "\\bNO WAI\\b": "Condition Not Met Code Block Delimiter",
                 "\\bOIC\\b": "If/Switch Block End",
                 "\\bWTF\?\\b": "Switch Block Start",
                 "\\bOMG\\b": "Case Keyword",
                 "\\bOMGWTF\\b": "Default Case Keyword",
                 "\\bIM IN YR\\b": "Loop Delimiter",
                 "\\bUPPIN\\b": "Increment Operation",
                 "\\bNERFIN\\b": "Decrement Operation",
                 "\\bYR\\b": "Partial Keyword",
                 "\\bTIL\\b": "Repeat Loop Until Condition Met",
                 "\\bWILE\\b": "Repeat Loop While Condition Met",
                 "\\bIM OUTTA YR\\b": "Loop Delimiter",
                 "\\bHOW IZ I\\b": "Function Delimiter",
                 "\\bIF U SAY SO\\b": "Function Delimiter",
                 "\\bGTFO\\b": "Break Keyword",
                 "\\bFOUND YR\\b": "Return Keyword",
                 "\\bI IZ\\b": "Function Call Keyword",
                 "\\bMKAY\\b": "Boolean Statement End"}

def tokenize_file(file_name):               # pass file name as paramenter (must be in same directory)
    tokens = []                 # all tokens, TODO eventually put the tokens back in order
    token_classes = []                  # unused yet, TODO also put token classes for each corresponding token index in order
    input_file = open(file_name, "r")

    for line in input_file.readlines():             # get all lines, remove leading spaces
        tokens.append(re.sub("^\s*", "", line))
    
    for line in tokens:                         # for each line
        line_lexemes = []
        line_lexeme_classes = []
        currline = line

        while currline != "":                       # copy line to currline, cut currline up into chunks of lexemes
            flag = False                            # flag for loop exiting
            for k, v in keyword_regex.items():              # iterate through all keyword regexes in dictionary
                matchfound = re.search(k, currline)                 # match regex to line string
                if matchfound:                                      # if match found
                    if matchfound.start() == 0:                         # check if that match is at the start of currline (we are interested chopping the line from the start one by one), will help with appending lexemes and their classifications correctly to their corresponding lists
                        print(v + " found\n")
                        currline = currline[matchfound.end():]                  # TODO append lexeme to line_lexemes list, append corresponding classification to line_lexeme_classes list
                        flag = True                         # set flag as found, don't bother continuing the loop, otherwise keep looping
                        break
            if flag:
                continue

            flag = False
            for k, v in literal_regex.items():                      # if no keyword regex match, try literals
                matchfound = re.search(k, currline)                 # same logic, only regex differs
                if matchfound:
                    if matchfound.start() == 0:
                        print(v + " found\n")
                        currline = currline[matchfound.end():]
                        flag = True
                        break
            if flag:
                continue

            matchfound = re.search(identifier_regex, currline)              # lastly, if neither keyword regex nor literal, try identifier
            if matchfound:
                if matchfound.start() == 0:
                    print("identifier found\n")
                    currline = currline[matchfound.end():]
                    continue

            if currline == "\n":
                currline = ""
                continue

            matchfound = re.search("\s", currline)
            if matchfound:
                if matchfound.start() == 0:
                    currline = currline[matchfound.end():]
                    continue
            
tokenize_file("test.lol")
