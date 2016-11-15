INTEGER, PLUS, MINUS, MUL, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF'

class Token(object):
        def __init__(self, type, value):
                self.type = type
                self.value = value
        
        def __str__(self):
                return 'Token({type}, {value})'.format(type = self.type, value = repr(self.value))
                
        def __repr__(self):
                return self.__str__()

class Lexer(object):
        def __init__(self, text):
                self.text = text
                self.pos = 0
                self.current_char = self.text[self.pos]

        def error(self):
                raise Exception('Invalid character.')
        
        def advance(self):
                self.pos += 1
                if self.pos > len(self.text) - 1: self.current_char = None
                else:                             self.current_char = self.text[self.pos]
                
        def skip_whitespace(self):
                while self.current_char is not None and self.current_char.isspace(): self.advance()
        
        def integer(self):
                result = ''
                while self.current_char is not None and self.current_char.isdigit():
                        result += self.current_char
                        self.advance()
                return int(result)

        def get_next_token(self):
                while self.current_char is not None:
                        if self.current_char.isspace():
                                self.skip_whitespace()
                                continue
                        
                        if self.current_char.isdigit(): return Token(INTEGER, self.integer())

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
                        
                        self.error()
                
                return Token(EOF, None)       

class Interpreter(object):
        def __init__(self, lexer):
                self.lexer = lexer
                self.current_token = self.lexer.get_next_token()

        def error(self):
                raise Exception('Invalid syntax.')
                
        def eat(self, token_type):
                if self.current_token.type == token_type: self.current_token = self.lexer.get_next_token()
                else:                                     self.error()

        def factor(self):
                token = self.current_token
                self.eat(INTEGER)
                return token.value
        
        def expr(self):
                result = self.factor()
                while self.current_token.value is not None:
                        op1 = self.current_token.value
                        if op1 == '+': self.eat(PLUS)
                        if op1 == '-': self.eat(MINUS)
                        a = self.factor()
                        op2 = self.current_token.value
                        if op2 == '*': self.eat(MUL)
                        if op2 == '/': self.eat(DIV)
                        b = self.factor()
                        if op1 == '+' and op2 == '*': result = result + a * b
                        if op1 == '+' and op2 == '/': result = result + a / b
                        if op1 == '-' and op2 == '*': result = result - a * b
                        if op1 == '-' and op2 == '/': result = result - a / b
                return result
                
def main():
        while True:
                try: text = raw_input('calc> ')
                except EOFError: break
                if not text: continue
                lexer = Lexer(text)
                interpreter = Interpreter(lexer)
                result = interpreter.expr()
                print result
                
if __name__ == '__main__':
        main()
