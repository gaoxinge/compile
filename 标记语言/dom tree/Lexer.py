class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.bra = False
        
    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1: self.current_char = None
        else:                             self.current_char = self.text[self.pos]
        
    def character(self, symbol):
        result = ''
        while self.current_char is not None and self.current_char != symbol:
            result += self.current_char
            self.advance()
        return result
    
    def get_next_token(self):
        if self.current_char is not None:
            if self.current_char == '<':
                self.bra = True
                self.advance()
                return '<'
            elif self.current_char == '>':
                self.bra = False
                self.advance()
                return '>'
            elif self.bra:
                return self.character('>')
            else:
                return self.character('<')
        return None
