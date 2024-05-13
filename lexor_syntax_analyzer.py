import sys
#ANASTASIOS PAPAGEWRGIOU AM:4758
#VASILEIOS PAPADIMITRIOU AM:4759

label = 1
temp_var_num = 1  # temporary variable counter.
main_func_declared_vars = []
symbol_table = []
current_subprogram = []
program_name = ""
starter_function = ""
all_quads = {}
startingOffset = 12
allVariableRecords = []


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
        filepath = "C:\\Users\\tasos\\PycharmProjects\\compiler\\test.cpy"
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
            self.globals()
            self.statements()

    def error(self, expected: str):
        raise Exception("Unexpected token. Expected " + expected + " but got " + self.currentToken.recognized_string + " in line: " + str(self.currentToken.line_number))

    def def_function(self, subprogramID: str):
        global current_subprogram
        if self.currentToken.family != "KEYWORD" and self.currentToken.recognized_string != "def":
            self.error("def")
        self.get_token()
        starter_function = self.currentToken.recognized_string
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

        start_quad = nextQuad()
        genQuad("begin_block", subprogramID, "_", "_")
        while True:
            if self.get_token().recognized_string == "#int":
                self.declarations(subprogramID)
            if self.get_token().recognized_string == "def":
                self.def_function(subprogramID)
            if self.get_token().recognized_string == "global":
                self.globals(subprogramID)
            else:
                break
        self.globals()

        self.statements()
        if self.currentToken.recognized_string != "#}":
            self.error("#}")
        if self.currentToken.recognized_string == "#}":
            self.get_token()

    def globals(self, subprogramID: str):

        global main_func_del

        while self.currentToken.recognized_string == "global":
            if self.nextToken.family != "ID":
                raise Exception("Unexpected token. Expected ID got ", self.nextToken.family, " instead in line:",
                                self.nextToken.line_number)
            self.declaration_line()

    def declarations(self, subprogramID: str):

        global main_func_declared_vars, startingOffset

        while self.currentToken.recognized_string == "#int":
            if self.nextToken.family != "ID":
                raise Exception("Unexpected token. Expected ID got ", self.nextToken.family, " instead in line:", self.nextToken.line_number)
            main_func_declared_vars.append(self.get_token())
            self.id_list(subprogramID)
            offset = startingOffset
            for var in main_func_declared_vars:
                isDeclared = Variable(var, "int", offset)
                offset += 4
                add_variable_records(isDeclared.name, isDeclared.datatype, isDeclared.offset)

    def id_list(self):

        global main_func_declared_vars, subprogramID, offset

        self.get_token()

        while True:
            self.parse_id_element()
            self.get_token()
            if self.currentToken.recognized_string == ")":
                break
            elif self.currentToken.recognized_string != ",":
                raise Exception(",")
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

    def if_stat(self):
        self.get_token()
        self.condition()
        if self.currentToken.recognized_string != ":":
            self.error(":")
        if self.get_token().recognized_string == "#{":
            self.get_token()
            self.statements()
            if self.get_token().recognized_string != "#}":
                self.error("#}")
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
            self.error(":")
        token = self.get_token()
        if token.recognized_string == "#{":
            self.get_token()
            self.statements()
            if self.get_token().recognized_string != "#}":
                self.error("#}")
        else:
            self.statement()

    def while_stat(self):
        self.get_token()
        self.condition()
        if self.currentToken.recognized_string != ":":
            self.error(":")
        if self.get_token().recognized_string == "#{":
            self.get_token()
            self.statements()
            if self.currentToken.recognized_string != "#}":
                self.error("#}")
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
                self.error("(")
            if self.get_token().recognized_string != "input":
                self.error("input")
            if self.get_token().recognized_string != "(":
                self.error("(")
            if self.get_token().recognized_string != ")":
                self.error(")")
            if self.get_token().recognized_string != ")":
                self.error(")")
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




def newTemp():
    # T_1, T_2, ..., T_n
    global temp_var_num
    new_tempID = "T_" + str(temp_var_num)
    temp_var_num += 1

    if len(symbol_table) > 1 :

        offset = getRecord(current_subprogram[-1]).framelength

        declared_temp_var = TemporaryVariable(new_tempID, "int", offset)
        addRecordToCurrentLevel(declared_temp_var)
        updateField(getRecord(current_subprogram[-1]), 4)

    else:
        offset = symbol_table[-1].offset

        declared_temp_var = TemporaryVariable(new_tempID, "int", offset)
        addRecordToCurrentLevel(declared_temp_var)

    return new_tempID


