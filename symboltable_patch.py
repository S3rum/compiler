import sys

label = 1
temp_var_num = 1  # temporary variable counter.
current_subprogram = []
program_name = ""
all_quads = {}
allVariableRecords = []
voffset = 0



class Token:
    def __init__(self, family, recognized_string, line_number, token_number):
        self.family = family
        self.recognized_string = recognized_string
        self.line_number = line_number
        self.token_number = token_number


class Lexer:
    def __init__(self):
        self.text = self.filepath()
        self.pos = 0  # Current position in given file
        self.prev_char = self.text[self.pos - 1]
        self.current_char = self.text[self.pos]
        self.next_char = self.text[self.pos + 1]
        self.token_number = 0
        self.current_line = 1

    def filepath(self):
        #filepath = input("Give me the file's path: ")
        filepath = "C:\\Users\\srig\\Desktop\\Uni\\compiler\\test.cpy"
        with open(filepath, "r") as fd:
            return fd.read()  # Read the file contents

    def _get_id(self):  # Find identifiers
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

    def number(self):
        if self.prev_char == "-" and self.current_char.isdigit():
            result = "-"
            while self.current_char is not None and self.current_char.isdigit():
                if self.next_char.isalpha():
                    print("Shouldnt expect char after number in line:", self.current_line)
                    sys.exit()
                result += self.current_char
                if int(result) < -32767:
                    print("The current integer is too big in line:", self.current_line)
                    sys.exit()
                self.advance()
            self.token_number += 1
            token = Token("NUMBER", result, self.current_line, self.token_number, )
            return token
        else:
            result = ""
            while self.current_char is not None and self.current_char.isdigit():
                if self.next_char.isalpha():
                    print("Shouldn't expect char after number in line:", self.current_line)
                    sys.exit()
                result += self.current_char
                if int(result) > 32767:
                    print("The current integer is too big in line:", self.current_line)
                    sys.exit()
                self.advance()
            self.token_number += 1
            token = Token("NUMBER", result, self.current_line, self.token_number,)
            return token

    def advance(self):
        self.pos += 1
        if self.pos == len(self.text):
            self.current_char = None
        elif self.pos == len(self.text) - 1:
            self.current_char = self.text[self.pos]
        else:
            self.current_char = self.text[self.pos]
            self.next_char = self.text[self.pos + 1]
            self.prev_char = self.text[self.pos - 1]

    def lexical_analyzer(self):
        while self.current_char != "None":
            if self.current_char is None:
                self.token_number += 1
                token = Token("EOF", "EOF", self.current_line, self.token_number)
                self.pos = 0  # Current position in given file
                self.current_char = self.text[self.pos]
                self.next_char = self.text[self.pos + 1]
                self.token_number = 0
                self.current_line = 1

                return token  # End of file
            if self.current_char == "#" and self.next_char == "#":
                self.advance()
                self.advance()
                while self.current_char != "#":
                    self.advance()
                if self.current_char == "#" and self.next_char == "#":
                    self.advance()
                    self.advance()
                else:
                    self.advance()

            elif self.current_char == "\n":
                self.advance()
                self.current_line += 1
                continue

            elif self.current_char.isspace():
                self.advance()
                continue

            elif self.current_char.isdigit():
                return self.number()

            elif self.current_char.isalpha():  # Keywords or Identifiers
                token_str = self._get_id()
                self.token_number += 1
                if token_str in ["def", "not", "int", "global", "main", "if", "elif", "else", "while", "print", "return", "input", "and", "or"]:
                    token = Token("KEYWORD", token_str, self.current_line, self.token_number, )

                    return token

                else:
                    token = Token("ID", token_str, self.current_line, self.token_number,)  # Identifiers

                    return token

            # Handle operators
            elif self.current_char in ["*", "/", "%"]:
                self.token_number += 1
                if self.current_char == "/" and self.next_char == "/":
                    token = Token("MUL_OPERATOR", self.current_char + self.next_char, self.current_line, self.token_number)

                    self.advance()
                    self.advance()
                else:
                    token = Token("MUL_OPERATOR", self.current_char, self.current_line, self.token_number)
                    self.advance()
                return token

            # Handle add operators
            elif self.current_char == "+":
                self.token_number += 1
                token = Token("ADD_OPERATOR", self.current_char, self.current_line, self.token_number)
                self.advance()
                return token

            elif self.current_char == "-":
                self.token_number += 1
                token = Token("ADD_OPERATOR", self.current_char, self.current_line, self.token_number)
                self.advance()
                return token

            # Handle comparators
            elif self.current_char == "<":
                if self.next_char == "=":
                    self.token_number += 1
                    token = Token("COMPARATOR", self.current_char + self.next_char, self.current_line,
                                  self.token_number)

                    self.advance()
                    self.advance()
                    return token

                else:
                    self.token_number += 1
                    token = Token("COMPARATOR", self.current_char, self.current_line, self.token_number)

                    self.advance()
                    return token
            elif self.current_char == ">":
                if self.next_char == "=":
                    self.token_number += 1
                    token = Token("COMPARATOR", self.current_char + self.next_char, self.current_line,
                                  self.token_number)

                    self.advance()
                    self.advance()
                    return token

                else:
                    self.token_number += 1
                    token = Token("COMPARATOR", self.current_char, self.current_line, self.token_number)

                    self.advance()
                    return token

            elif self.current_char == "!" and self.next_char == "=":
                self.token_number += 1
                token = Token("COMPARATOR", self.current_char, self.current_line, self.token_number)

                self.advance()
                self.advance()
                return token

            # Handle =
            elif self.current_char in ["="]:
                if self.next_char == "=":
                    self.token_number += 1
                    token = Token("COMPARATOR", self.current_char+self.next_char, self.current_line, self.token_number)

                    self.advance()
                    self.advance()
                    return token
                else:
                    self.token_number += 1
                    token = Token("EQUAL", self.current_char, self.current_line, self.token_number)

                    self.advance()
                    return token

            # Handle delimiters
            elif self.current_char == ",":
                self.token_number += 1
                token = Token("DELIMITER", self.current_char, self.current_line, self.token_number)

                self.advance()
                return token

            elif self.current_char == ":":
                if self.next_char.isspace():
                    self.token_number += 1
                    token = Token("DELIMITER", self.current_char, self.current_line, self.token_number)
                    self.advance()
                    return token
                else:
                    print("Shouldn't expect a value after : in line", self.current_line)
                    sys.exit()

            # Handle parentheses
            elif self.current_char in ["(", ")"]:
                self.token_number += 1
                token = Token("GROUP SYMBOL", self.current_char, self.current_line, self.token_number)

                self.advance()
                return token

            elif self.current_char == "#" and self.next_char in ["{", "}"]:
                self.token_number += 1
                token = Token("GROUP SYMBOL", self.current_char+self.next_char, self.current_line, self.token_number)
                self.advance()
                self.advance()
                return token

            elif self.current_char == "#" and self.next_char == "i":
                self.advance()
                token_str = self._get_id()
                if token_str == "int":
                    return Token("KEYWORD", "#" + token_str, self.current_line, self.token_number)
            elif self.current_char == "#" and self.next_char == "d":
                self.advance()
                token_str = self._get_id()
                if token_str == "def":
                    return Token("KEYWORD", "#" + token_str, self.current_line, self.token_number)
            else:
                print("Unexpected token in line: ", self.current_line)
                sys.exit()


