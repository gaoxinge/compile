INTEGER, PLUS, MINUS, SPACE, EOF = 'INTEGER', 'PLUS', 'MINUS', 'SPACE', 'EOF'

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
        
    def error(self):
        raise Exception('Error parsing input.')
                
    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1: return Token(EOF, None)
        current_char = text[self.pos]
        if current_char.isdigit():
            self.pos += 1
            return Token(INTEGER, int(current_char))
        if current_char == '+':
            self.pos += 1
            return Token(PLUS, current_char)
        if current_char == '-':
            self.pos += 1
            return Token(MINUS, current_char)
        if current_char == ' ':
            self.pos += 1
            return Token(SPACE, current_char)
        self.error()
                
    def eat(self, token_type):
        if self.current_token.type == token_type: self.current_token = self.get_next_token()
        else:                                     self.error()
                
    def expr(self):
        left, op, right = '', '', ''
                
        self.current_token = self.get_next_token()
        while self.current_token.value != '+' and self.current_token.value != '-' and self.current_token.value != None:
            if self.current_token.value == ' ': self.eat(SPACE)
            else:
                left = left + repr(self.current_token.value)
                self.eat(INTEGER)
        if left == '': self.error()
                
        if self.current_token.value == '+':
            op = '+'
            self.eat(PLUS)
        else:
            op = '-'
            self.eat(MINUS)
        if op == '': self.error()
                
        while self.current_token.value != None:
            if self.current_token.value == ' ': self.eat(SPACE)
            else:
                right = right + repr(self.current_token.value)
                self.eat(INTEGER)
        if right == '': self.error()
                
        if op == '+': return int(left) + int(right)
        else:         return int(left) - int(right)
                
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