def nextQuad():
    return label


def genQuad(op, oprnd1, oprnd2, target):
    global label, all_quads

    quad = Quad(op, oprnd1, oprnd2, target)

    all_quads[quad] = label

    label += 1


def emptyList():
    return []


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

def add_variable_records(name, datatype, offset):
    record = {
        'name' : name,
        'datatype' : datatype,
        'offset' : offset
    }
    allVariableRecords.append(record)


class Quad():
    def __init__(self, op, oprnd1, oprnd2, target):
        self.op = op
        self.oprnd1 = oprnd1
        self.oprnd2 = oprnd2
        self.target = target

    def __str__(self):
        return (str(self.op) + ", " + str(self.oprnd1) + ", " + str(self.oprnd2) + ", " + str(self.target))


class Entity:
    def __init__(self, name: str):
        self.name = name


class Variable(Entity):
    def __init__(self, name: str, datatype, offset: int):
        super().__init__(name)                      # variable's ID
        self.datatype = datatype                    # variable's data type
        self.offset = offset                        # distance from stack's head = 4 * len

    def __str__(self):
        return (str(self.name) + ", " + str(self.datatype) + ", " + str(self.offset))

class TemporaryVariable(Variable):
    def __init__(self, name: str, datatype, offset: int):
        super().__init__(name, datatype, offset)



class Subprogram(Entity):
    def __init__(self, name: str, startingQuad, formalParameters: list, framelength: int):
        super().__init__(name)                      # subprogram's ID
        self.startingQuad = startingQuad            # subprogram's first quad
        self.formalParameters = formalParameters    # list containing a subprogram's formal parameters
        self.framelength = framelength              # activation record's length in bytes


class Procedure(Subprogram):
        def __init__(self, name: str, startingQuad, formalParameters: list, framelength: int):
            super().__init__(name, startingQuad, formalParameters, framelength)

        def __str__(self):
            return str(self.name) + ", " + str(self.startingQuad) + ", "  + str(self.framelength)

class Function(Subprogram):
        def __init__(self, name: str, startingQuad, datatype, formalParameters: list, framelength: int):
            super().__init__(name, startingQuad, formalParameters, framelength)
            self.datatype = datatype

        def __str__(self):
            return str(self.name) + ", " + str(self.startingQuad) + ", " + str(self.datatype) + ", " + str(self.framelength)


class FormalParameter(Entity):
    def __init__(self, name: str, offset: int, datatype, mode: str):
        super().__init__(name)
        self.offset = offset
        self.datatype = datatype
        self.mode = mode

    def __str__(self):
        return str(self.name) + ", " + str(self.datatype) + ", " + str(self.offset) + ", " + str(self.mode)


class Parameter(FormalParameter):
    def __init__(self, name: str, datatype, mode: str, offset: int):
        super().__init__(name, datatype, mode)  # parameter's ID
        self.offset = offset


class SymbolicConstant(Entity):
    def __init__(self, name: str, datatype, value):
        super().__init__(name)
        self.datatype = datatype
        self.value = value




class Scope:
    def __init__(self, level: int):
        self.level = level
        self.offset = 12
        self.entity_list = []

    def __str__(self):

        return "Level: " + str(self.level) + ", " + str(self.offset)



def addRecordToCurrentLevel(record):
    global symbol_table

    symbol_table[-1].entity_list.append(record)
    symbol_table[-1].offset += 4



def addNewLevel():
    # invoked at the START of main program or a subprogram
    global symbol_table

    new_scope = Scope(len(symbol_table))

    symbol_table.append(new_scope)

def removeCurrentLevel():
    # invoked at the END of main program or a subprogram
    global symbol_table

    symbol_table.pop(-1)


def updateField(subprogram, field_value):
    # field_value is either framlength (int) or Quad object (Quad)
    global symbol_table

    if isinstance(field_value, int):
        subprogram.framelength += field_value


    elif isinstance(field_value, Quad):
        subprogram.startingQuad = field_value


def addFormalParameter(formal_parameter):
    global symbol_table
    symbol_table[-1][-1].formalParameters.append(formal_parameter)


def getRecord(recordName: str):
    entity = [entity for scope in reversed(symbol_table) for entity in scope.entity_list if entity.name == recordName][0]
    return entity


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
