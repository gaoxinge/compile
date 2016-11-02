r = [0, 0, 0, 0]
m = {}

COMMAND, NUMBER, REGISTER, MEMORY, EOF = 'COMMAND', 'NUMBER', 'REGISTER', 'MEMORY', 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type = self.type, value = repr(self.value))

    def __repr__(self):
        return self.__str__()
    
class Lexer:
    def __init__(self, line):
        self.line = line
        self.pos = 0
        self.current_token = None
        self.current_char = self.line[self.pos]
        
    def error(self):
        raise Exception('invalid character')

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.line): self.current_char = None
        else:                          self.current_char = self.line[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def command(self):
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result
    
    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
                
    def get_next_token(self):
        result = ''
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return Token(COMMAND, self.command())

            if self.current_char.isdigit():
                return Token(NUMBER, self.number())

            if self.current_char == '_':
                self.advance()
                if self.current_char is not None and self.current_char.isdigit():
                    result = self.current_char
                    self.advance()
                    return Token(REGISTER, int(result))

            if self.current_char == '*':
                self.advance()
                if self.current_char is not None and self.current_char.isdigit():
                    result = self.current_char
                    self.advance()
                    return Token(MEMORY, int(result))

            self.error()

        return Token(EOF, None)


class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type: self.current_token = self.lexer.get_next_token()
        else:                                     self.error()

    def interpreter(self):
        tmp = self.current_token.value
        self.eat(COMMAND)
            
        if tmp == 'mov':
            tmp1 = self.current_token.value
            if self.current_token.type == NUMBER:
                self.eat(NUMBER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] = tmp1
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] = tmp1
            if self.current_token.type == REGISTER:
                self.eat(REGISTER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] = r[tmp1]
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] = r[tmp1]
            if self.current_token.type == MEMORY:
                self.eat(MEMORY)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] = m[r[tmp1]]

        if tmp == 'push':
            pass
            
        if tmp == 'pop':
            pass
            
        if tmp == 'add':
            tmp1 = self.current_token.value
            if self.current_token.type == NUMBER:
                self.eat(NUMBER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] += tmp1
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] += tmp1
            if self.current_token.type == REGISTER:
                self.eat(REGISTER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] += r[tmp1]
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] += r[tmp1]
            if self.current_token.type == MEMORY:
                self.eat(MEMORY)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] += m[r[tmp1]]
                
        if tmp == 'sub':
            tmp1 = self.current_token.value
            if self.current_token.type == NUMBER:
                self.eat(NUMBER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] -= tmp1
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] -= tmp1
            if self.current_token.type == REGISTER:
                self.eat(REGISTER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] -= r[tmp1]
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] -= r[tmp1]
            if self.current_token.type == MEMORY:
                self.eat(MEMORY)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] -= m[r[tmp1]]

        if tmp == 'mul':
            tmp1 = self.current_token.value
            if self.current_token.type == NUMBER:
                self.eat(NUMBER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] *= tmp1
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] *= tmp1
            if self.current_token.type == REGISTER:
                self.eat(REGISTER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] *= r[tmp1]
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] *= r[tmp1]
            if self.current_token.type == MEMORY:
                self.eat(MEMORY)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] *= m[r[tmp1]]

        if tmp == 'div':
            tmp1 = self.current_token.value
            if self.current_token.type == NUMBER:
                self.eat(NUMBER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] /= tmp1
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] /= tmp1
            if self.current_token.type == REGISTER:
                self.eat(REGISTER)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] /= r[tmp1]
                elif self.current_token.type == MEMORY:
                    self.eat(MEMORY)
                    m[r[tmp2]] /= r[tmp1]
            if self.current_token.type == MEMORY:
                self.eat(MEMORY)
                tmp2 = self.current_token.value
                if self.current_token.type == REGISTER:
                    self.eat(REGISTER)
                    r[tmp2] /= m[r[tmp1]]

        self.eat(EOF)
        
