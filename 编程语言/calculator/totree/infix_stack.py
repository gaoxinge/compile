class BinOp(object):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
class Num(object):
    def __init__(self, value):
        self.value = value
        
class tree(object):
    def __init__(self, root):
        self.root = root
        
    def visit(self, node):
        func = getattr(self, 'visit_' + type(node).__name__)
        return func(node)
        
    def visit_BinOp(self, node):
        if node.op == '+': return self.visit(node.left) + self.visit(node.right)
        if node.op == '-': return self.visit(node.left) - self.visit(node.right)
        if node.op == '*': return self.visit(node.left) * self.visit(node.right)
        if node.op == '/': return self.visit(node.left) / self.visit(node.right)
        
    def visit_Num(self, node):
        return node.value
        
    def value(self):
        return self.visit(self.root)
        
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
            self.operand.append(BinOp(b, '+', a))
        elif self.operator[-1] == '-':
            self.operator.pop()
            self.operand.append(BinOp(b, '-', a))
        elif self.operator[-1] == '*':
            self.operator.pop()
            self.operand.append(BinOp(b, '*', a))
        elif self.operator[-1] == '/':
            self.operator.pop()
            self.operand.append(BinOp(b, '/', a))
    
    def tree(self):
        for i in self.expr:
            if i.isdigit():
                self.operand.append(Num(int(i)))
            elif i == '(':
                self.operator.append(i)
            elif i == ')':
                while self.operator[-1] != '(':
                    self.eval()
                self.operator.pop()
            elif i == '*' or i == '/':
                while self.operator and (self.operator[-1] == '*' or self.operator[-1] == '/'):
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
    root =  s.tree()

    s = tree(root)
    print s.value()