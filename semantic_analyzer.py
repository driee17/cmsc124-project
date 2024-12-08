class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Track variables/functions and their details
        self.errors = []        # Accumulate semantic errors
        self.visible_outputs = []  # Holds outputs of VISIBLE statements
        self.in_variable_block = False  # Track if inside a WAZZUP block
        self.it = None          # Implicit IT variable

    def analyze(self, syntax_output):
        print(f"Symbol Table: {self.symbol_table}") 
        """Analyze the structured output from the syntax analyzer."""
        if not isinstance(syntax_output, list):
            self.errors.append("Invalid syntax output structure.")
            return False

        for statement in syntax_output:
            self.process_statement(statement)
        
        print(f"Final Symbol Table: {self.symbol_table}")
        return len(self.errors) == 0


    def process_statement(self, statement):
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
            output = f"{result}"
            print(output)  # Print to console for debugging
            self.visible_outputs.append(output)  # Store for GUI
            self.it = result  # Update IT variable
        else:
            self.errors.append(f"Failed to evaluate VISIBLE statement: {expressions}")

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
                return expression.strip('"')  # YARN (remove quotes)

            # Check for boolean literals
            if expression == "WIN":
                return 'WIN'  # TROOF
            if expression == "FAIL":
                return 'FAIL'  # TROOF

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

            # Handle BIGGR OF and SMALLR OF
            elif expression[0] == "BIGGR OF":
                left = self.evaluate_expression(expression[1])
                right = self.evaluate_expression(expression[2])
                if left is None or right is None:
                    self.errors.append(f"Cannot evaluate operands for BIGGR OF: {expression}")
                    return None
                result = max(left, right)
                print(f"BIGGR OF: Comparing {left} and {right}, result = {result}")  # Debugging
                return result


            elif operator == "SMALLR OF":
                print(f"SMALLR OF: Evaluating {expression}")
                left = self.evaluate_expression(expression[1])
                right = self.evaluate_expression(expression[2])
                print(f"SMALLR OF: Comparing {left} and {right}")
                if left is None or right is None:
                    self.errors.append(f"Cannot evaluate operands for SMALLR OF: {expression}")
                    return None
                return min(left, right)

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

