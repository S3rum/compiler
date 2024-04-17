import sys
#ANASTASIOS PAPAGEWRGIOU AM:4758
#VASILEIOS PAPADIMITRIOU AM:4759


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
                print("Unexpected token in line: ",self.current_line)
                sys.exit()


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.currentToken = self.lexer.lexical_analyzer()
        self.nextToken = self.lexer.lexical_analyzer()
        self.looper()

    def def_main_function(self):
        if self.currentToken.family == "KEYWORD" and self.currentToken.recognized_string == "#def":
            if self.get_token().recognized_string != "main":
                raise Exception("Unexpected token. Expected main")
            self.get_token()
            self.declarations()
            self.globals()
            self.statements()

    def globals(self):
        while self.currentToken.recognized_string == "global":
            if self.nextToken.family != "ID":
                raise Exception("Unexpected token. Expected ID got ", self.nextToken.family, " instead in line:",
                                self.nextToken.line_number)
            self.declaration_line()

    def looper(self):
        self.declarations()
        while self.currentToken.recognized_string == "def":
            self.def_function()
        while self.currentToken.recognized_string == "#def":
            self.def_main_function()
        if self.currentToken.recognized_string == "EOF":
            print("\nParsing ended successfully.")

    def def_function(self):
        if self.currentToken.family != "KEYWORD" and self.currentToken.recognized_string == "def":
            raise Exception("Unexpected token. Expected def got ", self.currentToken.family, " instead in line:",
                            self.currentToken.line_number)
        self.get_token()
        self.parse_id_element()
        if self.get_token().recognized_string != "(":
            raise Exception("Unexpected token. Expected ( got ", self.currentToken.family, " instead in line:",
                            self.currentToken.line_number)
        self.get_token()
        self.id_list()
        if self.get_token().recognized_string != ":":
            raise Exception("Unexpected token. Expected : got ", self.currentToken.family, " instead in line:",
                            self.currentToken.line_number)
        if self.get_token().recognized_string != "#{":
            raise Exception("Unexpected token. Expected #{ got ", self.currentToken.recognized_string, " instead in line:",
                            self.currentToken.line_number)
        self.get_token()
        self.declarations()
        while self.currentToken.recognized_string == "def":
            self.def_function()
        self.globals()

        self.statements()
        if self.currentToken.recognized_string != "#}":
            raise Exception("Unexpected token. Expected #} got ", self.currentToken.recognized_string,
                            " instead in line:",
                            self.currentToken.line_number)
        if self.currentToken.recognized_string == "#}":
            self.get_token()

    def return_stat(self):
        self.get_token()
        self.expression()

    def if_stat(self):
        self.get_token()
        self.condition()
        if self.currentToken.recognized_string != ":":
            raise Exception("Unexpected token. Expected : got ", self.currentToken.family, " instead in line:", self.currentToken.line_number)
        if self.get_token().recognized_string == "#{":
            self.get_token()
            self.statements()
            if self.get_token().recognized_string != "#}":
                raise Exception("Unexpected token. Expected : got ", self.currentToken.family, " instead in line:", self.currentToken.line_number)
        else:
            self.statement()

        if self.currentToken.recognized_string == "elif":
            self.get_token()
            self.condition()
            self.elif_stat()

        if self.currentToken.recognized_string == "else":
            self.get_token()
            self.elif_stat()

    def elif_stat(self):
        if self.currentToken.recognized_string != ":":
            raise Exception("Unexpected token. Expected : got ", self.currentToken.family, " instead in line:",
                            self.currentToken.line_number)
        token = self.get_token()
        if token.recognized_string == "#{":
            self.get_token()
            self.statements()
            if self.get_token().recognized_string != "#}":
                raise Exception("Unexpected token. Expected : got ", self.currentToken.family, " instead in line:",
                                self.currentToken.line_number)
        else:
            self.statement()

    def while_stat(self):
        self.get_token()
        self.condition()
        if self.currentToken.recognized_string != ":":
            raise Exception("Unexpected token. Expected : got ", self.currentToken.family, " instead in line:", self.currentToken.line_number)
        if self.get_token().recognized_string == "#{":
            self.get_token()
            self.statements()
            if self.currentToken.recognized_string != "#}":
                raise Exception("Unexpected token. Expected : got ", self.currentToken.family, " instead in line:", self.currentToken.line_number)
            self.get_token()
        else:
            self.statement()

    def condition(self):
        self.bool_term()
        while self.currentToken.recognized_string == "or":
            self.get_token()
            self.bool_term()

    def bool_term(self):
        self.bool_factor()
        while self.currentToken.recognized_string == "and":
            self.get_token()
            self.bool_factor()

    def bool_factor(self):
        token = self.currentToken
        if token.recognized_string == "not":
            self.get_token()
            self.condition()
        self.expression()
        if self.currentToken.family == "COMPARATOR":  # maybe change > < klp se REL_OP gia na jexwrizei apo ta =
            self.get_token()
            self.expression()

    def declarations(self):
        while self.currentToken.recognized_string == "#int":
            if self.nextToken.family != "ID":
                raise Exception("Unexpected token. Expected ID got ", self.nextToken.family, " instead in line:", self.nextToken.line_number)
            self.declaration_line()

    def declaration_line(self):
        self.get_token()
        self.parse_id_element()
        self.get_token()
        while self.currentToken.recognized_string == ",":
            self.get_token()
            if self.currentToken.family != "ID":
                raise Exception("Unexpected token. Expected ID got ", self.currentToken.family, " instead in line:",
                                self.currentToken.line_number)
            self.parse_id_element()
            self.get_token()

    def id_list(self):
        while True:
            self.parse_id_element()
            self.get_token()
            if self.currentToken.recognized_string == ")":
                break
            elif self.currentToken.recognized_string != ",":
                raise Exception("Unexpected token. Expected , got ", self.currentToken.family, " instead in line:",
                                self.currentToken.line_number)
            self.get_token()

    def parse_id_element(self):
        if self.currentToken.family == "ID":
            return
        else:
            raise Exception("Unexpected token. Expected ID got ", self.currentToken.family, " instead in line:", self.currentToken.line_number)

    def statements(self):
        self.statement()
        string = self.currentToken.recognized_string
        while string == "print" or string == "return" or self.nextToken.recognized_string == "=" or string == "while" or string == "if":
            if self.nextToken.recognized_string == "=":
                self.statement()
            else:
                self.statement()
            string = self.currentToken.recognized_string

    def statement(self):
        string = self.currentToken.recognized_string
        if string == "print" or string == "return" or self.nextToken.recognized_string == "=":
            self.simple_statement()
        elif string == "if" or string == "while":
            self.structured_statement()
        else:
            raise Exception("Expected statement found:", string)

    def simple_statement(self):
        if self.currentToken.recognized_string == "print":
            self.print_stat()
        if self.currentToken.recognized_string == "return":
            self.return_stat()
        elif self.nextToken.recognized_string == "=":
            self.assignment_stat()

    def assignment_stat(self):
        self.get_token()
        self.get_token()
        if self.currentToken.recognized_string == "int":
            if self.get_token().recognized_string != "(":
                raise Exception("Unexpected token. Expected ( got ", self.currentToken.recognized_string,
                                " instead in line:", self.currentToken.line_number)
            if self.get_token().recognized_string != "input":
                raise Exception("Unexpected token. Expected ( got ", self.currentToken.recognized_string,
                                " instead in line:", self.currentToken.line_number)
            if self.get_token().recognized_string != "(":
                raise Exception("Unexpected token. Expected ( got ", self.currentToken.recognized_string,
                                " instead in line:", self.currentToken.line_number)
            if self.get_token().recognized_string != ")":
                raise Exception("Unexpected token. Expected ( got ", self.currentToken.recognized_string,
                                " instead in line:", self.currentToken.line_number)
            if self.get_token().recognized_string != ")":
                raise Exception("Unexpected token. Expected ) got ", self.currentToken.recognized_string,
                                " instead in line:", self.currentToken.line_number)
            self.get_token()
        else:
            self.expression()

    def structured_statement(self):
        if self.currentToken.recognized_string == "if":
            self.if_stat()
        elif self.currentToken.recognized_string == "while":
            self.while_stat()

    def print_stat(self):
        if self.nextToken.recognized_string != "(":
            raise Exception("Unexpected token. Expected ( got ", self.nextToken.recognized_string,
                            " instead in line:", self.currentToken.line_number)
        self.get_token()
        self.get_token()
        self.expression()
        if self.currentToken.recognized_string != ")":
            raise Exception("Unexpected token. Expected ) got ", self.currentToken.recognized_string,
                            " instead in line:", self.currentToken.line_number)
        self.get_token()

    def id_tail(self):
        if self.currentToken.recognized_string != "(":
            raise Exception("Unexpected token. Expected ) got ", self.currentToken.family, " instead in line:", self.currentToken.line_number)
        self.get_token()
        self.actual_par_list()
        if self.currentToken.recognized_string == ")":
            self.get_token()

    def actual_par_list(self):
        self.expression()
        while self.currentToken.recognized_string == ",":
            self.get_token()
            self.expression()

    def optional_sign(self):
        if self.currentToken.family == "ADD_OPERATOR":
            return

    def expression(self):
        self.term()
        while self.currentToken.family == "ADD_OPERATOR":
            self.get_token()
            self.term()

    def term(self):
        self.factor()
        while self.currentToken.family == "MUL_OPERATOR":
            self.get_token()
            self.factor()

    def factor(self):
        token = self.currentToken
        if token.recognized_string == "(":
            self.get_token()
            self.expression()
        elif token.family == "ID":
            self.parse_id_element()
            self.get_token()
            if self.currentToken.recognized_string == ")" and self.nextToken.family in ["MUL_OPERATOR", "ADD_OPERATOR"]:
                self.get_token()
            if self.currentToken.recognized_string == "(":
                self.id_tail()
        elif token.family == "NUMBER":
            self.get_token()
        elif self.nextToken.family == "NUMBER" and token.recognized_string == "-":
            self.get_token()
            self.get_token()
        else:
            raise Exception("Unexpected token. Expected factor got ", self.currentToken.family, " instead in line:",
                            self.currentToken.line_number)

    def get_token(self):
        print(self.currentToken.recognized_string)
        self.currentToken = self.nextToken
        self.nextToken = self.lexer.lexical_analyzer()
        return self.currentToken


class Quad:

  def __init__(self, op, arg1, arg2, result):
    """
    Initializes a Quad object.

    Args:
      op: The operation of the quad (e.g., "+", "*").
      arg1: The first operand (can be a variable name, constant, or None).
      arg2: The second operand (can be a variable name, constant, or None).
      result: The variable where the result is stored.
    """
    self.op = op
    self.arg1 = arg1
    self.arg2 = arg2
    self.result = result

  def __str__(self):
    """
    Returns a string representation of the quad in a human-readable format.
    """
    if self.arg2 is None:
      return f"{self.result} = {self.op} {self.arg1}"
    else:
      return f"{self.result} = {self.arg1} {self.op} {self.arg2}"


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


if __name__ == "__main__":
    main()
