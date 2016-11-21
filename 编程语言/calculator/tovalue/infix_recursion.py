class infix(object):
    def __init__(self, expr):
        self.expr = expr
        self.pos = 0

    def expression(self):
        result = self.term()
        while self.pos < len(self.expr) and self.expr[self.pos] in ('+', '-'):
            if self.expr[self.pos] == '+':
                self.pos += 1
                result = result + self.term()
            elif self.expr[self.pos] == '-':
                self.pos += 1
                result = result - self.term()
        return result
    
    def term(self):
        result = self.factor()
        while self.pos <len(self.expr) and self.expr[self.pos] in ('*', '/'):
            if self.expr[self.pos] == '*':
                self.pos += 1
                result = result * self.factor()
            elif self.expr[self.pos] == '/':
                self.pos += 1
                result = result / self.factor()
        return result
        
    def factor(self):
        if self.expr[self.pos].isdigit():
            result = int(self.expr[self.pos])
            self.pos += 1
        elif self.expr[self.pos] == '(':
            self.pos += 1
            result = self.expression()
            self.pos += 1
        return result 

if __name__ == '__main__':
    expr = ['1', '+', '2', '*', '(', '3', '+', '4', ')', '+', '(', '8', '+', '9', '*', '10', ')', '*', '4', '-', '5']
    s = infix(expr)
    print s.expression()