import sys
#ANASTASIOS PAPAGEWRGIOU AM:4758 cse94758
#VASILEIOS PAPADIMITRIOU AM:4759 cse94759


label = 1
temp_var_num = 1  # temporary variable counter.
current_subprogram = []
program_name = ""
all_quads = {}


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
        filepath = input("Give me the file's path: ")
        #filepath = "C:\\Users\\srig\\Desktop\\Uni\\compiler\\test.cpy"
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


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currentToken = self.lexer.lexical_analyzer()
        self.nextToken = self.lexer.lexical_analyzer()
        self.looper()

    def program(self):
        global program_name
        program_name = self.nextToken.recognized_string
        print("Program '" + program_name + "' has started.")
        if self.currentToken.recognized_string == "def":
            self.def_function(program_name)
        elif self.currentToken.recognized_string == "#def":
            self.def_main_function(program_name)
        else:
            self.error("def")

    def looper(self):
        while self.currentToken.recognized_string == "def" or self.currentToken.recognized_string == "#def":
            self.program()
        if self.currentToken.recognized_string == "EOF":
            print("\nParsing ended successfully.")

    def def_main_function(self, subprogramID: str):
        if self.currentToken.family == "KEYWORD" and self.currentToken.recognized_string == "#def":
            if self.get_token().recognized_string != "main":
                self.error("main")
            self.get_token()
            self.declarations(subprogramID)
            self.globals(subprogramID)
            self.statements(subprogramID)

    def def_function(self, subprogramID: str):
        global current_subprogram
        if self.currentToken.family != "KEYWORD" and self.currentToken.recognized_string != "def":
            self.error("def")
        self.get_token()

        subprogramID = self.currentToken.recognized_string
        current_subprogram = subprogramID

        self.parse_id_element()
        if self.get_token().recognized_string != "(":
            self.error("(")
        self.get_token()
        self.id_list()
        if self.get_token().recognized_string != ":":
            self.error(":")
        if self.get_token().recognized_string != "#{":
            self.error("#{")
        self.get_token()
        self.globals(subprogramID)
        self.declarations(subprogramID)

        genQuad("begin_block", subprogramID, '_', '_')

        while True:
            if self.currentToken.recognized_string == "#int":
                self.declarations(subprogramID)
            if self.currentToken.recognized_string == "def":
                self.def_function(subprogramID)
            if self.currentToken.recognized_string == "global":
                self.globals(subprogramID)
            if self.currentToken.family == "ID":
                self.statements(subprogramID)
            else:
                break

        genQuad("halt", '_', '_', '_')
        genQuad('end_block', subprogramID, '_', '_')

        if self.currentToken.recognized_string != "#}":
            self.error("#}")
        if self.currentToken.recognized_string == "#}":
            self.get_token()

    def globals(self, subprogramID: str):
        while self.currentToken.recognized_string == "global":
            if self.nextToken.family != "ID":
                raise Exception("Unexpected token. Expected ID got ", self.nextToken.family, " instead in line:",
                                self.nextToken.line_number)
            self.get_token()
            self.id_list()

    def declarations(self, subprogramID: str):
        while self.currentToken.recognized_string == "#int":
            if self.nextToken.family != "ID":
                raise Exception("Unexpected token. Expected ID got ", self.nextToken.family, " instead in line:", self.nextToken.line_number)
            self.get_token()
            self.id_list()

    def id_list(self):
        global main_func_declared_vars, offset
        self.parse_id_element()
        while self.nextToken.recognized_string == ",":
            self.get_token()
            self.get_token()
            if self.currentToken.recognized_string == ")":
                break
            self.parse_id_element()
        self.get_token()

    def declaration_line(self):
        self.get_token()
        self.parse_id_element()    #JUNK CODE
        self.get_token()
        while self.currentToken.recognized_string == ",":
            self.get_token()
            if self.currentToken.family != "ID":
                self.error("ID")
            self.parse_id_element()
            self.get_token()

    def return_stat(self):
        self.get_token()
        self.expression()

    def if_stat(self, subprogramID: str):
        self.get_token()
        (condition_True, condition_False) = self.condition()
        if self.currentToken.recognized_string != ":":
            self.error(":")
        backpatch(condition_True, nextQuad())
        if self.get_token().recognized_string == "#{":
            self.get_token()
            self.statements(subprogramID)
            if self.get_token().recognized_string != "#}":
                self.error("#}")
            ifList = makeList(nextQuad())
            genQuad('jump', '_', '_', '_')
            backpatch(condition_False,nextQuad())
        else:
            self.statement(subprogramID)
            ifList = makeList(nextQuad())
            genQuad('jump', '_', '_', '_')
            backpatch(condition_False,nextQuad())

        if self.currentToken.recognized_string == "elif":
            self.get_token()
            (condition_True, condition_False) = self.condition()
            if self.currentToken.recognized_string != ":":
                self.error(":")
            backpatch(condition_True, nextQuad())
            token = self.get_token()
            if token.recognized_string == "#{":
                self.get_token()
                self.statements(subprogramID)
                ifList = makeList(nextQuad())
                genQuad('jump', '_', '_', '_')
                if self.get_token().recognized_string != "#}":
                    self.error("#}")
                backpatch(ifList, nextQuad())
            else:
                self.statement(subprogramID)
                ifList = makeList(nextQuad())
                genQuad('jump', '_', '_', '_')
                backpatch(condition_False,nextQuad())
        if self.currentToken.recognized_string == "else":
            self.get_token()
            if self.currentToken.recognized_string != ":":
                self.error(":")
            token = self.get_token()
            if token.recognized_string == "#{":
                self.get_token()
                self.statements(subprogramID)
                if self.get_token().recognized_string != "#}":
                    self.error("#}")
                backpatch(ifList, nextQuad())
            else:
                self.statement(subprogramID)
                ifList = makeList(nextQuad())
                genQuad('jump', '_', '_', '_')
                backpatch(condition_False,nextQuad())
        else:
            self.statement(subprogramID)
            backpatch(ifList, nextQuad())

    def while_stat(self,subprogramID: str):
        self.get_token()
        condQuad = nextQuad()
        (condition_True, condition_False) = self.condition()
        backpatch(condition_True, nextQuad())
        if self.currentToken.recognized_string != ":":
            self.error(":")
        if self.get_token().recognized_string == "#{":
            self.get_token()
            self.statements(subprogramID)
            if self.currentToken.recognized_string != "#}":
                self.error("#}")
            self.get_token()
            genQuad('jump', '_', '_', condQuad)
            backpatch(condition_False, nextQuad())
        else:
            self.statement(subprogramID)
            genQuad('jump', '_', '_', condQuad)
            backpatch(condition_False, nextQuad())

    def condition(self):
        (Q1_True, Q1_False) = self.bool_term()
        B_True = Q1_True
        B_False = Q1_False

        while self.currentToken.recognized_string == "or":
            backpatch(B_False, nextQuad())
            self.get_token()
            (Q2_True, Q2_False) = self.bool_term()
            B_True = mergeList(B_True, Q2_True)
            B_False = Q2_False
        return (B_True, B_False)

    def bool_term(self):
        (R1_True, R1_False) = self.bool_factor()
        Q_True = R1_True
        Q_False = R1_False

        while self.currentToken.recognized_string == "and":
            backpatch(Q_True, nextQuad())
            self.get_token()
            (R2_True, R2_False) = self.bool_factor()
            Q_False = mergeList(Q_False, R2_False)
            Q_True = R2_True
        return (Q_True, Q_False)

    def bool_factor(self):
        token = self.currentToken
        if token.recognized_string == "not":                #bool_factor: ’not’ condition|
            self.get_token()                                #                   condition|
            (B_True, B_False) = self.condition()            #                   expression REL_OP expression
            R_True = B_False
            R_False = B_True
        elif self.nextToken.recognized_string in ('!=', '<=', '>=', '>', '<', '==', "(", "%"):
            E1 = self.expression()
            rel_op = self.currentToken.recognized_string
            self.get_token()
            E2 = self.expression()
            R_True = makeList(nextQuad())
            genQuad(rel_op, E1, E2, '_')
            R_False = makeList(nextQuad())
            genQuad("jump", '_', '_', '_')
        else:
            (B_True, B_False) = self.condition()
            R_True = B_True
            R_False = B_False

        return (R_True, R_False)

    def parse_id_element(self):
        if self.currentToken.family == "ID":
            return
        else:
            raise Exception("Unexpected token. Expected ID got ", self.currentToken.family, " instead in line:", self.currentToken.line_number)

    def statements(self, subprogramID: str):
        self.statement(subprogramID)
        string = self.currentToken.recognized_string
        while string == "print" or string == "return" or self.nextToken.recognized_string == "=" or string == "while" or string == "if":
            if self.nextToken.recognized_string == "=":
                self.statement(subprogramID)
            else:
                self.statement(subprogramID)
            string = self.currentToken.recognized_string

    def statement(self,subprogramID: str):
        string = self.currentToken.recognized_string
        if string == "print" or string == "return" or self.nextToken.recognized_string == "=":
            self.simple_statement(subprogramID)
        elif string == "if" or string == "while":
            self.structured_statement(subprogramID)
        else:
            raise Exception("Expected statement found:"+ string)

    def simple_statement(self, subprogramID: str):
        if self.currentToken.recognized_string == "print":
            self.print_stat()
        if self.currentToken.recognized_string == "return":
            self.return_stat()
        elif self.nextToken.recognized_string == "=":
            self.assignment_stat(subprogramID)

    def assignment_stat(self, subprogramID: str):
        self.get_token()
        self.get_token()
        if self.currentToken.recognized_string == "int":
            if self.get_token().recognized_string != "(":
                self.error("(")
            if self.get_token().recognized_string != "input":
                self.error("input")
            if self.get_token().recognized_string != "(":
                self.error("(")
            if self.get_token().recognized_string != ")":
                self.error(")")
            if self.get_token().recognized_string != ")":
                self.error(")")
            genQuad("in", subprogramID, '_', '_')
            self.get_token()
        else:
            source_expression = self.expression()
            genQuad('=', source_expression, '_', subprogramID)

    def structured_statement(self, subprogramID: str):
        if self.currentToken.recognized_string == "if":
            self.if_stat(subprogramID)
        elif self.currentToken.recognized_string == "while":
            self.while_stat(subprogramID)

    def print_stat(self):
        if self.nextToken.recognized_string != "(":
            raise Exception("Unexpected token. Expected ( got ", self.nextToken.recognized_string,
                            " instead in line:", self.currentToken.line_number )
        self.get_token()
        self.get_token()
        self.expression()
        if self.currentToken.recognized_string != ")":
            self.error(")")
        self.get_token()

    def id_tail(self):
        if self.currentToken.recognized_string != "(":
            self.error("(")
        self.get_token()
        self.actual_par_list()
        if self.currentToken.recognized_string == ")":
            self.get_token()

    def actual_par_list(self):
        expression_parameter = self.expression()
        genQuad("par", expression_parameter, "cv", '_')
        while self.currentToken.recognized_string == ",":
            self.get_token()
            expression_parameter = self.expression()
            genQuad("par", expression_parameter, "cv", '_')

    def optional_sign(self):
        if self.currentToken.family == "ADD_OPERATOR":
            return

    def expression(self):
        possible_left_term = self.currentToken.recognized_string
        left_term = self.term()
        if left_term is None:
            left_term = possible_left_term
        while self.currentToken.family == "ADD_OPERATOR":
            add_op = self.currentToken.recognized_string
            possible_right_term = self.get_token().recognized_string
            right_term = self.term()
            if right_term is None:
                right_term = possible_right_term
            factor_temp = newTemp()
            genQuad(add_op, left_term, right_term, factor_temp)
            left_term = factor_temp
        return left_term

    def term(self):
        possible_left_factor = self.currentToken.recognized_string
        left_factor = self.factor()
        if left_factor is None:
            left_factor = possible_left_factor
        while self.currentToken.family == "MUL_OPERATOR":
            mul_op = self.currentToken.recognized_string
            possible_right_factor = self.get_token()
            right_factor = self.factor()
            if right_factor is None:
                right_factor = possible_right_factor
            term_temp = newTemp()
            genQuad(mul_op, left_factor, right_factor, term_temp)
            left_factor = term_temp
        return left_factor

    def factor(self):
        token = self.currentToken
        returned_expression = ""
        if token.recognized_string == "(":
            self.get_token()
            returned_expression = self.expression()
            if self.currentToken.recognized_string == ")":
                self.get_token()
                return returned_expression
        elif token.family == "ID":
            self.parse_id_element()
            self.get_token()
            if self.currentToken.recognized_string == ")" and self.nextToken.family in ["MUL_OPERATOR", "ADD_OPERATOR"]:
                self.get_token()
            if self.currentToken.recognized_string == "(":
                is_subprogram = self.id_tail()
                if is_subprogram:
                    returned_value = newTemp()
                    genQuad("par", returned_value, "ret", '_')
                    return returned_value

        elif token.family == "NUMBER":
            returned_int = self.currentToken.recognized_string
            self.get_token()
            return returned_int

        elif self.nextToken.family == "NUMBER" and token.recognized_string == "-":
            self.get_token()
            returned_int = self.currentToken.recognized_string
            self.get_token()
            return returned_int

        else:
            raise Exception("Unexpected token. Expected factor got ", self.currentToken.family, " instead in line:",
                            self.currentToken.line_number)

    def get_token(self):
        print(self.currentToken.recognized_string)
        self.currentToken = self.nextToken
        self.nextToken = self.lexer.lexical_analyzer()
        return self.currentToken