class SymbolTable:
    def __init__(self):
        self.scopes = [{}]
        self.global_scope = self.scopes[0]

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Attempt to pop global scope")

    def add_variable(self, name, datatype, is_global=False):
        # Calculate offset based on the scope the variable is being added to
        offset = self.current_offset(is_global)

        variable = Variable(name, datatype, offset)
        if is_global:
            self.global_scope[name] = variable  # Add to global scope
        else:
            self.scopes[-1][name] = variable  # Add to current scope

    def current_offset(self, is_global=False):
        if is_global:
            return len(self.global_scope) * 4  # Offset within global scope
        else:
            return sum(len(scope) * 4 for scope in self.scopes)  # Total offset across all scopes

    def add_function(self, name, starting_quad, datatype, formal_parameters, frame_length):
        function = Function(name, starting_quad, datatype, formal_parameters, frame_length)
        self.scopes[-1][name] = function

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None



    def __str__(self):
        result = []
        for i, scope in enumerate(self.scopes):
            result.append(f"Scope {i}:")
            for name, entity in scope.items():
                if isinstance(entity, Function):
                    result.append(f"  {name} : {entity.datatype}")
                else:
                    result.append(f"  {name} : {entity.datatype} {entity.offset}")  # Use the stored offset

        return "\n".join(result)



