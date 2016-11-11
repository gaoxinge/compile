from AST import AST
from interpreter import interpreter

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.symbol = ['{', '}', ':', ';', ',', '(', ')', '.', '#', '~', '<', '>', '*', '+', '[', ']', '=', '|', '^']
        self.isString = False
        
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1: self.current_char = None
        else:                             self.current_char = self.text[self.pos]
        
    def get_next_token(self):
        if self.current_char is not None:
            s = ''
            if self.current_char in self.symbol:
                s = self.current_char
                self.advance()
                return s
            if self.current_char.isspace():
                self.advance()
                return s
            else:
                while self.current_char is not None and (self.isString or (not self.current_char.isspace() and not self.current_char in self.symbol)):
                    s += self.current_char
                    if self.current_char == '\'' or self.current_char == '\"':
                        self.isString = not self.isString
                    self.advance()
                return s
        return None

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.stack = [AST('root')]
        self.symbol = ['img', 'br', 'hr', 'col', 'area', 'link', 'meta', 'frame', 'input', 'param']
        self.isScript = False
        self.isStyle  = False

    def eat(self):
        self.current_token = self.lexer.get_next_token()

    def parser(self):
        while self.current_token is not None:
            if self.current_token == '<':
                self.eat()
                if self.current_token[0] == '!' or self.current_token in self.symbol:
                    self.stack[-1].childrens.append(AST(self.current_token))
                elif self.current_token[0] != '/':
                    if not self.isScript and not self.isStyle:
                        node = AST(self.current_token)
                        self.stack[-1].childrens.append(node)
                        self.stack.append(node)
                    if self.current_token == 'script': self.isScript = True
                    if self.current_token == 'style':  self.isStyle  = True
                else:
                    if self.current_token[1:] == self.stack[-1].name:
                        self.stack.pop()
                    if self.current_token[1:] == 'script': self.isScript = False
                    if self.current_token[1:] == 'style':  self.isStyle  = False
            self.eat()
        return self.stack[0]

if __name__  == '__main__':
    with open('index2.html', 'r') as f:
        html = f.read()

    lexer = Lexer(html)
    parser = Parser(lexer)
    root = parser.parser()
    s = interpreter(root)
    print s
