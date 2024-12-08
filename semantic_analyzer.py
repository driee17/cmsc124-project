class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {"IT": []}  # Ensure IT starts as an empty list
        self.errors = []        # Accumulate semantic errors
        self.visible_outputs = []  # Holds outputs of VISIBLE statements
        self.in_variable_block = False  # Track if inside a WAZZUP block

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
        result = self.evaluate_expression(expressions)
        if result is not None:
            # Ensure IT is initialized as a list if it's not already
            if "IT" not in self.symbol_table:
                self.symbol_table["IT"] = []

            # Check if the expression directly refers to an identifier
            if isinstance(expressions, str) and expressions in self.symbol_table:
                # Output value but do not append to IT
                output = f"{result}"
                print(f"VISIBLE: {output}")  # Debugging output
                self.visible_outputs.append(output)  # Store for GUI
            elif not self.is_expression_tied_to_identifier(expressions):
                # Append to IT if the expression is not tied to an identifier
                self.symbol_table["IT"].append(result)
                output = f"{result}"
                print(f"VISIBLE (IT): {output}")  # Debugging for IT
                self.visible_outputs.append(output)  # Store for GUI
            else:
                # Output without appending to IT
                output = f"{result}"
                print(f"VISIBLE (not IT): {output}")  # Debugging for non-IT values
                self.visible_outputs.append(output)  # Store for GUI
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
        print(f"Evaluating expression: {expression}")

        # Handle single tokens (literals or variables)
        if isinstance(expression, str):
            # Numeric literals
            if expression.isdigit():
                return int(expression)  # NUMBR
            try:
                return float(expression)  # NUMBAR
            except ValueError:
                pass

            # String literals
            if expression.startswith('"') and expression.endswith('"'):
                return expression.strip('"')  # YARN (remove quotes)

            # Boolean literals
            if expression == "WIN":
                return 'WIN'  # TROOF
            if expression == "FAIL":
                return 'FAIL'  # TROOF

            # Variables from the symbol table
            if expression in self.symbol_table:
                return self.symbol_table[expression]

            # Undefined identifier
            self.errors.append(f"Undefined identifier: {expression}")
            return None

        # Handle nested list-style literals
        elif isinstance(expression, list):
            if len(expression) == 1:  # Single token wrapped in a list
                return self.evaluate_expression(expression[0])
            elif len(expression) > 1 and expression[0] == '"' and expression[-1] == '"':  # String literal
                return ''.join(expression[1:-1])  # Concatenate string parts

            # Handle arithmetic or logical operators
            operator = expression[0]
            if operator in {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"}:
                if len(expression) < 4 or expression[2] != "AN":
                    self.errors.append(f"Invalid binary operation: {expression}")
                    return None
                left = self.evaluate_expression(expression[1])  # Evaluate left operand
                right = self.evaluate_expression(expression[3])  # Evaluate right operand
                print(f"{operator}: {left} and {right}")  # Debugging
                if left is None or right is None:
                    self.errors.append(f"Cannot evaluate operands for operation: {expression}")
                    return None
                return self.compute_arithmetic(operator, left, right)

            elif operator == "BIGGR OF":
                left = self.evaluate_expression(expression[1])
                right = self.evaluate_expression(expression[2])
                if left is None or right is None:
                    self.errors.append(f"Cannot evaluate operands for BIGGR OF: {expression}")
                    return None
                return max(left, right)

            elif operator == "SMALLR OF":
                left = self.evaluate_expression(expression[1])
                right = self.evaluate_expression(expression[2])
                print(f"SMALLR OF: Comparing {left} and {right}")
                if left is None or right is None:
                    self.errors.append(f"Cannot evaluate operands for SMALLR OF: {expression}")
                    return None
                return min(left, right)

            else:
                self.errors.append(f"Unrecognized operator: {operator}")
                return None

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
                return left / right
            elif operator == "MOD OF":
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

