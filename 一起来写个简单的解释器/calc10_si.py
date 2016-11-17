import sys

(INTEGER, REAL, INTEGER_CONST, REAL_CONST, PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV, LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, SEMI, DOT, PROGRAM, VAR, COLON, COMMA, EOF) = ('INTEGER', 'REAL', 'INTEGER_CONST', 'REAL_CONST', 'PLUS', 'MINUS', 'MUL', 'INTEGER_DIV', 'REAL_DIV', 'LPAREN', 'RPAREN', 'ID', 'ASSIGN', 'BEGIN', 'END', 'SEMI', 'DOT', 'PROGRAM', 'VAR', 'COLON', 'COMMA', 'EOF')

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type = self.type, value = repr(self.value))

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {'PROGRAM': Token('PROGRAM', 'PROGRAM'), 'VAR': Token('VAR', 'VAR'), 'DIV': Token('INTEGER_DIV', 'DIV'), 'INTEGER': Token('INTEGER', 'INTEGER'), 'REAL': Token('REAL', 'REAL'), 'BEGIN': Token('BEGIN', 'BEGIN'), 'END': Token('END', 'END')}

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

    def skip_comment(self):
        while self.current_char != '}': self.advance()
        self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            token = Token('REAL_CONST', float(result))
        else: token = Token('INTEGER_CONST', int(result))
        return token

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
            
            if self.current_char == '{':
                self.skip_comment()
                continue
            
            if self.current_char.isalpha(): return self._id()

            if self.current_char.isdigit(): return self.number()

            if self.current_char == ':' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')
                
            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')
                
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

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
                return Token(FLOAT_DIV, '/')

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

class Program(object):
    def __init__(self, variable, block):
        self.variable = variable
        self.block = block

class Block(object):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement

class VarDecl(object):
    def __init__(self, variable, type):
        self.variable = variable
        self.type = type

class Type(object):
    def __init__(self, token):
        self.token = token
        self.value = token.value

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
        self.eat(PROGRAM)
        variable = self.variable()
        self.eat(SEMI)
        block = self.block()
        node = Program(variable, block)
        self.eat(DOT)
        return node

    def block(self):
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        node = Block(declarations, compound_statement)
        return node

    def declarations(self):
        nodes = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                nodes.extend(var_decl)
                self.eat(SEMI)
        return nodes
    
    def variable_declaration(self):
        nodes = [Var(self.current_token)]
        self.eat(ID)
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            nodes.append(Var(self.current_token))
            self.eat(ID)
        self.eat(COLON)
        type = self.type_spec()
        nodes = [VarDecl(var, type) for var in nodes]
        return nodes

    def type_spec(self):
        token = self.current_token
        if self.current_token.type == INTEGER: self.eat(INTEGER)
        else:                                  self.eat(REAL)
        node = Type(token)
        return node

    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        root = Compound()
        for node in nodes: root.children.append(node)
        return root

    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())
        if self.current_token.type == ID: self.error()
        return results

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

    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        return NoOp()

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
        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type == MUL:           self.eat(MUL)
            elif token.type == INTEGER_DIV: self.eat(INTEGER_DIV)
            elif token.type == FLOAT_DIV:   self.eat(FLOAT_DIV) 
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
        if token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        if token.type == REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        node = self.variable()
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF: self.error()
        return node

class Interpreter(object):
    def __init__(self, parser):
        self.parser = parser
        self.name = None
        self.GLOBAL_SCOPE = {}
        
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
    
    def visit_Program(self, node):
        self.name = node.variable.value
        self.visit(node.block)

    def visit_Block(self, node):
        self.visit(node.compound_statement)
    
    def visit_BinOp(self, node):
        if node.op.type == PLUS:          return self.visit(node.left) + self.visit(node.right)
        if node.op.type == MINUS:         return self.visit(node.left) - self.visit(node.right)
        if node.op.type == MUL:           return self.visit(node.left) * self.visit(node.right)
        if node.op.type == INTEGER_DIV:   return self.visit(node.left) // self.visit(node.right)
        if node.op.type == FLOAT_DIV:     return float(self.visit(node.left)) / float(self.visit(node.right))

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
        val_value = self.GLOBAL_SCOPE.get(var_name)
        if val_value is None: raise NameError(repr(var_name))
        else:                 return val_value

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
    print interpreter.name
    for k,v in interpreter.GLOBAL_SCOPE.items(): 
        print '%s = %s' % (k, v)

if __name__ == '__main__':
    main()