class Parser:
    def __init__(self, lexer, symbolTable):
        self.lexer = lexer
        self.current_token = self.lexer.lexical_analyzer()
        self.next_token = self.lexer.lexical_analyzer()
        self.symbol_table = symbolTable  # Instantiate symbol table
        self.looper()

    def program(self):
        global program_name
        program_name = self.next_token.recognized_string
        print("Program '" + program_name + "' has started.")
        if self.current_token.recognized_string == "def":
            self.def_function(program_name)
        elif self.current_token.recognized_string == "#def":
            self.def_main_function(program_name)
        else:
            self.error("def")

    def looper(self):
        while self.current_token.recognized_string == "def" or self.current_token.recognized_string == "#def":
            self.program()
        if self.current_token.recognized_string == "EOF":
            print("\nParsing ended successfully.")
            print("\nSymbol Table:")
            print(self.symbol_table)

    def def_main_function(self, subprogram_id: str):
        if self.current_token.family == "KEYWORD" and self.current_token.recognized_string == "#def":
            if self.get_token().recognized_string != "main":
                self.error("main")
            self.get_token()
            self.symbol_table.enter_scope()  # Enter a new scope for the main function
            self.declarations(subprogram_id)
            self.globals(subprogram_id)
            self.statements(subprogram_id)
            self.symbol_table.exit_scope()  # Exit the main function scope

    def def_function(self, subprogram_id: str):
        global current_subprogram
        if self.current_token.family != "KEYWORD" and self.current_token.recognized_string != "def":
            self.error("def")
        self.get_token()

        subprogram_id = self.current_token.recognized_string
        current_subprogram = subprogram_id

        self.symbol_table.enter_scope()  # Enter a new scope for the function

        self.parse_id_element()
        if self.get_token().recognized_string != "(":
            self.error("(")
        self.get_token()
        self.id_list(is_parameters=True)
        if self.current_token.recognized_string != ":":
            self.error(":")
        if self.get_token().recognized_string != "#{":
            self.error("#{")
        self.get_token()
        self.globals(subprogram_id)
        self.declarations(subprogram_id)

        self.symbol_table.add_function(subprogram_id, next_quad(), "int", [], 12)
        gen_quad("begin_block", subprogram_id, '_', '_')

        while True:
            if self.current_token.recognized_string == "#int":
                self.declarations(subprogram_id)
            if self.current_token.recognized_string == "def":
                self.def_function(subprogram_id)
            if self.current_token.recognized_string == "global":
                self.globals(subprogram_id)
            if self.current_token.family == "ID":
                self.statements(subprogram_id)
            else:
                break

        gen_quad("halt", '_', '_', '_')
        gen_quad('end_block', subprogram_id, '_', '_')

        self.symbol_table.exit_scope()  # Exit the function scope

        if self.current_token.recognized_string != "#}":
            self.error("#}")
        if self.current_token.recognized_string == "#}":
            self.get_token()

    def globals(self, subprogram_id: str):
        while self.current_token.recognized_string == "global":
            self.get_token()
            if self.next_token.family != "ID":
                self.error("ID after global")
            while self.current_token.family == "ID":
                var_name = self.current_token.recognized_string
                self.symbol_table.add_variable(var_name, "int", is_global=True)
                self.get_token()
                if self.current_token.recognized_string == ",":
                    self.get_token()
                else:
                    break

    def declarations(self, subprogram_id: str):
        while self.current_token.recognized_string == "#int":
            self.get_token()
            if self.current_token.family != "ID":
                self.error("variable name after #int")
            while self.current_token.family == "ID":
                var_name = self.current_token.recognized_string

                self.symbol_table.add_variable(var_name, "int")
                self.get_token()

                if self.current_token.recognized_string == ",":
                    self.get_token()
                else:
                    break

    def id_list(self, is_parameters=False):
        if self.current_token.family != "ID":
            self.error("variable name")
        while True:
            var_name = self.current_token.recognized_string
            self.symbol_table.add_variable(var_name, "int")
            self.get_token()
            if self.current_token.recognized_string != ",":
                break
            self.get_token()
        if is_parameters:
            if self.current_token.recognized_string != ")":
                self.error(")")
            self.get_token()

    def declaration_line(self):
        self.get_token()
        self.parse_id_element()    # JUNK CODE
        self.get_token()
        while self.current_token.recognized_string == ",":
            self.get_token()
            if self.current_token.family != "ID":
                self.error("ID")
            self.parse_id_element()
            self.get_token()

    def return_stat(self):
        self.get_token()
        self.expression()

    def if_stat(self, subprogram_id: str):
        self.get_token()
        (condition_true, condition_false) = self.condition()
        if self.current_token.recognized_string != ":":
            self.error(":")
        backpatch(condition_true, next_quad())
        if self.get_token().recognized_string == "#{":
            self.get_token()
            self.statements(subprogram_id)
            if self.get_token().recognized_string != "#}":
                self.error("#}")
            if_list = make_list(next_quad())
            gen_quad('jump', '_', '_', '_')
            backpatch(condition_false, next_quad())
        else:
            self.statement(subprogram_id)
            if_list = make_list(next_quad())
            gen_quad('jump', '_', '_', '_')
            backpatch(condition_false, next_quad())

        if self.current_token.recognized_string == "elif":
            self.get_token()
            (condition_true, condition_false) = self.condition()
            if self.current_token.recognized_string != ":":
                self.error(":")
            backpatch(condition_true, next_quad())
            token = self.get_token()
            if token.recognized_string == "#{":
                self.get_token()
                self.statements(subprogram_id)
                if_list = make_list(next_quad())
                gen_quad('jump', '_', '_', '_')
                if self.get_token().recognized_string != "#}":
                    self.error("#}")
                backpatch(if_list, next_quad())
            else:
                self.statement(subprogram_id)
                if_list = make_list(next_quad())
                gen_quad('jump', '_', '_', '_')
                backpatch(condition_false, next_quad())
        if self.current_token.recognized_string == "else":
            self.get_token()
            if self.current_token.recognized_string != ":":
                self.error(":")
            token = self.get_token()
            if token.recognized_string == "#{":
                self.get_token()
                self.statements(subprogram_id)
                if self.get_token().recognized_string != "#}":
                    self.error("#}")
                backpatch(if_list, next_quad())
            else:
                self.statement(subprogram_id)
                if_list = make_list(next_quad())
                gen_quad('jump', '_', '_', '_')
                backpatch(condition_false, next_quad())
        else:
            self.statement(subprogram_id)
            backpatch(if_list, next_quad())

    def while_stat(self, subprogram_id: str):
        self.get_token()
        cond_quad = next_quad()
        (condition_true, condition_false) = self.condition()
        backpatch(condition_true, next_quad())
        if self.current_token.recognized_string != ":":
            self.error(":")
        if self.get_token().recognized_string == "#{":
            self.get_token()
            self.statements(subprogram_id)
            if self.current_token.recognized_string != "#}":
                self.error("#}")
            self.get_token()
            gen_quad('jump', '_', '_', cond_quad)
            backpatch(condition_false, next_quad())
        else:
            self.statement(subprogram_id)
            gen_quad('jump', '_', '_', cond_quad)
            backpatch(condition_false, next_quad())

    def condition(self):
        (q1_true, q1_false) = self.bool_term()
        b_true = q1_true
        b_false = q1_false

        while self.current_token.recognized_string == "or":
            backpatch(b_false, next_quad())
            self.get_token()
            (q2_true, q2_false) = self.bool_term()
            b_true = merge_list(b_true, q2_true)
            b_false = q2_false
        return (b_true, b_false)

    def bool_term(self):
        (r1_true, r1_false) = self.bool_factor()
        q_true = r1_true
        q_false = r1_false

        while self.current_token.recognized_string == "and":
            backpatch(q_true, next_quad())
            self.get_token()
            (r2_true, r2_false) = self.bool_factor()
            q_false = merge_list(q_false, r2_false)
            q_true = r2_true
        return (q_true, q_false)

    def bool_factor(self):
        token = self.current_token
        if token.recognized_string == "not":                # bool_factor: ’not’ condition|
            self.get_token()                                #                   condition|
            (b_true, b_false) = self.condition()            #                   expression REL_OP expression
            r_true = b_false
            r_false = b_true
        elif self.next_token.recognized_string in ('!=', '<=', '>=', '>', '<', '==', "%"):
            e1 = self.expression()
            rel_op = self.current_token.recognized_string
            self.get_token()
            e2 = self.expression()
            r_true = make_list(next_quad())
            gen_quad(rel_op, e1, e2, '_')
            r_false = make_list(next_quad())
            gen_quad("jump", '_', '_', '_')
        elif self.next_token.recognized_string == "(":
            e1 = self.expression()
            rel_op = self.current_token.recognized_string
            self.get_token()
            e2 = self.expression()
            r_true = make_list(next_quad())
            gen_quad(rel_op, e1, e2, '_')
            r_false = make_list(next_quad())
            gen_quad("jump", '_', '_', '_')
        else:
            (b_true, b_false) = self.condition()
            r_true = b_true
            r_false = b_false

        return (r_true, r_false)

    def parse_id_element(self):
        if self.current_token.family == "ID":
            return
        else:
            raise Exception("Unexpected token. Expected ID got ", self.current_token.family, " instead in line:", self.current_token.line_number)

    def statements(self, subprogram_id: str):
        self.statement(subprogram_id)
        string = self.current_token.recognized_string
        while string == "print" or string == "return" or self.next_token.recognized_string == "=" or string == "while" or string == "if":
            if self.next_token.recognized_string == "=":
                self.statement(subprogram_id)
            else:
                self.statement(subprogram_id)
            string = self.current_token.recognized_string

    def statement(self, subprogram_id: str):
        string = self.current_token.recognized_string
        if string == "print" or string == "return" or self.next_token.recognized_string == "=":
            self.simple_statement(subprogram_id)
        elif string == "if" or string == "while":
            self.structured_statement(subprogram_id)
        else:
            raise Exception("Expected statement found:" + string)

    def assignment_stat(self, subprogram_id: str):
        # We assume current token is an ID and needs to be checked
        var_name = self.current_token.recognized_string

        # Ensure the current token is indeed an identifier
        if self.current_token.family != "ID":
            raise Exception(f"Expected variable name, but found {self.current_token.recognized_string}")

        # Ensure the variable is declared
        if not self.symbol_table.lookup(var_name):
            raise Exception(f"Undeclared variable {var_name}")

        self.get_token()  # Move to the next token which should be '='

        if self.current_token.recognized_string != "=":
            raise Exception(f"Expected '=', but found {self.current_token.recognized_string}")

        self.get_token()  # Move to the next token which should be the start of the expression
        source_expression = self.expression()
        gen_quad('=', source_expression, '_', var_name)

    def simple_statement(self, subprogram_id: str):
        if self.current_token.recognized_string == "print":
            self.print_stat()
        elif self.current_token.recognized_string == "return":
            self.return_stat()
        elif self.current_token.family == "ID" and self.next_token.recognized_string == "=":  # Ensure it's an identifier and followed by '='
            self.assignment_stat(subprogram_id)
        else:
            raise Exception(f"Unexpected token {self.current_token.recognized_string} in simple statement")


    def structured_statement(self, subprogram_id: str):
        if self.current_token.recognized_string == "if":
            self.if_stat(subprogram_id)
        elif self.current_token.recognized_string == "while":
            self.while_stat(subprogram_id)

    def print_stat(self):
        if self.next_token.recognized_string != "(":
            raise Exception("Unexpected token. Expected ( got ", self.next_token.recognized_string,
                            " instead in line:", self.current_token.line_number )
        self.get_token()
        self.get_token()
        self.expression()
        if self.current_token.recognized_string != ")":
            self.error(")")
        self.get_token()

    def id_tail(self):
        if self.current_token.recognized_string != "(":
            self.error("(")
        self.get_token()
        self.actual_par_list()
        if self.current_token.recognized_string == ")":
            self.get_token()

    def actual_par_list(self):
        expression_parameter = self.expression()
        gen_quad("par", expression_parameter, "cv", '_')
        while self.current_token.recognized_string == ",":
            self.get_token()
            expression_parameter = self.expression()
            gen_quad("par", expression_parameter, "cv", '_')

    def optional_sign(self):
        if self.current_token.family == "ADD_OPERATOR":
            return

    def expression(self):
        possible_left_term = self.current_token.recognized_string
        left_term = self.term()
        if left_term is None:
            left_term = possible_left_term
        while self.current_token.family == "ADD_OPERATOR":
            add_op = self.current_token.recognized_string
            possible_right_term = self.get_token().recognized_string
            right_term = self.term()
            if right_term is None:
                right_term = possible_right_term
            factor_temp = new_temp()
            gen_quad(add_op, left_term, right_term, factor_temp)
            left_term = factor_temp
        return left_term

    def term(self):
        possible_left_factor = self.current_token.recognized_string
        left_factor = self.factor()
        if left_factor is None:
            left_factor = possible_left_factor
        while self.current_token.family == "MUL_OPERATOR":
            mul_op = self.current_token.recognized_string
            possible_right_factor = self.get_token()
            right_factor = self.factor()
            if right_factor is None:
                right_factor = possible_right_factor
            term_temp = new_temp()
            gen_quad(mul_op, left_factor, right_factor, term_temp)
            left_factor = term_temp
        return left_factor

    def factor(self):
        token = self.current_token
        returned_expression = ""
        if token.recognized_string == "(":
            self.get_token()
            returned_expression = self.expression()
            if self.current_token.recognized_string == ")":
                self.get_token()
                return returned_expression
            return returned_expression
        elif token.family == "ID":
            id = self.current_token.recognized_string
            self.parse_id_element()
            self.get_token()
            if self.current_token.recognized_string == ")" and self.next_token.family in ["MUL_OPERATOR", "ADD_OPERATOR"]:
                self.get_token()
                return id
            if self.current_token.recognized_string == "(":
                is_subprogram = self.id_tail()
                if is_subprogram:
                    returned_value = new_temp()
                    gen_quad("par", returned_value, "ret", '_')
                    return returned_value
            return id

        elif token.family == "NUMBER":
            returned_int = self.current_token.recognized_string
            self.get_token()
            return returned_int

        elif self.next_token.family == "NUMBER" and token.recognized_string == "-":
            self.get_token()
            returned_int = self.current_token.recognized_string
            self.get_token()
            return returned_int

        else:
            raise Exception("Unexpected token. Expected factor got ", self.current_token.family, " instead in line:",
                            self.current_token.line_number)

    def get_token(self):
        self.current_token = self.next_token
        self.next_token = self.lexer.lexical_analyzer()
        return self.current_token

    def error(self, expected: str):
        raise Exception("Unexpected token. Expected " + expected + " but got " + self.current_token.recognized_string + " in line: " + str(self.current_token.line_number))


