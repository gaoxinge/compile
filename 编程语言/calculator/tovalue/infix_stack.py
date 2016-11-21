class infix(object):
    def __init__(self, expr):
        self.expr = expr
        self.operand = []
        self.operator = []
    
    def eval(self):
        a = self.operand.pop()
        b = self.operand.pop()
        if self.operator[-1] == '+':
            self.operator.pop()
            self.operand.append(b + a)
        elif self.operator[-1] == '-':
            self.operator.pop()
            self.operand.append(b - a)
        elif self.operator[-1] == '*':
            self.operator.pop()
            self.operand.append(b * a)
        elif self.operator[-1] == '/':
            self.operator.pop()
            self.operand.append(b / a)
    
    def value(self):
        for i in self.expr:
            if i.isdigit():
                self.operand.append(int(i))
            elif i == '(':
                self.operator.append(i)
            elif i == ')':
                while self.operator[-1] != '(':
                    self.eval()
                self.operator.pop()
            elif i == '*' or i == '/':
                while self.operator and (self.operator[-1] ==  '*' or self.operator[-1] == '/'):
                    self.eval()
                self.operator.append(i)
            elif i == '+' or i == '-':
                while self.operator and self.operator[-1] != '(':
                    self.eval()
                self.operator.append(i)
        
        while self.operator:
            self.eval()
            
        return self.operand[-1]
        
if __name__ == '__main__':
    expr = ['1', '+', '2', '*', '(', '3', '+', '4', ')', '+', '(', '8', '+', '9', '*', '10', ')', '*', '4', '-', '5']
    s = infix(expr)
    print s.value()