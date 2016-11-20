class suffix(object):
    def __init__(self, expr):
        self.expr = expr
    
    def value(self):
        stack = []
        for i in self.expr:
            if i.isdigit():
                stack.append(i)
            else:
                b = stack.pop()
                a = stack.pop()
                result = eval(a + i + b)
                stack.append(str(result))
        return stack[0]
        
if __name__ == '__main__':
    expr = ['1','2','3','4','+','*','+','8','9','10','*','+','4','*','+','5','-']
    s = suffix(expr)
    print s.value()