class Entity:
    def __init__(self, name: str):
        self.name = name


class Variable(Entity):
    def __init__(self, name: str, datatype, offset: int):
        super().__init__(name)
        self.datatype = datatype
        self.offset = offset

    def __str__(self):
        return f"{self.name}, {self.datatype}, {self.offset}"


class Function(Entity):
    def __init__(self, name: str, starting_quad, datatype, formal_parameters: list, frame_length: int):
        super().__init__(name)
        self.starting_quad = starting_quad
        self.formal_parameters = formal_parameters
        self.framelength = frame_length
        self.datatype = datatype

    def __str__(self):
        return f"{self.name}, {self.starting_quad}, {self.datatype}, {self.framelength}"


def create_int_file():
    with open('test.int', 'w', encoding='utf-8') as int_code_file:
        for q, q_label in all_quads.items():
            int_code_file.write(str(q_label) + ": " + str(q) + '\n')


def new_temp():
    global temp_var_num
    new_temp_id = "T_" + str(temp_var_num)
    temp_var_num += 1
    return new_temp_id


def next_quad():
    return label


def gen_quad(op, oprnd1, oprnd2, target):
    global label, all_quads
    quad = Quad(op, oprnd1, oprnd2, target)
    all_quads[quad] = label
    label += 1


def make_list(label):
    return [label]