def error(self, expected: str):
    raise Exception("Unexpected token. Expected " + expected + " but got " + self.currentToken.recognized_string + " in line: " + str(self.currentToken.line_number))

def create_int_file():
    with open('test.int', 'w', encoding='utf-8') as int_code_file:
        for q, q_label in all_quads.items():
            int_code_file.write(str(q_label) + ": " + str(q) + '\n')

def newTemp():
    # T_1, T_2, ..., T_n
    global temp_var_num
    new_tempID = "T_" + str(temp_var_num)
    temp_var_num += 1
    return new_tempID

def nextQuad():
    return label

def genQuad(op, oprnd1, oprnd2, target):
    global label, all_quads

    quad = Quad(op, oprnd1, oprnd2, target)

    all_quads[quad] = label

    label += 1

def makeList(label):
    return [label]


def mergeList(list1, list2):
    return list1 + list2


# assigns label to target field of quads with label in list
def backpatch(list, label):
    global all_quads

    for q, q_label in all_quads.items():
        if q_label in list:
            q.target = label  # set q's 4th field to label




class Quad:
    def __init__(self, op, oprnd1, oprnd2, target):
        self.op = op
        self.oprnd1 = oprnd1
        self.oprnd2 = oprnd2
        self.target = target

    def __str__(self):
        return str(self.op) + ", " + str(self.oprnd1) + ", " + str(self.oprnd2) + ", " + str(self.target)




def main():

    tokens = []

    lexer = Lexer()
    token = lexer.lexical_analyzer()

    tokens.append(token)

    print("Token family:" + token.family + " Token recognized_string:" + token.recognized_string + " Token line:" + str(
        token.line_number) + " Token number is:" + str(token.token_number))
    while token.family != "EOF":
        token = lexer.lexical_analyzer()
        print("Token family:"+token.family + " Token recognized_string:" + token.recognized_string + " Token line:" + str(token.line_number) + " Token number is:" + str(token.token_number))
        tokens.append(token)
    Parser(lexer)
    create_int_file()


if __name__ == "__main__":
    main()
