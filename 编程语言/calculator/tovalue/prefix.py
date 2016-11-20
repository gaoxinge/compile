class prefix(object):
    def __init__(self, expr):
        self.expr = expr
        
    def value(self):
        stack = []
        for i in self.expr[::-1]:
            if i.isdigit():
                stack.append(i)
            else:
                a = stack.pop()
                b = stack.pop()
                result = eval(a + i + b)
                stack.append(str(result))
        return stack[0]
        
if __name__ == '__main__':
    expr = ['+','1','+','*','2','+','3','4','-','*','+','8','*','9','10','4','5']
    s = prefix(expr)
    print s.value()