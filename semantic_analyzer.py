class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}  # Track variables/functions and their details
        self.errors = []        # Accumulate semantic errors
        self.in_variable_block = False  # Track whether we are inside a WAZZUP block

    def analyze(self, syntax_output):
        """Analyze the structured output from the syntax analyzer."""
        if isinstance(syntax_output, list):  # Assume list structure
            for statement in syntax_output:
                self.process_statement(statement)
        else:
            self.errors.append("Invalid syntax analyzer output.")
        return len(self.errors) == 0

    def process_statement(self, statement):
        """Process individual statements based on their type."""
        if isinstance(statement, list) and statement:
            keyword = statement[0]

            if keyword == "WAZZUP":  # Start of variable block
                self.handle_wazzup(statement)
            elif keyword == "BUHBYE":  # End of variable block
                self.handle_buhbye(statement)
            elif self.in_variable_block and keyword == "I HAS A":  # Variable declaration
                self.handle_variable_declaration(statement)
            elif keyword == "VISIBLE":  # Output statement
                self.handle_output(statement)
            elif len(statement) > 1 and statement[1] == "R":  # Assignment
                self.handle_assignment(statement)
            elif keyword == "HOW IZ I":  # Function declaration
                self.handle_function_declaration(statement)
            elif keyword in {"O RLY?", "IM IN YR", "WTF?"}:  # Control structures
                self.handle_control_structure(statement)
            else:
                self.errors.append(f"Unrecognized statement: {statement}")

    def handle_wazzup(self, statement):
        """Start of variable declaration block."""
        if self.in_variable_block:
            self.errors.append("Nested WAZZUP blocks are not allowed.")
        else:
            self.in_variable_block = True

    def handle_buhbye(self, statement):
        """End of variable declaration block."""
        if not self.in_variable_block:
            self.errors.append("BUHBYE encountered outside of a WAZZUP block.")
        else:
            self.in_variable_block = False

    def handle_variable_declaration(self, statement):
        """Check variable declarations."""
        try:
            var_name = statement[1]
            if var_name in self.symbol_table:
                self.errors.append(f"Variable '{var_name}' is already declared.")
            else:
                # Add variable to symbol table
                initial_value = statement[3] if len(statement) > 3 and statement[2] == "ITZ" else "NOOB"
                self.symbol_table[var_name] = initial_value
        except IndexError:
            self.errors.append(f"Invalid variable declaration: {statement}")

    def handle_assignment(self, statement):
        """Check assignments for correctness."""
        try:
            var_name = statement[0]
            if var_name not in self.symbol_table:
                self.errors.append(f"Variable '{var_name}' assigned before declaration.")
            else:
                # Optionally validate the value type
                value = statement[2]
                self.symbol_table[var_name] = value
        except IndexError:
            self.errors.append(f"Invalid assignment statement: {statement}")

    def handle_output(self, statement):
        """Handle VISIBLE (output) statements."""
        # Verify each argument in the output statement
        for value in statement[1:]:
            print(value[0])
            if isinstance(value, str) and value not in self.symbol_table:
                self.errors.append(f"Undefined variable '{value}' in output statement.")

    def handle_function_declaration(self, statement):
        """Handle function declarations."""
        func_name = statement[1]
        if func_name in self.symbol_table:
            self.errors.append(f"Function '{func_name}' is already declared.")
        else:
            self.symbol_table[func_name] = "FUNCTION"

    def handle_control_structure(self, statement):
        """Validate control structures."""
        # Add logic for O RLY?, IM IN YR, etc., as needed
        pass

    def report_errors(self):
        """Return all semantic errors."""
        return self.errors
