class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {"IT": []}  # Ensure IT starts as an empty list
        self.errors = []        # Accumulate semantic errors
        self.visible_outputs = []  # Holds outputs of VISIBLE statements
        self.in_variable_block = False  # Track if inside a WAZZUP block
        self.it = None          # Implicit IT variable

    def analyze(self, syntax_output, input_callback=None):
        """Analyze the structured output from the syntax analyzer."""
        if not isinstance(syntax_output, list):
            self.errors.append("Invalid syntax output structure.")
            return False

        for statement in syntax_output:
            self.process_statement(statement, input_callback=input_callback)

        print(f"Final Symbol Table: {self.symbol_table}")
        return len(self.errors) == 0

    def process_statement(self, statement, input_callback=None):
        print(f"Processing statement: {statement}")
        """Process a single statement."""
        if isinstance(statement, str):  # Handle standalone keywords
            if statement == "HAI":
                return  # Ignore program start
            elif statement == "KTHXBYE":
                return  # Ignore program end
            else:
                self.errors.append(f"Invalid statement format: {statement}")
                return

        if isinstance(statement, list) and statement:
            keyword = statement[0]
            if keyword == "WAZZUP":
                self.in_variable_block = True
                for var_decl in statement[1:]:
                    if var_decl == "BUHBYE":
                        self.in_variable_block = False
                        break
                    self.handle_variable_declaration(var_decl)
            elif keyword == "VISIBLE":
                self.handle_visible(statement[1])
            elif keyword == "GIMMEH":
                self.handle_gimmeh(statement[1], input_callback=input_callback)
            else:
                self.errors.append(f"Unrecognized statement: {statement}")
        else:
            self.errors.append(f"Invalid statement format: {statement}")

    def handle_variable_declaration(self, declaration):
        """Process variable declarations in the WAZZUP block."""
        if len(declaration) < 2 or declaration[0] != "I HAS A":
            self.errors.append(f"Invalid variable declaration: {declaration}")
            return

        var_name = declaration[1]
        if var_name in self.symbol_table:
            self.errors.append(f"Variable '{var_name}' already declared.")
            return

        # Handle initialization
        if len(declaration) > 2 and declaration[2] == "ITZ":
            value = self.evaluate_expression(declaration[3])
        else:
            value = "NOOB"  # Default uninitialized value

        self.symbol_table[var_name] = value
        print(f"Declared variable: {var_name} = {value}")

    def handle_visible(self, expressions):
        """Process VISIBLE statements."""
        print(f"Processing VISIBLE: {expressions}")
        
        # Function to check if concatenation ('+') is present
        def contains_plus(exp):
            return isinstance(exp, list) and '+' in exp

        # Handle concatenation explicitly
        if contains_plus(expressions):
            concatenated_result = ''
            for part in expressions:
                if part == '+':
                    print("Found '+', skipping to next part")  # Debugging
                    continue
                # Evaluate each part recursively
                evaluated = self.evaluate_expression(part)
                print(f"Evaluated part: {part}, Result: {evaluated}")  # Debugging
                if evaluated is None:
                    self.errors.append(f"Failed to evaluate part of VISIBLE statement: {part}")
                    return
                concatenated_result += str(evaluated)
            # Store the concatenated result in 'IT'
            self.symbol_table["IT"] = concatenated_result
            print(f"VISIBLE (IT): {concatenated_result}")  # Debugging
            self.visible_outputs.append(concatenated_result)  # Store for GUI
        else:
            # Evaluate as a single expression
            result = self.evaluate_expression(expressions)
            if result is not None:
                print(f"Evaluated single expression for VISIBLE: {result}")  # Debugging
                # Store in 'IT' only for non-identifier results
                if not self.is_expression_tied_to_identifier(expressions):
                    if "IT" not in self.symbol_table or not isinstance(self.symbol_table["IT"], list):
                        self.symbol_table["IT"] = []
                    self.symbol_table["IT"].append(result)
                self.visible_outputs.append(result)  # Store for GUI
            else:
                self.errors.append(f"Failed to evaluate VISIBLE statement: {expressions}")

    def is_expression_tied_to_identifier(self, expression):
        """Check if the given expression corresponds to an explicit identifier."""
        if isinstance(expression, str):
            # If the expression is a direct reference to a variable
            return expression in self.symbol_table
        if isinstance(expression, list) and len(expression) == 1:
            # If the expression is wrapped in a list, check the single element
            return self.is_expression_tied_to_identifier(expression[0])
        # Otherwise, it's not tied to any specific identifier
        return False

    def handle_gimmeh(self, variable_name, input_callback=None):
        """Handle the GIMMEH keyword to prompt user input."""
        if variable_name not in self.symbol_table:
            self.errors.append(f"Undefined variable: {variable_name}")
            return

        if input_callback is not None:
            # Use the input callback to get input from the GUI
            user_input = input_callback(variable_name)
            if user_input is not None:
                # Store the user input as a YARN but allow for numeric inference
                try:
                    # Infer type: NUMBR if integer, NUMBAR if float, else YARN
                    if user_input.isdigit():
                        self.symbol_table[variable_name] = int(user_input)
                    else:
                        self.symbol_table[variable_name] = float(user_input)
                except ValueError:
                    self.symbol_table[variable_name] = user_input  # Store as YARN (string)
                
                print(f"User input received for {variable_name}: {self.symbol_table[variable_name]}")
            else:
                self.errors.append(f"No input provided for variable: {variable_name}")
        else:
            self.errors.append("No input callback provided for GIMMEH.")


    def evaluate_expression(self, expression):
        """Evaluate expressions recursively."""
        # Handle single tokens (literals or variables)
        print(f"Evaluating expression: {expression}")
        if isinstance(expression, str):
            # Check for numeric literals
            if expression.isdigit():
                return int(expression)  # NUMBR
            try:
                return float(expression)  # NUMBAR
            except ValueError:
                pass

            # Check for string literals
            if expression.startswith('"') and expression.endswith('"'):
                value = expression.strip('"')  # YARN (remove quotes)
                # Try converting to number if used in arithmetic
                if value.isdigit():
                    return int(value)
                try:
                    return float(value)
                except ValueError:
                    return value  # Return as YARN if not numeric

            # Check for boolean literals
            if expression == "WIN":
                return True  # TROOF
            if expression == "FAIL":
                return False  # TROOF

            # Check for variables in the symbol table
            if expression in self.symbol_table:
                value = self.symbol_table[expression]
                if value == "NOOB":
                    return value  # Allow NOOB for non-arithmetic contexts
                return value

            # If the expression is not recognized
            self.errors.append(f"Undefined identifier: {expression}")
            return None

        # Handle nested list-style literals (like ['"', 'seventeen', '"'])
        elif isinstance(expression, list):
            # Handle single-element list (e.g., ['x'] or nested lists like [['x']])
            if len(expression) == 1:
                print(f"Single element list: {expression}")  # Debugging
                return self.evaluate_expression(expression[0])

            # Handle string literals in list form (e.g., ['"', 'declarations', '"'])
            if len(expression) > 1 and expression[0] == '"' and expression[-1] == '"':
                print(f"String literal in list form: {expression}")  # Debugging
                return ''.join(expression[1:-1])

            # Concatenation with '+' operator
            if '+' in expression:
                concatenated = ''
                for part in expression:
                    if part == '+':
                        continue
                    value = self.evaluate_expression(part)
                    if value is None:
                        self.errors.append(f"Failed to evaluate part of concatenation: {part}")
                        return None
                    concatenated += str(value)
                return concatenated
            # Handle arithmetic or logical operators
            operator = expression[0]
            if operator in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"}:
                if len(expression) < 4 or expression[2] != "AN":
                    self.errors.append(f"Invalid binary operation: {expression}")
                    return None
                left = self.evaluate_expression(expression[1])  # Evaluate left operand
                right = self.evaluate_expression(expression[3])  # Evaluate right operand
                print(f"{operator}: Left = {left}, Right = {right}")  # Debugging
                left = 1 if left == "WIN" else (0 if left == "FAIL" else left)
                right = 1 if right == "WIN" else (0 if right == "FAIL" else right)
                if left is None or right is None:
                    self.errors.append(f"Cannot evaluate operands for operation: {expression}")
                    return None
                return self.compute_arithmetic(operator, left, right)

            # Handle BIGGR OF and SMALLR OF
            elif operator in {"BIGGR OF", "SMALLR OF"}:
                left = self.evaluate_expression(expression[1])
                right = self.evaluate_expression(expression[2])
                print(f"{operator}: Left = {left}, Right = {right}")  # Debugging
                left = 1 if left == "WIN" else (0 if left == "FAIL" else left)
                right = 1 if right == "WIN" else (0 if right == "FAIL" else right)
                return max(left, right) if operator == "BIGGR OF" else min(left, right)

            # Unrecognized operator
            else:
                self.errors.append(f"Unrecognized operator: {operator}")
                return None

        # Invalid expression type
        else:
            self.errors.append(f"Invalid expression format: {expression}")
            return None

    def compute_arithmetic(self, operator, left, right):
        """Perform arithmetic operations."""
        try:
            if operator == "SUM OF":
                return left + right
            elif operator == "DIFF OF":
                return left - right
            elif operator == "PRODUKT OF":
                return left * right
            elif operator == "QUOSHUNT OF":
                if right == 0:
                    self.errors.append("Division by zero in QUOSHUNT OF")
                    return None
                return left / right
            elif operator == "MOD OF":
                if right == 0:
                    self.errors.append("Division by zero in MOD OF")
                    return None
                return left % right
            elif operator == 'BIGGR OF':
                return max(left, right)
            elif operator == 'SMALLR OF':
                return min(left, right)
            elif operator == 'BOTH OF':
                return 'WIN' if (left and right) else 'FAIL'
            elif operator == 'EITHER OF':
                return 'WIN' if (left or right) else 'FAIL'
            elif operator == 'WON OF':
                return 'WIN' if (left or right) and not (left and right) else 'FAIL'
            elif operator == 'BOTH SAEM':
                return 'WIN' if (left == right) else 'FAIL'
            elif operator == 'DIFFRINT':
                return 'WIN' if (left != right) else 'FAIL'
            else:
                self.errors.append(f"Unknown arithmetic operator: {operator}")
                return None
        except TypeError:
            self.errors.append(f"Type error in operation '{operator}' with operands '{left}' and '{right}'.")
            return None
        except ZeroDivisionError:
            self.errors.append("Division by zero.")
            return None

    def get_visible_outputs(self):
        """Return all visible outputs."""
        return self.visible_outputs

    def report_errors(self):
        """Return all semantic errors."""
        return self.errors