def merge_list(list1, list2):
    return list1 + list2


def backpatch(lst, label):
    global all_quads
    for q, q_label in all_quads.items():
        if q_label in lst:
            q.target = label


class Quad:
    def __init__(self, op, oprnd1, oprnd2, target):
        self.op = op
        self.oprnd1 = oprnd1
        self.oprnd2 = oprnd2
        self.target = target

    def __str__(self):
        return str(self.op) + ", " + str(self.oprnd1) + ", " + str(self.oprnd2) + ", " + str(self.target)


def add_variable_records(name, datatype, offset):
    record = {
        'name': name,
        'datatype': datatype,
        'offset': offset
    }
    allVariableRecords.append(record)


def load(v, reg):
    global voffset

    for var in allVariableRecords:
        if var['name'] == v:
            voffset = var['offset']

    if str(v).isdigit():
        final_file.write('li {} , {}\n'.format(reg, int(v)))
    else:
        final_file.write('lw {} ,{}($gp)\n'.format(reg, -voffset))

    final_file.flush()


def store(reg, v):
    global voffset

    for var in allVariableRecords:
        if var['name'] == v:
            voffset = var['offset']
    final_file.write('sw {} ,{}($gp)\n'.format(reg, -voffset))

    final_file.flush()


def create_asm_file(quad, quad_num):
    global halt_label

    num_op = ('+', '-', '*', '/')
    num_op_riscv = ('add', 'sub', 'mul', 'div')

    rel_op = ('==', '!=', '<', '>', '<=', '>=')
    rel_op_riscv = ('beq', 'bne', 'blt', 'bge', 'ble', 'bge')

    if quad.op == "halt":
        halt_label = quad_num

    if quad_num == 1:
        final_file.write('\n' * 25)  # padding.

    final_file.write('L_' + str(quad_num) + ':\n')

    if quad.op == "jump":
        if quad.target != '_':
            final_file.write('j L_{} \n'.format(int(quad.target)))
        else:
            final_file.write('j _\n')

    elif quad.op == "halt":
        final_file.write("li a0, 0 \n")
        final_file.write("li a7, 10 \n")
        final_file.write("ecall \n")

    elif quad.op == 'begin_block':
        final_file.write('sw ra, 0(sp)\n')
        final_file.write('addi sp, sp, -4\n')
        final_file.seek(0, 0)
        final_file.write(".data\n")
        final_file.write("str_nl: .asciz " + '"\\n" \n')
        final_file.write(".text\n")
        final_file.write('j L_{} \n'.format(quad_num))
        final_file.seek(0, 2)

    elif quad.op == 'end_block':
        final_file.write('j L_{} \n'.format(halt_label))

    elif quad.op in num_op:
        ret_op = num_op_riscv[num_op.index(quad.op)]
        load(quad.oprnd1, 't1')
        load(quad.oprnd2, 't2')
        final_file.write(f'{ret_op} t1, t1, t2 \n')
        store('t1', quad.target)

    elif quad.op == "=":
        load(quad.oprnd1, 't1')
        store('t1', quad.target)

    elif quad.op in rel_op:
        ret_op = rel_op_riscv[rel_op.index(quad.op)]
        load(quad.oprnd1, 't1')
        load(quad.oprnd2, 't2')
        final_file.write(f'{ret_op} t1, t2, L_{int(quad.target) if quad.target != "_" else "_"} \n')

    elif quad.op == "in":
        final_file.write('li a7, 5\n')
        final_file.write('ecall\n')

    elif quad.op == "out":
        load(quad.oprnd1, 'a0')
        final_file.write('li a7, 1\n')
        final_file.write('ecall \n')
        final_file.write('la a0, str_nl\n')
        final_file.write('li a7, 4\n')
        final_file.write('ecall \n')

    elif quad.op == "ret":
        load(quad.oprnd1, 't1')
        final_file.write('lw t0, -8(sp)\n')
        final_file.write('sw t1, 0(t0)\n')

    final_file.flush()


def main():
    global final_file
    global symbol_table

    tokens = []

    lexer = Lexer()
    token = lexer.lexical_analyzer()

    tokens.append(token)

    print("Token family:" + token.family + " Token recognized_string:" + token.recognized_string + " Token line:" + str(
        token.line_number) + " Token number is:" + str(token.token_number))
    while token.family != "EOF":
        token = lexer.lexical_analyzer()
        print("Token family:" + token.family + " Token recognized_string:" + token.recognized_string + " Token line:" + str(
            token.line_number) + " Token number is:" + str(token.token_number))
        tokens.append(token)

    final_file = open("test.asm", "w+")

    symbol_table = SymbolTable()
    Parser(lexer,symbol_table)

    create_int_file()
    for quad, quad_num in all_quads.items():
        create_asm_file(quad, quad_num + 1)


if __name__ == "__main__":
    main()