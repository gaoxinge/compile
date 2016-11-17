INTEGER, MUL, DIV, EOF = 'INTEGER', 'MUL', 'DIV', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    def __str__(self):
        return 'Token({type}, {value})'.format(type = self.type, value = repr(self.value))
                
    def __repr__(self):
        return self.__str__()
                
class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    ##########################################################
    # Lexer code                                             #
    ##########################################################
    def error(self):
        raise Exception('Invalid syntax.')
        
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
                        
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
                        
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
                        
            self.error()
        return Token(EOF, None)

    ##########################################################
    # Parser / Interpreter code                              #
    ##########################################################
    def eat(self, token_type):
        if self.current_token.type == token_type: self.current_token = self.get_next_token()
        else:                                     self.error()

    def term(self):
        token = self.current_token
        self.eat(INTEGER)
        return token.value
        
    def expr(self):
        self.current_token = self.get_next_token()
        result = self.term()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.term()
            if token.type == DIV:
                self.eat(DIV)
                result = result / self.term()
        return result 
                
def main():
    while True:
        try: text = raw_input('calc> ')
        except EOFError: break
        if not text: continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print result
                
if __name__ == '__main__':
    main()