import sys
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, SEMI, DOT, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'ID', 'ASSIGN', 'BEGIN', 'END',  'SEMI', 'DOT', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type = self.type, value = repr(self.value))

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {'BEGIN': Token('BEGIN', 'BEGIN'), 'END': Token('END', 'END')}

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1: self.current_char = None
        else:                             self.current_char = self.text[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1: return None
        else:                             return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace(): self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def _id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha(): return self._id()

            if self.current_char.isdigit(): return Token(INTEGER, self.integer())

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')

            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char  == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            self.error()

        return Token(EOF, None)

class BinOp(object):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Num(object):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class UnaryOp(object):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Compound(object):
    def __init__(self):
        self.children = []

class Assign(object):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(object):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class NoOp(object):
    pass

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type: self.current_token = self.lexer.get_next_token()
        else:                                     self.error()

    def program(self):
        node = self.compound_statement()
        self.eat(DOT)
        return node

    def compound_statement(self):
        self.eat(BEGIN)
        node = self.statement_list()
        self.eat(END)
        return node

    def statement_list(self):
        node = Compound()
        node.children.append(self.statement())
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            node.children.append(self.statement())
        return node

    def statement(self):
        if self.current_token.type == BEGIN: node = self.compound_statement()
        elif self.current_token.type == ID:  node = self.assignment_statement()
        else:                                node = self.empty()
        return node

    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:    self.eat(PLUS)
            elif token.type == MINUS: self.eat(MINUS)
            node = BinOp(left = node, op = token, right = self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:   self.eat(MUL)
            elif token.type == DIV: self.eat(DIV)
            node = BinOp(left = node, op = token, right = self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        if token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        node = self.variable()
        return node
    
    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()
        
    def parse(self):
        node = self.program()
        if self.current_token.type != EOF: self.error()
        return node

class Interpreter(object):
    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_BinOp(self, node):
        if node.op.type == PLUS:  return self.visit(node.left) + self.visit(node.right)
        if node.op.type == MINUS: return self.visit(node.left) - self.visit(node.right)
        if node.op.type == MUL:   return self.visit(node.left) * self.visit(node.right)
        if node.op.type == DIV:   return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:  return + self.visit(node.expr)
        if op == MINUS: return - self.visit(node.expr)

    def visit_Compound(self, node):
        for child in node.children: self.visit(child)

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None: raise NameError(repr(var_name))
        else:           return val

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None: return ''
        else:            return self.visit(tree)

def main():
    text = open(sys.argv[1], 'r').read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print interpreter.GLOBAL_SCOPE

if __name__ == '__main__':
    main()